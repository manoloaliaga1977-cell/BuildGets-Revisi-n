"""
Conversion routes for budget formats - MEJORADO
Con mejor manejo de errores y limpieza de archivos temporales
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import tempfile
import os
from pathlib import Path
import traceback
import atexit
from typing import List

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

# Lista global para rastrear archivos temporales
temp_files: List[str] = []


def cleanup_temp_file(file_path: str):
    """Limpia un archivo temporal de forma segura"""
    try:
        if file_path and os.path.exists(file_path):
            os.unlink(file_path)
            print(f"🗑️  Archivo temporal eliminado: {file_path}")
            if file_path in temp_files:
                temp_files.remove(file_path)
    except Exception as e:
        print(f"⚠️  Error eliminando archivo temporal {file_path}: {e}")


def cleanup_all_temp_files():
    """Limpia todos los archivos temporales al cerrar"""
    print(f"🧹 Limpiando {len(temp_files)} archivos temporales...")
    for file_path in temp_files[:]:  # Crear copia para iterar
        cleanup_temp_file(file_path)


# Registrar limpieza al salir
atexit.register(cleanup_all_temp_files)


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
    temp_bc3_path = None
    temp_pdf_path = None

    try:
        print(f"📥 Recibiendo archivo: {file.filename} ({file.content_type})")

        # Validar extensión
        if not file.filename.lower().endswith('.bc3'):
            raise HTTPException(status_code=400, detail="El archivo debe ser .bc3")

        # Guardar archivo BC3 temporal
        with tempfile.NamedTemporaryFile(delete=False, suffix='.bc3', mode='wb') as temp_bc3:
            content = await file.read()
            temp_bc3.write(content)
            temp_bc3_path = temp_bc3.name
            temp_files.append(temp_bc3_path)

        print(f"💾 Archivo guardado en: {temp_bc3_path} ({len(content)} bytes)")

        # Parsear BC3
        print("🔍 Parseando BC3...")
        budget = bc3_parser.parse_file(temp_bc3_path)

        # Mejorar con IA si se solicita
        if enhance:
            print("✨ Mejorando con IA...")
            try:
                budget = budget_enhancer.enhance_descriptions(budget)
            except Exception as e:
                print(f"⚠️  Error en IA (continuando sin mejoras): {e}")

        # Generar PDF
        print("📄 Generando PDF...")
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf', mode='wb') as temp_pdf:
            temp_pdf_path = temp_pdf.name
            temp_files.append(temp_pdf_path)

        pdf_generator.generate_file(budget, temp_pdf_path)
        print(f"✅ PDF generado: {temp_pdf_path}")

        # Limpiar BC3 temporal
        cleanup_temp_file(temp_bc3_path)
        temp_bc3_path = None

        # Retornar PDF (se limpiará después de enviar)
        output_filename = f"{Path(file.filename).stem}.pdf"

        return FileResponse(
            temp_pdf_path,
            media_type='application/pdf',
            filename=output_filename,
            background=lambda: cleanup_temp_file(temp_pdf_path)
        )

    except HTTPException:
        raise
    except Exception as e:
        error_detail = f"Error al convertir BC3 a PDF: {str(e)}\n{traceback.format_exc()}"
        print(f"❌ {error_detail}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Asegurar limpieza si algo salió mal
        if temp_bc3_path:
            cleanup_temp_file(temp_bc3_path)


@router.post("/pdf-to-bc3")
async def pdf_to_bc3(file: UploadFile = File(...), use_ai: bool = True):
    """
    Convert PDF file to BC3

    Args:
        file: PDF file to convert
        use_ai: Whether to use AI for extraction

    Returns:
        BC3 file
    """
    temp_pdf_path = None
    temp_bc3_path = None

    try:
        print(f"📥 Recibiendo PDF: {file.filename}")

        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="El archivo debe ser .pdf")

        # Guardar PDF temporal
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf', mode='wb') as temp_pdf:
            content = await file.read()
            temp_pdf.write(content)
            temp_pdf_path = temp_pdf.name
            temp_files.append(temp_pdf_path)

        print(f"💾 PDF guardado: {temp_pdf_path}")

        # Extraer budget desde PDF
        print("🔍 Extrayendo presupuesto desde PDF...")
        budget = pdf_extractor.extract_from_file(temp_pdf_path)

        # Generar BC3
        print("📄 Generando BC3...")
        with tempfile.NamedTemporaryFile(delete=False, suffix='.bc3', mode='wb') as temp_bc3:
            temp_bc3_path = temp_bc3.name
            temp_files.append(temp_bc3_path)

        bc3_generator.generate_file(budget, temp_bc3_path)
        print(f"✅ BC3 generado: {temp_bc3_path}")

        # Limpiar PDF temporal
        cleanup_temp_file(temp_pdf_path)
        temp_pdf_path = None

        # Retornar BC3
        output_filename = f"{Path(file.filename).stem}.bc3"

        return FileResponse(
            temp_bc3_path,
            media_type='application/octet-stream',
            filename=output_filename,
            background=lambda: cleanup_temp_file(temp_bc3_path)
        )

    except HTTPException:
        raise
    except Exception as e:
        error_detail = f"Error al convertir PDF a BC3: {str(e)}\n{traceback.format_exc()}"
        print(f"❌ {error_detail}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if temp_pdf_path:
            cleanup_temp_file(temp_pdf_path)


@router.post("/bc3-to-json")
async def bc3_to_json(file: UploadFile = File(...)):
    """
    Convert BC3 file to JSON

    Args:
        file: BC3 file to convert

    Returns:
        JSON budget data
    """
    temp_bc3_path = None

    try:
        print(f"📥 Recibiendo BC3 para JSON: {file.filename}")

        if not file.filename.lower().endswith('.bc3'):
            raise HTTPException(status_code=400, detail="El archivo debe ser .bc3")

        # Guardar BC3 temporal
        with tempfile.NamedTemporaryFile(delete=False, suffix='.bc3', mode='wb') as temp_bc3:
            content = await file.read()
            temp_bc3.write(content)
            temp_bc3_path = temp_bc3.name
            temp_files.append(temp_bc3_path)

        print(f"💾 BC3 guardado: {temp_bc3_path}")

        # Parsear BC3
        print("🔍 Parseando BC3...")
        budget = bc3_parser.parse_file(temp_bc3_path)

        # Limpiar archivo temporal
        cleanup_temp_file(temp_bc3_path)
        temp_bc3_path = None

        # Retornar JSON
        print("✅ Retornando JSON")
        return budget.model_dump()

    except HTTPException:
        raise
    except Exception as e:
        error_detail = f"Error al convertir BC3 a JSON: {str(e)}\n{traceback.format_exc()}"
        print(f"❌ {error_detail}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if temp_bc3_path:
            cleanup_temp_file(temp_bc3_path)


@router.post("/pdf-to-json")
async def pdf_to_json(file: UploadFile = File(...)):
    """
    Convert PDF file to JSON

    Args:
        file: PDF file to convert

    Returns:
        JSON budget data
    """
    temp_pdf_path = None

    try:
        print(f"📥 Recibiendo PDF para JSON: {file.filename}")

        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="El archivo debe ser .pdf")

        # Guardar PDF temporal
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf', mode='wb') as temp_pdf:
            content = await file.read()
            temp_pdf.write(content)
            temp_pdf_path = temp_pdf.name
            temp_files.append(temp_pdf_path)

        print(f"💾 PDF guardado: {temp_pdf_path}")

        # Extraer budget
        print("🔍 Extrayendo presupuesto desde PDF...")
        budget = pdf_extractor.extract_from_file(temp_pdf_path)

        # Limpiar archivo temporal
        cleanup_temp_file(temp_pdf_path)
        temp_pdf_path = None

        # Retornar JSON
        print("✅ Retornando JSON")
        return budget.model_dump()

    except HTTPException:
        raise
    except Exception as e:
        error_detail = f"Error al convertir PDF a JSON: {str(e)}\n{traceback.format_exc()}"
        print(f"❌ {error_detail}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if temp_pdf_path:
            cleanup_temp_file(temp_pdf_path)


@router.post("/json-to-bc3")
async def json_to_bc3(budget_data: Budget):
    """
    Convert JSON budget data to BC3 file

    Args:
        budget_data: Budget object as JSON

    Returns:
        BC3 file
    """
    temp_bc3_path = None

    try:
        print("📥 Recibiendo JSON para BC3")

        # Generar BC3
        with tempfile.NamedTemporaryFile(delete=False, suffix='.bc3', mode='wb') as temp_bc3:
            temp_bc3_path = temp_bc3.name
            temp_files.append(temp_bc3_path)

        print("📄 Generando BC3...")
        bc3_generator.generate_file(budget_data, temp_bc3_path)
        print(f"✅ BC3 generado: {temp_bc3_path}")

        # Retornar BC3
        return FileResponse(
            temp_bc3_path,
            media_type='application/octet-stream',
            filename="presupuesto.bc3",
            background=lambda: cleanup_temp_file(temp_bc3_path)
        )

    except Exception as e:
        error_detail = f"Error al convertir JSON a BC3: {str(e)}\n{traceback.format_exc()}"
        print(f"❌ {error_detail}")
        if temp_bc3_path:
            cleanup_temp_file(temp_bc3_path)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/json-to-pdf")
async def json_to_pdf(budget_data: Budget):
    """
    Convert JSON budget data to PDF file

    Args:
        budget_data: Budget object as JSON

    Returns:
        PDF file
    """
    temp_pdf_path = None

    try:
        print("📥 Recibiendo JSON para PDF")

        # Generar PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf', mode='wb') as temp_pdf:
            temp_pdf_path = temp_pdf.name
            temp_files.append(temp_pdf_path)

        print("📄 Generando PDF...")
        pdf_generator.generate_file(budget_data, temp_pdf_path)
        print(f"✅ PDF generado: {temp_pdf_path}")

        # Retornar PDF
        return FileResponse(
            temp_pdf_path,
            media_type='application/pdf',
            filename="presupuesto.pdf",
            background=lambda: cleanup_temp_file(temp_pdf_path)
        )

    except Exception as e:
        error_detail = f"Error al convertir JSON a PDF: {str(e)}\n{traceback.format_exc()}"
        print(f"❌ {error_detail}")
        if temp_pdf_path:
            cleanup_temp_file(temp_pdf_path)
        raise HTTPException(status_code=500, detail=str(e))
