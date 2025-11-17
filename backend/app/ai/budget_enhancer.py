"""
AI Budget Enhancer
Uses AI to improve, validate and enrich budget data
"""
import os
import json
from typing import Optional, List, Dict, Any
from anthropic import Anthropic
from ..models.budget import Budget, BudgetChapter, BudgetItem


class BudgetEnhancer:
    """Enhance budget data using AI"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize budget enhancer

        Args:
            api_key: Anthropic API key (if None, reads from env)
        """
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        if self.api_key:
            self.client = Anthropic(api_key=self.api_key)
        else:
            self.client = None

    def enhance_descriptions(self, budget: Budget) -> Budget:
        """
        Improve item descriptions using AI

        Args:
            budget: Budget object to enhance

        Returns:
            Enhanced budget with improved descriptions
        """
        if not self.client:
            return budget

        for chapter in budget.chapters:
            self._enhance_chapter_descriptions(chapter)

        return budget

    def _enhance_chapter_descriptions(self, chapter: BudgetChapter):
        """Enhance descriptions in a chapter"""
        if not chapter.items:
            return

        # Prepare items for enhancement
        items_data = []
        for item in chapter.items:
            items_data.append({
                'code': item.code,
                'description': item.description,
                'unit': item.unit
            })

        # Ask AI to improve descriptions
        prompt = f"""Mejora las siguientes descripciones de partidas de presupuesto de construcción.
Hazlas más claras, profesionales y detalladas, pero mantén la información técnica esencial.

Partidas:
{json.dumps(items_data, indent=2, ensure_ascii=False)}

Responde SOLO con un JSON array con el mismo formato, incluyendo las descripciones mejoradas:
[
  {{
    "code": "código",
    "description": "descripción mejorada",
    "unit": "unidad"
  }}
]
"""

        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2048,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            response_text = response.content[0].text

            # Extract JSON
            if "```json" in response_text:
                start = response_text.index("```json") + 7
                end = response_text.index("```", start)
                json_text = response_text[start:end].strip()
            elif "```" in response_text:
                start = response_text.index("```") + 3
                end = response_text.index("```", start)
                json_text = response_text[start:end].strip()
            else:
                json_text = response_text.strip()

            enhanced_items = json.loads(json_text)

            # Update descriptions
            for i, enhanced in enumerate(enhanced_items):
                if i < len(chapter.items):
                    chapter.items[i].description = enhanced['description']

        except Exception as e:
            print(f"Error enhancing descriptions: {e}")

        # Recursively enhance subchapters
        for subchapter in chapter.subchapters:
            self._enhance_chapter_descriptions(subchapter)

    def validate_budget(self, budget: Budget) -> Dict[str, Any]:
        """
        Validate budget and find potential issues

        Args:
            budget: Budget to validate

        Returns:
            Dictionary with validation results
        """
        if not self.client:
            return self._basic_validation(budget)

        # Prepare budget summary for AI
        summary = self._budget_to_summary(budget)

        prompt = f"""Analiza este presupuesto y detecta posibles problemas o inconsistencias:

{summary}

Busca:
1. Precios inusuales o sospechosos (muy altos o muy bajos)
2. Descripciones incompletas o poco claras
3. Unidades incorrectas o inconsistentes
4. Partidas duplicadas
5. Errores de cálculo
6. Falta de información importante

Responde en JSON con este formato:
{{
  "is_valid": true/false,
  "warnings": ["lista de advertencias"],
  "errors": ["lista de errores"],
  "suggestions": ["lista de sugerencias de mejora"]
}}
"""

        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2048,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            response_text = response.content[0].text

            # Extract JSON
            if "```json" in response_text:
                start = response_text.index("```json") + 7
                end = response_text.index("```", start)
                json_text = response_text[start:end].strip()
            elif "```" in response_text:
                start = response_text.index("```") + 3
                end = response_text.index("```", start)
                json_text = response_text[start:end].strip()
            else:
                json_text = response_text.strip()

            return json.loads(json_text)

        except Exception as e:
            print(f"Error validating budget: {e}")
            return self._basic_validation(budget)

    def _budget_to_summary(self, budget: Budget) -> str:
        """Convert budget to text summary for AI analysis"""
        lines = []
        lines.append(f"Título: {budget.metadata.title}")
        lines.append(f"Total: {float(budget.total):.2f} {budget.metadata.currency}")
        lines.append(f"Partidas: {budget.total_items}")
        lines.append("\nCapítulos:")

        for chapter in budget.chapters:
            lines.append(f"\n{chapter.code} - {chapter.title} (Total: {float(chapter.total):.2f})")
            for item in chapter.items[:10]:  # Limit to first 10 items per chapter
                lines.append(
                    f"  {item.code}: {item.description} | "
                    f"{float(item.quantity)} {item.unit} x {float(item.price)} = {float(item.total)}"
                )
            if len(chapter.items) > 10:
                lines.append(f"  ... y {len(chapter.items) - 10} partidas más")

        return "\n".join(lines)

    def _basic_validation(self, budget: Budget) -> Dict[str, Any]:
        """Basic validation without AI"""
        warnings = []
        errors = []

        # Check for empty budget
        if not budget.chapters:
            errors.append("El presupuesto no tiene capítulos")

        # Check for chapters without items
        for chapter in budget.chapters:
            if not chapter.items and not chapter.subchapters:
                warnings.append(f"Capítulo '{chapter.title}' está vacío")

            # Check for zero prices
            for item in chapter.items:
                if item.price == 0:
                    warnings.append(f"Partida '{item.code}' tiene precio 0")
                if item.quantity == 0:
                    warnings.append(f"Partida '{item.code}' tiene cantidad 0")

        return {
            "is_valid": len(errors) == 0,
            "warnings": warnings,
            "errors": errors,
            "suggestions": []
        }
