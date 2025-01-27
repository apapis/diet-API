from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from pathlib import Path
from app.services.pdf_splitter import PDFSplitter

router = APIRouter()

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted.")

    # Ścieżki robocze
    input_pdf_path = Path(f"/tmp/{file.filename}")
    output_dir = Path(f"/tmp/{file.filename}_parts")

    # Zapisz plik tymczasowo
    with open(input_pdf_path, "wb") as f:
        f.write(await file.read())

    # Podziel plik PDF
    splitter = PDFSplitter(max_pages=10)
    try:
        parts = splitter.split(input_pdf_path, output_dir)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")

    return {"message": "PDF processed successfully", "parts": [str(part) for part in parts]}