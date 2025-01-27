from fastapi.testclient import TestClient
from app.main import app
from pathlib import Path
import pytest
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

client = TestClient(app)

@pytest.fixture
def sample_pdf(tmp_path):
    sample_pdf_path = tmp_path / "sample.pdf"
    # Używamy pypdf do tworzenia przykładowego pliku PDF
    from pypdf import PdfWriter
    writer = PdfWriter()
    for _ in range(12):
        writer.add_blank_page(width=100, height=100)
    with open(sample_pdf_path, "wb") as f:
        writer.write(f)
    return sample_pdf_path

def test_upload_pdf(sample_pdf):
    with open(sample_pdf, "rb") as f:
        response = client.post("/recipes/upload", files={"file": ("sample.pdf", f, "application/pdf")})
    
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "PDF processed successfully"
    assert len(data["parts"]) == 2

def test_upload_non_pdf():
    response = client.post("/recipes/upload", files={"file": ("test.txt", b"Sample text", "text/plain")})
    
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Only PDF files are accepted."
