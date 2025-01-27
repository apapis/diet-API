import pytest
from pathlib import Path
from app.services.pdf_splitter import PDFSplitter
from pypdf import PdfReader, PdfWriter
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

@pytest.fixture
def sample_pdf(tmp_path):
    # Tworzymy przykładowy plik PDF z 15 stronami
    sample_pdf_path = tmp_path / "sample.pdf"
    writer = PdfWriter()
    for _ in range(15):
        writer.add_blank_page(width=100, height=100)
    with open(sample_pdf_path, "wb") as f:
        writer.write(f)
    return sample_pdf_path

def test_split_into_parts(tmp_path, sample_pdf):
    output_dir = tmp_path / "output"
    splitter = PDFSplitter(max_pages=10)
    parts = splitter.split(sample_pdf, output_dir)

    # Sprawdzamy, czy plik został podzielony na 2 części
    assert len(parts) == 2
    assert parts[0].exists()
    assert parts[1].exists()

def test_split_less_than_max_pages(tmp_path):
    # Plik PDF z 5 stronami
    sample_pdf_path = tmp_path / "small_sample.pdf"
    writer = PdfWriter()
    for _ in range(5):
        writer.add_blank_page(width=100, height=100)
    with open(sample_pdf_path, "wb") as f:
        writer.write(f)

    output_dir = tmp_path / "output"
    splitter = PDFSplitter(max_pages=10)
    parts = splitter.split(sample_pdf_path, output_dir)

    # Sprawdzamy, czy powstał tylko jeden plik
    assert len(parts) == 1
    assert parts[0].exists()

def test_split_empty_pdf(tmp_path):
    # Pusty plik PDF
    empty_pdf_path = tmp_path / "empty.pdf"
    writer = PdfWriter()
    with open(empty_pdf_path, "wb") as f:
        writer.write(f)

    output_dir = tmp_path / "output"
    splitter = PDFSplitter(max_pages=10)
    parts = splitter.split(empty_pdf_path, output_dir)

    # Sprawdzamy, czy nie powstały żadne części
    assert len(parts) == 0
