from unstructured.partition.pdf import partition_pdf
from unstructured.documents.elements import Element
from fastapi import UploadFile
from typing import List


def parse_pdf(file: UploadFile) -> List[Element]:
    elements = partition_pdf(file=file.file, strategy="hi_res", include_page_breaks=False)
    # elements_to_json(elements=elements, filename=f"{file_path}/{base_file_name}-output.json")
    return elements
