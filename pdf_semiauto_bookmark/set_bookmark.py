import pymupdf
from .parse_bookmark import parse_markdown


def set_bookmark(file_path):
    target_path = file_path.with_suffix(".pdf")
    target_pdf = pymupdf.open(target_path)
    bookmark = parse_markdown(file_path)
    target_pdf.set_toc(bookmark)
    target_pdf.save(file_path.stem + "_with_bookmark.pdf")
