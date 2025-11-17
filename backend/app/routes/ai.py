"""
AI enhancement routes
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
import tempfile
import os
from ..parsers.bc3_parser import BC3Parser
from ..ai.budget_enhancer import BudgetEnhancer
from ..models.budget import Budget

router = APIRouter(prefix="/ai", tags=["ai"])

# Initialize services
bc3_parser = BC3Parser()
budget_enhancer = BudgetEnhancer()


@router.post("/enhance-budget")
async def enhance_budget(budget_data: Budget):
    """
    Enhance budget descriptions using AI

    Args:
        budget_data: Budget object as JSON

    Returns:
        Enhanced budget
    """
    try:
        enhanced_budget = budget_enhancer.enhance_descriptions(budget_data)
        return enhanced_budget.model_dump()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Enhancement failed: {str(e)}")


@router.post("/validate-budget")
async def validate_budget(budget_data: Budget):
    """
    Validate budget and get suggestions

    Args:
        budget_data: Budget object as JSON

    Returns:
        Validation results with warnings and suggestions
    """
    try:
        validation_result = budget_enhancer.validate_budget(budget_data)
        return validation_result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Validation failed: {str(e)}")


@router.post("/enhance-bc3")
async def enhance_bc3_file(file: UploadFile = File(...)):
    """
    Enhance a BC3 file using AI

    Args:
        file: BC3 file to enhance

    Returns:
        Enhanced budget as JSON
    """
    if not file.filename.endswith('.bc3'):
        raise HTTPException(status_code=400, detail="File must be a BC3 file")

    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.bc3') as temp_bc3:
            content = await file.read()
            temp_bc3.write(content)
            temp_bc3_path = temp_bc3.name

        # Parse BC3
        budget = bc3_parser.parse_file(temp_bc3_path)

        # Enhance
        enhanced_budget = budget_enhancer.enhance_descriptions(budget)

        # Clean up temp file
        os.unlink(temp_bc3_path)

        # Return enhanced budget
        return enhanced_budget.model_dump()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Enhancement failed: {str(e)}")
