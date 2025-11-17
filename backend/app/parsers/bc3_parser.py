"""
BC3 Format Parser
Parses FIEBDC-3 (BC3) budget files
"""
import re
from typing import Dict, List, Tuple, Optional
from decimal import Decimal
from datetime import datetime
from ..models.budget import Budget, BudgetChapter, BudgetItem, BudgetMetadata


class BC3Parser:
    """Parser for BC3 (FIEBDC-3) format files"""

    # BC3 format separators
    FIELD_SEPARATOR = '|'
    RECORD_SEPARATOR = '~'
    SUBFIELD_SEPARATOR = '\\'

    def __init__(self):
        self.records: Dict[str, Dict] = {}
        self.metadata = BudgetMetadata()

    def parse_file(self, file_path: str) -> Budget:
        """Parse a BC3 file and return a Budget object"""
        with open(file_path, 'r', encoding='latin-1') as f:
            content = f.read()

        return self.parse_content(content)

    def parse_content(self, content: str) -> Budget:
        """Parse BC3 content string"""
        # Split into records
        records = content.split(self.RECORD_SEPARATOR)

        # First pass: collect all records
        for record in records:
            if not record.strip():
                continue
            self._parse_record(record)

        # Second pass: build budget structure
        budget = self._build_budget()
        return budget

    def _parse_record(self, record: str):
        """Parse a single BC3 record"""
        if not record or len(record) < 2:
            return

        record_type = record[0]
        fields = record[1:].split(self.FIELD_SEPARATOR)

        if record_type == 'V':
            # Version record
            self._parse_version_record(fields)
        elif record_type == 'C':
            # Concept record (item)
            self._parse_concept_record(fields)
        elif record_type == 'D':
            # Decomposition record
            self._parse_decomposition_record(fields)
        elif record_type == 'K':
            # General information
            self._parse_info_record(fields)

    def _parse_version_record(self, fields: List[str]):
        """Parse version information"""
        if len(fields) > 0:
            # Format version
            pass

    def _parse_concept_record(self, fields: List[str]):
        """Parse concept/item record"""
        if len(fields) < 2:
            return

        code = fields[0].strip()

        record_data = {
            'code': code,
            'unit': fields[1].strip() if len(fields) > 1 else 'ud',
            'description': fields[2].strip() if len(fields) > 2 else '',
            'price': self._parse_decimal(fields[3]) if len(fields) > 3 else Decimal('0'),
            'type': fields[5].strip() if len(fields) > 5 else '0',
        }

        self.records[code] = record_data

    def _parse_decomposition_record(self, fields: List[str]):
        """Parse decomposition (parent-child relationship) record"""
        if len(fields) < 2:
            return

        parent_code = fields[0].strip()

        # Parse child items
        if parent_code not in self.records:
            self.records[parent_code] = {
                'code': parent_code,
                'children': []
            }

        if 'children' not in self.records[parent_code]:
            self.records[parent_code]['children'] = []

        # Children are in field 1, separated by subfield separator
        if len(fields) > 1:
            children_data = fields[1].split(self.SUBFIELD_SEPARATOR)
            for i in range(0, len(children_data), 4):
                if i < len(children_data):
                    child_code = children_data[i].strip()
                    quantity = self._parse_decimal(children_data[i+1]) if i+1 < len(children_data) else Decimal('1')

                    self.records[parent_code]['children'].append({
                        'code': child_code,
                        'quantity': quantity
                    })

    def _parse_info_record(self, fields: List[str]):
        """Parse general information record"""
        if len(fields) > 0:
            info_type = fields[0].strip()

            if info_type == '1':  # Title
                self.metadata.title = fields[1].strip() if len(fields) > 1 else "Presupuesto"
            elif info_type == '2':  # Owner
                self.metadata.owner = fields[1].strip() if len(fields) > 1 else None
            elif info_type == '3':  # Date
                if len(fields) > 1:
                    try:
                        date_str = fields[1].strip()
                        self.metadata.date = datetime.strptime(date_str, '%d/%m/%Y')
                    except:
                        pass

    def _parse_decimal(self, value: str) -> Decimal:
        """Parse decimal value from string"""
        try:
            # BC3 uses comma as decimal separator
            clean_value = value.strip().replace(',', '.')
            return Decimal(clean_value)
        except:
            return Decimal('0')

    def _build_budget(self) -> Budget:
        """Build Budget object from parsed records"""
        budget = Budget(metadata=self.metadata)

        # Find root items (chapters)
        root_code = self._find_root_code()

        if root_code and root_code in self.records:
            root_record = self.records[root_code]
            if 'children' in root_record:
                for child in root_record['children']:
                    chapter = self._build_chapter(child['code'])
                    if chapter:
                        budget.chapters.append(chapter)
        else:
            # If no root found, treat all items without parents as chapters
            for code, record in self.records.items():
                if record.get('type') == '0':  # Chapter type
                    chapter = self._build_chapter(code)
                    if chapter:
                        budget.chapters.append(chapter)

        return budget

    def _find_root_code(self) -> Optional[str]:
        """Find the root code of the budget"""
        # Usually the first record or a special root code
        for code, record in self.records.items():
            if 'children' in record and len(record['children']) > 0:
                # Check if this code is not a child of any other
                is_root = True
                for other_code, other_record in self.records.items():
                    if 'children' in other_record:
                        if any(c['code'] == code for c in other_record['children']):
                            is_root = False
                            break
                if is_root:
                    return code
        return None

    def _build_chapter(self, code: str) -> Optional[BudgetChapter]:
        """Build a chapter from a code"""
        if code not in self.records:
            return None

        record = self.records[code]

        chapter = BudgetChapter(
            code=code,
            title=record.get('description', code)
        )

        # Add children
        if 'children' in record:
            for child in record['children']:
                child_code = child['code']
                quantity = child['quantity']

                if child_code in self.records:
                    child_record = self.records[child_code]

                    # Determine if it's a subchapter or an item
                    if 'children' in child_record and len(child_record['children']) > 0:
                        # It's a subchapter
                        subchapter = self._build_chapter(child_code)
                        if subchapter:
                            chapter.subchapters.append(subchapter)
                    else:
                        # It's an item
                        item = BudgetItem(
                            code=child_code,
                            unit=child_record.get('unit', 'ud'),
                            description=child_record.get('description', ''),
                            price=child_record.get('price', Decimal('0')),
                            quantity=quantity
                        )
                        chapter.items.append(item)

        return chapter
