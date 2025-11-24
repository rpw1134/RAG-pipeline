import warnings
import logging
import time 

from unstructured.partition.pdf import partition_pdf
from unstructured.documents.elements import Element
from typing import BinaryIO as File
from typing import List, Tuple
from fastapi import HTTPException, status

# Suppress pdfminer FontBBox warnings
warnings.filterwarnings("ignore", message=".*FontBBox.*")
logging.getLogger("pdfminer").setLevel(logging.ERROR)


def parse_pdf(file: File) -> Tuple[List[Element], float]:
    """
    Parse a PDF file and return a list of Element objects.
    Each element includes type, text, metadata, and other attributes.
    """
    if file is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No file provided")
    try:
        start_time = time.time()
        elements = partition_pdf(file=file, strategy="hi_res", include_page_breaks=False)
        end_time = time.time()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Failed to parse PDF: {str(e)}")

    if not elements:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="No content could be extracted from PDF")
    if not start_time or not end_time:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to measure parsing time")
    time_taken = end_time - start_time
    return elements, time_taken
