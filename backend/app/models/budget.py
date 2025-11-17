"""
Data models for budget representation
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
from decimal import Decimal


class BudgetItem(BaseModel):
    """Represents a single budget item/concept"""
    code: str = Field(..., description="Item code")
    unit: str = Field(default="ud", description="Unit of measurement")
    description: str = Field(..., description="Item description")
    price: Decimal = Field(..., description="Unit price")
    quantity: Decimal = Field(default=Decimal("1.0"), description="Quantity")

    @property
    def total(self) -> Decimal:
        """Calculate total price"""
        return self.price * self.quantity

    class Config:
        json_encoders = {
            Decimal: lambda v: float(v)
        }


class BudgetChapter(BaseModel):
    """Represents a budget chapter/section"""
    code: str = Field(..., description="Chapter code")
    title: str = Field(..., description="Chapter title")
    items: List[BudgetItem] = Field(default_factory=list, description="Items in this chapter")
    subchapters: List['BudgetChapter'] = Field(default_factory=list, description="Subchapters")

    @property
    def total(self) -> Decimal:
        """Calculate total for this chapter"""
        items_total = sum((item.total for item in self.items), Decimal("0"))
        subchapters_total = sum((sub.total for sub in self.subchapters), Decimal("0"))
        return items_total + subchapters_total

    class Config:
        json_encoders = {
            Decimal: lambda v: float(v)
        }


class BudgetMetadata(BaseModel):
    """Budget metadata and general information"""
    title: str = Field(default="Presupuesto", description="Budget title")
    owner: Optional[str] = Field(default=None, description="Budget owner/company")
    date: datetime = Field(default_factory=datetime.now, description="Budget date")
    version: str = Field(default="1.0", description="Budget version")
    currency: str = Field(default="EUR", description="Currency")
    comments: Optional[str] = Field(default=None, description="Additional comments")


class Budget(BaseModel):
    """Complete budget structure"""
    metadata: BudgetMetadata = Field(default_factory=BudgetMetadata)
    chapters: List[BudgetChapter] = Field(default_factory=list, description="Budget chapters")

    @property
    def total(self) -> Decimal:
        """Calculate total budget"""
        return sum((chapter.total for chapter in self.chapters), Decimal("0"))

    @property
    def total_items(self) -> int:
        """Count total number of items"""
        count = 0
        for chapter in self.chapters:
            count += len(chapter.items)
            count += sum(len(sub.items) for sub in chapter.subchapters)
        return count

    class Config:
        json_encoders = {
            Decimal: lambda v: float(v),
            datetime: lambda v: v.isoformat()
        }


# Allow forward references
BudgetChapter.model_rebuild()
