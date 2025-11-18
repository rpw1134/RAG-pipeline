from fastapi import FastAPI
from .utils.pdf import parse_pdf
from .utils.chunking import chunk_document_elements_semantically, chunk_document_recursively, chunk_document_simply


app = FastAPI()

def main():
    elements = parse_pdf()
    print(f"Total elements parsed from PDF: {len(elements)}")
    
    semantic_chunks = chunk_document_elements_semantically(elements)
    print(f"Semantic:")
    print(semantic_chunks[0])
    
    recursive_chunks = chunk_document_recursively(elements)
    print(f"Recursive:")
    print(recursive_chunks[0])
    
    simple_chunks = chunk_document_simply(elements)
    print(f"Simple:")
    print(simple_chunks[0])
    
if __name__ == "__main__":
    main()