from PyPDF2 import PdfReader, PdfWriter
from pathlib import Path

class PDFSplitter:
    def __init__(self, max_pages: int = 10):
        self.max_pages = max_pages

    def split(self, input_pdf: Path, output_dir: Path) -> list[Path]:
        reader = PdfReader(input_pdf)
        total_pages = len(reader.pages)
        output_dir.mkdir(parents=True, exist_ok=True)

        output_files = []

        for i in range(0, total_pages, self.max_pages):
            writer = PdfWriter()
            part_pages = reader.pages[i:i + self.max_pages]

            for page in part_pages:
                writer.add_page(page)

            output_path = output_dir / f"part_{i // self.max_pages + 1}.pdf"
            with output_path.open("wb") as output_file:
                writer.write(output_file)

            output_files.append(output_path)

        return output_files
