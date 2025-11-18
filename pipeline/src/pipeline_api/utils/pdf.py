from unstructured.partition.pdf import partition_pdf
from unstructured.staging.base import elements_to_json
from unstructured.documents.elements import Element
from typing import List

file_path = "/Users/ryanwilliams/Projects/RAG-pipeline/pipeline/src/pipeline_api/public"
base_file_name = "layout-parser-paper"

def parse_pdf() -> List[Element]:
    elements = partition_pdf(filename=f"{file_path}/{base_file_name}.pdf", strategy="hi_res", include_page_breaks=False)
    # elements_to_json(elements=elements, filename=f"{file_path}/{base_file_name}-output.json")
    return elements

if __name__ == "__main__":
    parse_pdf()