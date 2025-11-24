import warnings
import logging

from unstructured.partition.pdf import partition_pdf
from unstructured.documents.elements import Element
from typing import BinaryIO as File
from typing import List
from fastapi import HTTPException, status

# Suppress pdfminer FontBBox warnings
warnings.filterwarnings("ignore", message=".*FontBBox.*")
logging.getLogger("pdfminer").setLevel(logging.ERROR)


def parse_pdf(file: File) -> List[Element]:
    """
    Parse a PDF file and return a list of Element objects.
    Each element includes type, text, metadata, and other attributes.
    """
    if file is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No file provided")

    try:
        elements = partition_pdf(file=file, strategy="hi_res", include_page_breaks=False)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Failed to parse PDF: {str(e)}")

    if not elements:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="No content could be extracted from PDF")

    return elements
