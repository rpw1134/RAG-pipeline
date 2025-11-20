from unstructured.partition.pdf import partition_pdf
from unstructured.documents.elements import Element
from typing import BinaryIO as File
from typing import List


def parse_pdf(file: File) -> List[Element]:
    """
    Parse a PDF file and return a list of Element objects.
    Each element includes type, text, metadata, and other attributes.
    """
    elements = partition_pdf(file=file, strategy="hi_res", include_page_breaks=False)
    return elements
