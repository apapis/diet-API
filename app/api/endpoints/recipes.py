from fastapi import APIRouter, UploadFile, HTTPException, Depends
from sqlalchemy.orm import Session
from pathlib import Path
from app.db.session import SessionLocal
from app.services.pdf_splitter import PDFSplitter
from app.services.pdf_storage import PDFStorage
from app.services.openai_service import process_pdf_parts_with_gpt
from app.db.db_utils import save_meals_to_db

router = APIRouter()

def get_db():
    """Generator sesji bazy danych dla FastAPI"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/process")
async def process_pdf(file: UploadFile, db: Session = Depends(get_db)):
    """Przetwarza PDF, wysyła do OpenAI, a następnie zapisuje wyniki w bazie."""
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

    # Przetwórz pierwszy fragment PDF
    first_text_path = storage.save_pdf_as_text(split_pdfs[0])
    extracted_recipes = process_pdf_parts_with_gpt([first_text_path.read_text()])

    # Zapisz przepisy do bazy
    saved_meals = save_meals_to_db(db, extracted_recipes)

    return {
        "message": "PDF processed successfully",
        "original_pdf": str(saved_pdf_path),
        "processed_meals": [meal.id for meal in saved_meals]  # Zwracamy ID zapisanych posiłków
    }
