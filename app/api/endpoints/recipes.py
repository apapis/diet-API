from fastapi import APIRouter, UploadFile, HTTPException
from pathlib import Path
from app.services.pdf_splitter import PDFSplitter
from app.services.pdf_storage import PDFStorage
from app.services.openai_service import process_pdf_parts_with_gpt

router = APIRouter()

@router.post("/process")
async def process_pdf(
    file: UploadFile,
):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are accepted.")

    storage_dir = Path("/tmp/pdf_storage")
    storage = PDFStorage(storage_dir)

    # Zapisz oryginalny PDF
    temp_pdf_path = Path(f"/tmp/{file.filename}")
    with temp_pdf_path.open("wb") as temp_file:
        temp_file.write(file.file.read())

    saved_pdf_path = storage.save_original_pdf(temp_pdf_path)

    # Podziel PDF na części
    splitter = PDFSplitter(max_pages=5)
    page_ranges = splitter.split(saved_pdf_path)
    split_pdfs = storage.save_split_pdfs(saved_pdf_path, page_ranges)

    # Przetwórz pierwszy podzielony PDF na tekst
    if not split_pdfs:
        raise HTTPException(status_code=500, detail="Failed to split PDF into parts.")

    first_text_path = storage.save_pdf_as_text(split_pdfs[0])  # Tylko pierwszy fragment

    # Przetwórz tekst na JSON za pomocą OpenAI
    result = process_pdf_parts_with_gpt([first_text_path.read_text()])  # Tylko pierwszy fragment

    return {
        "message": "PDF processed successfully",
        "original_pdf": str(saved_pdf_path),
        "split_pdfs": [str(f) for f in split_pdfs],
        "split_text": str(first_text_path),
        "result": result
    }
