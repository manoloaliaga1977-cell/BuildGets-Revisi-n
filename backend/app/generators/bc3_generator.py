"""
BC3 Format Generator
Generates FIEBDC-3 (BC3) budget files from Budget objects
"""
from typing import List, Set
from datetime import datetime
from ..models.budget import Budget, BudgetChapter, BudgetItem


class BC3Generator:
    """Generator for BC3 (FIEBDC-3) format files"""

    FIELD_SEPARATOR = '|'
    RECORD_SEPARATOR = '~'
    SUBFIELD_SEPARATOR = '\\'

    def __init__(self):
        self.generated_codes: Set[str] = set()

    def generate_file(self, budget: Budget, file_path: str):
        """Generate a BC3 file from a Budget object"""
        content = self.generate_content(budget)

        with open(file_path, 'w', encoding='latin-1') as f:
            f.write(content)

    def generate_content(self, budget: Budget) -> str:
        """Generate BC3 content string from Budget object"""
        records = []

        # Version record
        records.append(self._generate_version_record())

        # General information records
        records.extend(self._generate_info_records(budget.metadata))

        # Root record
        root_code = "##"
        records.append(self._generate_root_decomposition(root_code, budget.chapters))

        # Generate all chapter and item records
        for chapter in budget.chapters:
            records.extend(self._generate_chapter_records(chapter))

        return self.RECORD_SEPARATOR.join(records) + self.RECORD_SEPARATOR

    def _generate_version_record(self) -> str:
        """Generate version record"""
        # V|FIEBDC-3/2004|
        return f"V{self.FIELD_SEPARATOR}FIEBDC-3/2004{self.FIELD_SEPARATOR}"

    def _generate_info_records(self, metadata) -> List[str]:
        """Generate general information records"""
        records = []

        # Title
        records.append(
            f"K{self.FIELD_SEPARATOR}1{self.FIELD_SEPARATOR}{metadata.title}{self.FIELD_SEPARATOR}"
        )

        # Owner
        if metadata.owner:
            records.append(
                f"K{self.FIELD_SEPARATOR}2{self.FIELD_SEPARATOR}{metadata.owner}{self.FIELD_SEPARATOR}"
            )

        # Date
        date_str = metadata.date.strftime('%d/%m/%Y')
        records.append(
            f"K{self.FIELD_SEPARATOR}3{self.FIELD_SEPARATOR}{date_str}{self.FIELD_SEPARATOR}"
        )

        # Currency
        records.append(
            f"K{self.FIELD_SEPARATOR}4{self.FIELD_SEPARATOR}{metadata.currency}{self.FIELD_SEPARATOR}"
        )

        return records

    def _generate_root_decomposition(self, root_code: str, chapters: List[BudgetChapter]) -> str:
        """Generate root decomposition record"""
        children_str = ""

        for chapter in chapters:
            if children_str:
                children_str += self.SUBFIELD_SEPARATOR

            children_str += f"{chapter.code}{self.SUBFIELD_SEPARATOR}1{self.SUBFIELD_SEPARATOR}{self.SUBFIELD_SEPARATOR}"

        return f"D{self.FIELD_SEPARATOR}{root_code}{self.FIELD_SEPARATOR}{children_str}{self.FIELD_SEPARATOR}"

    def _generate_chapter_records(self, chapter: BudgetChapter) -> List[str]:
        """Generate all records for a chapter"""
        records = []

        # Chapter concept record
        if chapter.code not in self.generated_codes:
            records.append(self._generate_concept_record(
                code=chapter.code,
                unit="",
                description=chapter.title,
                price=float(chapter.total),
                concept_type="0"  # 0 = chapter
            ))
            self.generated_codes.add(chapter.code)

        # Chapter decomposition record
        children_str = ""

        # Add items
        for item in chapter.items:
            if children_str:
                children_str += self.SUBFIELD_SEPARATOR

            quantity_str = str(float(item.quantity)).replace('.', ',')
            children_str += f"{item.code}{self.SUBFIELD_SEPARATOR}{quantity_str}{self.SUBFIELD_SEPARATOR}{self.SUBFIELD_SEPARATOR}"

            # Generate item concept record
            if item.code not in self.generated_codes:
                records.append(self._generate_concept_record(
                    code=item.code,
                    unit=item.unit,
                    description=item.description,
                    price=float(item.price),
                    concept_type="1"  # 1 = item
                ))
                self.generated_codes.add(item.code)

        # Add subchapters
        for subchapter in chapter.subchapters:
            if children_str:
                children_str += self.SUBFIELD_SEPARATOR

            children_str += f"{subchapter.code}{self.SUBFIELD_SEPARATOR}1{self.SUBFIELD_SEPARATOR}{self.SUBFIELD_SEPARATOR}"

            # Recursively generate subchapter records
            records.extend(self._generate_chapter_records(subchapter))

        # Decomposition record
        if children_str:
            records.append(
                f"D{self.FIELD_SEPARATOR}{chapter.code}{self.FIELD_SEPARATOR}{children_str}{self.FIELD_SEPARATOR}"
            )

        return records

    def _generate_concept_record(self, code: str, unit: str, description: str,
                                  price: float, concept_type: str = "1") -> str:
        """Generate a concept record"""
        price_str = f"{price:.2f}".replace('.', ',')

        return (
            f"C{self.FIELD_SEPARATOR}"
            f"{code}{self.FIELD_SEPARATOR}"
            f"{unit}{self.FIELD_SEPARATOR}"
            f"{description}{self.FIELD_SEPARATOR}"
            f"{price_str}{self.FIELD_SEPARATOR}"
            f"{self.FIELD_SEPARATOR}"
            f"{concept_type}{self.FIELD_SEPARATOR}"
        )
