from pypdf import PdfReader, PdfWriter
from pathlib import Path
from typing import List

class PDFStorage:
    def __init__(self, storage_dir: Path):
        self.storage_dir = storage_dir
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def save_original_pdf(self, input_pdf: Path) -> Path:
        """
        Zapisuje oryginalny plik PDF w katalogu o nazwie pliku.
        """
        pdf_folder = self.storage_dir / input_pdf.stem
        pdf_folder.mkdir(parents=True, exist_ok=True)

        original_path = pdf_folder / input_pdf.name
        input_pdf.rename(original_path)

        return original_path

    def save_pdf_as_text(self, input_pdf: Path) -> Path:
        """
        Konwertuje cały PDF na plik `.txt` (niezależnie od tego, czy jest oryginalny, czy podzielony).
        """
        reader = PdfReader(input_pdf)
        text_path = input_pdf.with_suffix(".txt")

        text_content = [page.extract_text() or "" for page in reader.pages]
        with text_path.open("w", encoding="utf-8") as text_file:
            text_file.write("\n".join(text_content))

        return text_path

    def save_split_pdfs(self, original_pdf_path: Path, page_ranges: List[List[int]]) -> List[Path]:
        """
        Zapisuje podzielone fragmenty PDF w katalogu `parts`.
        """
        reader = PdfReader(original_pdf_path)
        pdf_folder = original_pdf_path.parent
        parts_folder = pdf_folder / "parts"
        parts_folder.mkdir(parents=True, exist_ok=True)

        output_files = []

        for idx, pages in enumerate(page_ranges):
            writer = PdfWriter()
            for page_num in pages:
                writer.add_page(reader.pages[page_num])

            output_pdf_path = parts_folder / f"part_{idx + 1}.pdf"
            with output_pdf_path.open("wb") as output_file:
                writer.write(output_file)

            output_files.append(output_pdf_path)

        return output_files
