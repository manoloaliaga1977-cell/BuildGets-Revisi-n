"""
BC3 Format Parser - MEJORADO
Parses FIEBDC-3 (BC3) budget files con manejo robusto de errores
"""
import re
from typing import Dict, List, Optional
from decimal import Decimal, InvalidOperation
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
        try:
            # Intentar con diferentes encodings
            encodings = ['latin-1', 'utf-8', 'iso-8859-1', 'cp1252']
            content = None

            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        content = f.read()
                    print(f"✅ Archivo leído con encoding: {encoding}")
                    break
                except UnicodeDecodeError:
                    continue

            if content is None:
                raise ValueError("No se pudo leer el archivo con ningún encoding conocido")

            return self.parse_content(content)

        except Exception as e:
            print(f"❌ Error leyendo archivo BC3: {str(e)}")
            raise

    def parse_content(self, content: str) -> Budget:
        """Parse BC3 content string"""
        print(f"📄 Parseando BC3... ({len(content)} caracteres)")

        # Limpiar el contenido
        content = content.strip()

        # Split into records
        records = content.split(self.RECORD_SEPARATOR)
        print(f"📋 Encontrados {len(records)} registros")

        # First pass: collect all records
        for i, record in enumerate(records):
            if not record.strip():
                continue
            try:
                self._parse_record(record)
            except Exception as e:
                print(f"⚠️ Error en registro {i}: {str(e)}")
                continue

        print(f"✅ Parseados {len(self.records)} conceptos")

        # Second pass: build budget structure
        budget = self._build_budget()
        print(f"✅ Budget creado: {len(budget.chapters)} capítulos, Total: {float(budget.total):.2f}")
        return budget

    def _parse_record(self, record: str):
        """Parse a single BC3 record"""
        if not record or len(record) < 2:
            return

        record_type = record[0]
        fields = record[1:].split(self.FIELD_SEPARATOR)

        if record_type == 'V':
            self._parse_version_record(fields)
        elif record_type == 'C':
            self._parse_concept_record(fields)
        elif record_type == 'D':
            self._parse_decomposition_record(fields)
        elif record_type == 'K':
            self._parse_info_record(fields)

    def _parse_version_record(self, fields: List[str]):
        """Parse version information"""
        if len(fields) > 0:
            print(f"📌 Versión BC3: {fields[0]}")

    def _parse_concept_record(self, fields: List[str]):
        """Parse concept/item record"""
        if len(fields) < 2:
            return

        code = fields[0].strip()
        if not code:
            return

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
        if not parent_code:
            return

        if parent_code not in self.records:
            self.records[parent_code] = {
                'code': parent_code,
                'children': []
            }

        if 'children' not in self.records[parent_code]:
            self.records[parent_code]['children'] = []

        # Children are in field 1
        if len(fields) > 1 and fields[1]:
            children_data = fields[1].split(self.SUBFIELD_SEPARATOR)
            for i in range(0, len(children_data), 4):
                if i < len(children_data) and children_data[i].strip():
                    child_code = children_data[i].strip()
                    quantity = self._parse_decimal(children_data[i+1]) if i+1 < len(children_data) else Decimal('1')

                    self.records[parent_code]['children'].append({
                        'code': child_code,
                        'quantity': quantity
                    })

    def _parse_info_record(self, fields: List[str]):
        """Parse general information record"""
        if len(fields) == 0:
            return

        info_type = fields[0].strip()

        if info_type == '1':  # Title
            self.metadata.title = fields[1].strip() if len(fields) > 1 else "Presupuesto"
        elif info_type == '2':  # Owner
            self.metadata.owner = fields[1].strip() if len(fields) > 1 else None
        elif info_type == '3':  # Date
            if len(fields) > 1:
                try:
                    date_str = fields[1].strip()
                    # Probar diferentes formatos de fecha
                    for fmt in ['%d/%m/%Y', '%Y-%m-%d', '%d-%m-%Y']:
                        try:
                            self.metadata.date = datetime.strptime(date_str, fmt)
                            break
                        except ValueError:
                            continue
                except Exception as e:
                    print(f"⚠️ Error parseando fecha: {e}")

    def _parse_decimal(self, value: str) -> Decimal:
        """Parse decimal value from string with robust error handling"""
        try:
            if not value or not value.strip():
                return Decimal('0')

            # Limpiar el valor
            clean_value = value.strip()

            # BC3 usa coma como separador decimal
            clean_value = clean_value.replace(',', '.')

            # Eliminar espacios y caracteres no numéricos excepto punto y signo menos
            clean_value = re.sub(r'[^\d.\-]', '', clean_value)

            if not clean_value or clean_value == '-':
                return Decimal('0')

            return Decimal(clean_value)
        except (InvalidOperation, ValueError) as e:
            print(f"⚠️ Error parseando decimal '{value}': {e}")
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
            # Si no hay root, buscar capítulos (type = 0)
            chapter_codes = [code for code, rec in self.records.items()
                           if rec.get('type') == '0' and 'children' in rec]

            if not chapter_codes:
                # Si tampoco hay capítulos marcados, crear uno con todos los items
                default_chapter = BudgetChapter(
                    code="CAP01",
                    title="Presupuesto General"
                )

                for code, record in self.records.items():
                    if 'children' not in record and record.get('type') != '0':
                        item = BudgetItem(
                            code=code,
                            unit=record.get('unit', 'ud'),
                            description=record.get('description', ''),
                            price=record.get('price', Decimal('0')),
                            quantity=Decimal('1')
                        )
                        default_chapter.items.append(item)

                if default_chapter.items:
                    budget.chapters.append(default_chapter)
            else:
                for code in chapter_codes:
                    chapter = self._build_chapter(code)
                    if chapter:
                        budget.chapters.append(chapter)

        return budget

    def _find_root_code(self) -> Optional[str]:
        """Find the root code of the budget"""
        # Buscar código especial de root (## o similar)
        if '##' in self.records:
            return '##'

        # Buscar el código que tenga hijos pero no sea hijo de nadie
        all_children = set()
        for code, record in self.records.items():
            if 'children' in record:
                for child in record['children']:
                    all_children.add(child['code'])

        for code, record in self.records.items():
            if 'children' in record and code not in all_children:
                return code

        return None

    def _build_chapter(self, code: str) -> Optional[BudgetChapter]:
        """Build a chapter from a code"""
        if code not in self.records:
            print(f"⚠️ Código {code} no encontrado en records")
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
                else:
                    print(f"⚠️ Código hijo {child_code} no encontrado")

        return chapter
