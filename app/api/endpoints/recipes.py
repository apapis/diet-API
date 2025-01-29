from fastapi import APIRouter, UploadFile, HTTPException
from app.services.pdf_splitter import PDFSplitter
from app.services.pdf_storage import PDFStorage
from pathlib import Path

router = APIRouter()

@router.post("/process")
async def process_pdf(file: UploadFile):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are accepted.")

    # 📌 **Ustawienie katalogu przechowywania PDF**
    storage_dir = Path("/tmp/pdf_storage")
    storage = PDFStorage(storage_dir)

    # 📌 **Zapisz przesłany plik tymczasowo**
    temp_pdf_path = Path(f"/tmp/{file.filename}")
    with temp_pdf_path.open("wb") as temp_file:
        temp_file.write(file.file.read())

    # 📌 **Zapisz oryginalny PDF**
    saved_pdf_path = storage.save_original_pdf(temp_pdf_path)

    # 📌 **Podziel PDF na zakresy stron**
    splitter = PDFSplitter(max_pages=10)
    page_ranges = splitter.split(saved_pdf_path)

    # 📌 **Zapisz podzielone pliki PDF**
    split_pdfs = storage.save_split_pdfs(saved_pdf_path, page_ranges)

    # 📌 **Konwertuj podzielone PDF-y na TXT**
    split_texts = [storage.save_pdf_as_text(pdf) for pdf in split_pdfs]

    return {
        "message": "PDF processed successfully",
        "original_pdf": str(saved_pdf_path),
        "split_pdfs": [str(f) for f in split_pdfs],
        "split_texts": [str(f) for f in split_texts],
    }
