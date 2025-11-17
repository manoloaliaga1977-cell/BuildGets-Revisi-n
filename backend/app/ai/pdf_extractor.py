"""
AI-Powered PDF Extractor
Uses AI to extract budget information from PDF files
"""
import pdfplumber
import base64
from typing import Optional, Dict, Any, List
from pathlib import Path
import json
import os
from anthropic import Anthropic
from ..models.budget import Budget, BudgetChapter, BudgetItem, BudgetMetadata
from decimal import Decimal
from datetime import datetime


class PDFExtractor:
    """Extract budget data from PDF using AI"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize PDF extractor with AI client

        Args:
            api_key: Anthropic API key (if None, reads from env)
        """
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        if self.api_key:
            self.client = Anthropic(api_key=self.api_key)
        else:
            self.client = None

    def extract_from_file(self, file_path: str) -> Budget:
        """
        Extract budget data from a PDF file

        Args:
            file_path: Path to PDF file

        Returns:
            Budget object with extracted data
        """
        # Extract text from PDF
        text_content = self._extract_text(file_path)

        # Try AI extraction if available
        if self.client:
            try:
                return self._extract_with_ai(file_path, text_content)
            except Exception as e:
                print(f"AI extraction failed: {e}")
                # Fallback to rule-based extraction
                return self._extract_with_rules(text_content)
        else:
            # Use rule-based extraction
            return self._extract_with_rules(text_content)

    def _extract_text(self, file_path: str) -> str:
        """Extract text content from PDF"""
        text_parts = []

        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    text_parts.append(text)

        return "\n\n".join(text_parts)

    def _extract_with_ai(self, file_path: str, text_content: str) -> Budget:
        """
        Use AI to extract structured budget data from PDF

        Args:
            file_path: Path to PDF file
            text_content: Extracted text content

        Returns:
            Budget object
        """
        # Prepare the prompt for Claude
        prompt = """Analiza este presupuesto y extrae la información estructurada en formato JSON.

El JSON debe tener esta estructura:
{
  "metadata": {
    "title": "Título del presupuesto",
    "owner": "Empresa/Propietario (si está disponible)",
    "date": "YYYY-MM-DD",
    "currency": "EUR"
  },
  "chapters": [
    {
      "code": "código del capítulo",
      "title": "título del capítulo",
      "items": [
        {
          "code": "código de partida",
          "unit": "unidad (ud, m2, ml, etc.)",
          "description": "descripción de la partida",
          "price": precio_unitario,
          "quantity": cantidad
        }
      ]
    }
  ]
}

Extrae TODOS los capítulos y partidas que encuentres. Los precios deben ser números decimales sin símbolos de moneda.

Contenido del presupuesto:
""" + text_content

        # Call Claude API
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4096,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )

        # Parse the response
        response_text = response.content[0].text

        # Extract JSON from response
        json_data = self._extract_json_from_text(response_text)

        # Convert to Budget object
        return self._json_to_budget(json_data)

    def _extract_json_from_text(self, text: str) -> Dict[str, Any]:
        """Extract JSON from AI response text"""
        # Try to find JSON in markdown code blocks
        if "```json" in text:
            start = text.index("```json") + 7
            end = text.index("```", start)
            json_text = text[start:end].strip()
        elif "```" in text:
            start = text.index("```") + 3
            end = text.index("```", start)
            json_text = text[start:end].strip()
        else:
            # Try to parse the whole text as JSON
            json_text = text.strip()

        return json.loads(json_text)

    def _json_to_budget(self, data: Dict[str, Any]) -> Budget:
        """Convert JSON data to Budget object"""
        # Parse metadata
        metadata_data = data.get('metadata', {})
        metadata = BudgetMetadata(
            title=metadata_data.get('title', 'Presupuesto'),
            owner=metadata_data.get('owner'),
            currency=metadata_data.get('currency', 'EUR'),
            date=self._parse_date(metadata_data.get('date'))
        )

        # Parse chapters
        chapters = []
        for chapter_data in data.get('chapters', []):
            chapter = self._parse_chapter(chapter_data)
            if chapter:
                chapters.append(chapter)

        return Budget(metadata=metadata, chapters=chapters)

    def _parse_chapter(self, data: Dict[str, Any]) -> Optional[BudgetChapter]:
        """Parse chapter from JSON data"""
        try:
            items = []
            for item_data in data.get('items', []):
                item = BudgetItem(
                    code=str(item_data.get('code', '')),
                    unit=str(item_data.get('unit', 'ud')),
                    description=str(item_data.get('description', '')),
                    price=Decimal(str(item_data.get('price', 0))),
                    quantity=Decimal(str(item_data.get('quantity', 1)))
                )
                items.append(item)

            subchapters = []
            for subchapter_data in data.get('subchapters', []):
                subchapter = self._parse_chapter(subchapter_data)
                if subchapter:
                    subchapters.append(subchapter)

            return BudgetChapter(
                code=str(data.get('code', '')),
                title=str(data.get('title', '')),
                items=items,
                subchapters=subchapters
            )
        except Exception as e:
            print(f"Error parsing chapter: {e}")
            return None

    def _parse_date(self, date_str: Optional[str]) -> datetime:
        """Parse date string to datetime"""
        if not date_str:
            return datetime.now()

        try:
            # Try different date formats
            for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y']:
                try:
                    return datetime.strptime(date_str, fmt)
                except:
                    continue
            return datetime.now()
        except:
            return datetime.now()

    def _extract_with_rules(self, text_content: str) -> Budget:
        """
        Fallback: Extract budget using rule-based approach

        Args:
            text_content: Text extracted from PDF

        Returns:
            Budget object with basic extraction
        """
        import re

        budget = Budget()
        current_chapter = None

        lines = text_content.split('\n')

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Try to detect chapter (usually uppercase or specific format)
            if re.match(r'^[A-Z\s]{10,}$', line) or re.match(r'^\d+\.\s+[A-Z]', line):
                # New chapter
                code = f"CAP{len(budget.chapters) + 1:02d}"
                current_chapter = BudgetChapter(code=code, title=line)
                budget.chapters.append(current_chapter)

            # Try to detect budget items (code, description, quantities, prices)
            # Pattern: code description quantity unit price total
            item_match = re.match(
                r'^([A-Z0-9\.]+)\s+(.+?)\s+(\d+(?:,\d+)?)\s+([a-zA-Z]+)\s+(\d+(?:,\d+)?)\s+(\d+(?:,\d+)?)',
                line
            )

            if item_match and current_chapter:
                code = item_match.group(1)
                description = item_match.group(2).strip()
                quantity = item_match.group(3).replace(',', '.')
                unit = item_match.group(4)
                price = item_match.group(5).replace(',', '.')

                item = BudgetItem(
                    code=code,
                    description=description,
                    quantity=Decimal(quantity),
                    unit=unit,
                    price=Decimal(price)
                )
                current_chapter.items.append(item)

        # If no chapters were detected, create a default one
        if not budget.chapters:
            budget.chapters.append(BudgetChapter(
                code="CAP01",
                title="Presupuesto General"
            ))

        return budget
