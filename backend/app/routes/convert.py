"""
Conversion routes for budget formats
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import tempfile
import os
from pathlib import Path
from ..parsers.bc3_parser import BC3Parser
from ..generators.bc3_generator import BC3Generator
from ..generators.pdf_generator import PDFGenerator
from ..ai.pdf_extractor import PDFExtractor
from ..ai.budget_enhancer import BudgetEnhancer
from ..models.budget import Budget

router = APIRouter(prefix="/convert", tags=["convert"])

# Initialize services
bc3_parser = BC3Parser()
bc3_generator = BC3Generator()
pdf_generator = PDFGenerator()
pdf_extractor = PDFExtractor()
budget_enhancer = BudgetEnhancer()


@router.post("/bc3-to-pdf")
async def bc3_to_pdf(file: UploadFile = File(...), enhance: bool = False):
    """
    Convert BC3 file to PDF

    Args:
        file: BC3 file to convert
        enhance: Whether to enhance descriptions with AI

    Returns:
        PDF file
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

        # Enhance if requested
        if enhance:
            budget = budget_enhancer.enhance_descriptions(budget)

        # Generate PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_pdf:
            temp_pdf_path = temp_pdf.name

        pdf_generator.generate_file(budget, temp_pdf_path)

        # Clean up BC3 temp file
        os.unlink(temp_bc3_path)

        # Return PDF file
        return FileResponse(
            temp_pdf_path,
            media_type='application/pdf',
            filename=f"{Path(file.filename).stem}.pdf"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Conversion failed: {str(e)}")


@router.post("/pdf-to-bc3")
async def pdf_to_bc3(file: UploadFile = File(...), use_ai: bool = True):
    """
    Convert PDF file to BC3

    Args:
        file: PDF file to convert
        use_ai: Whether to use AI for extraction (recommended)

    Returns:
        BC3 file
    """
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File must be a PDF file")

    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_pdf:
            content = await file.read()
            temp_pdf.write(content)
            temp_pdf_path = temp_pdf.name

        # Extract budget from PDF
        budget = pdf_extractor.extract_from_file(temp_pdf_path)

        # Generate BC3
        with tempfile.NamedTemporaryFile(delete=False, suffix='.bc3') as temp_bc3:
            temp_bc3_path = temp_bc3.name

        bc3_generator.generate_file(budget, temp_bc3_path)

        # Clean up PDF temp file
        os.unlink(temp_pdf_path)

        # Return BC3 file
        return FileResponse(
            temp_bc3_path,
            media_type='application/octet-stream',
            filename=f"{Path(file.filename).stem}.bc3"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Conversion failed: {str(e)}")


@router.post("/bc3-to-json")
async def bc3_to_json(file: UploadFile = File(...)):
    """
    Convert BC3 file to JSON

    Args:
        file: BC3 file to convert

    Returns:
        JSON budget data
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

        # Clean up temp file
        os.unlink(temp_bc3_path)

        # Return JSON
        return budget.model_dump()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Parsing failed: {str(e)}")


@router.post("/pdf-to-json")
async def pdf_to_json(file: UploadFile = File(...)):
    """
    Convert PDF file to JSON

    Args:
        file: PDF file to convert

    Returns:
        JSON budget data
    """
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File must be a PDF file")

    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_pdf:
            content = await file.read()
            temp_pdf.write(content)
            temp_pdf_path = temp_pdf.name

        # Extract budget from PDF
        budget = pdf_extractor.extract_from_file(temp_pdf_path)

        # Clean up temp file
        os.unlink(temp_pdf_path)

        # Return JSON
        return budget.model_dump()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")


@router.post("/json-to-bc3")
async def json_to_bc3(budget_data: Budget):
    """
    Convert JSON budget data to BC3 file

    Args:
        budget_data: Budget object as JSON

    Returns:
        BC3 file
    """
    try:
        # Generate BC3
        with tempfile.NamedTemporaryFile(delete=False, suffix='.bc3') as temp_bc3:
            temp_bc3_path = temp_bc3.name

        bc3_generator.generate_file(budget_data, temp_bc3_path)

        # Return BC3 file
        return FileResponse(
            temp_bc3_path,
            media_type='application/octet-stream',
            filename="presupuesto.bc3"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")


@router.post("/json-to-pdf")
async def json_to_pdf(budget_data: Budget):
    """
    Convert JSON budget data to PDF file

    Args:
        budget_data: Budget object as JSON

    Returns:
        PDF file
    """
    try:
        # Generate PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_pdf:
            temp_pdf_path = temp_pdf.name

        pdf_generator.generate_file(budget_data, temp_pdf_path)

        # Return PDF file
        return FileResponse(
            temp_pdf_path,
            media_type='application/pdf',
            filename="presupuesto.pdf"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")
