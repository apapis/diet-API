from pypdf import PdfReader
from pathlib import Path
from typing import List

class PDFSplitter:
    def __init__(self, max_pages: int = 10):
        self.max_pages = max_pages

    def split(self, input_pdf: Path) -> List[List[int]]:
        reader = PdfReader(input_pdf)
        total_pages = len(reader.pages)

        page_ranges = [list(range(i, min(i + self.max_pages, total_pages))) for i in range(0, total_pages, self.max_pages)]
        return page_ranges
