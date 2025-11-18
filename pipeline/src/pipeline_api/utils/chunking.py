from unstructured.documents.elements import Element
from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain_core.documents.base import Document

def chunk_document_elements_semantically(elements: List[Element], chunk_size: int = 1000, overlap: int = 200) -> List[Document]:
    sections: List[str] = group_related_elements(elements=elements)
    documents: List[Document] = []
            
        
    
def chunk_document_recursively(elements: List[Element], chunk_size: int = 1000, overlap: int = 200) -> List[Document]:
    document: str = "\n\n".join([str(element.text) for element in elements if element.text])
    splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", " ", ""],
        chunk_size=1000,
        chunk_overlap=200,
    )
    chunks = splitter.split_text(document)
    num_chunks = len(chunks)
    print(f"Number of chunks created: {num_chunks}")
    documents: List[Document] = []
    for i, chunk in enumerate(chunks):
        doc = Document(page_content=chunk, metadata={"chunk": i, "total_chunks": num_chunks})
        documents.append(doc)
    return documents

def chunk_document_simply(elements: List[Element], chunk_size: int = 1000, overlap: int = 200)  -> List[Document]:
    document: str = "\n\n".join([str(element.text) for element in elements if element.text])
    splitter = CharacterTextSplitter(
        seperator="\n\n",
        chunk_size=chunk_size,
        chunk_overlap=overlap,
    )
    chunks = splitter.split_text(document)
    num_chunks = len(chunks)
    print(f"Number of chunks created: {num_chunks}")
    documents: List[Document] = []
    for i, chunk in enumerate(chunks):
        doc = Document(page_content=chunk, metadata={"chunk": i, "total_chunks": num_chunks})
        documents.append(doc)
    
    return documents


def group_related_elements(elements: List[Element]) -> List[str]:
    sections: List[str] = []
    i = 0
    while i<len(elements):
        element: Element = elements[i]
        type_of: str = element.category
        current = f"{element.text}\n\n" if element.text else ""
        if type_of in ["Title", "Header"]:
            while i<len(elements) and elements[i].category == "NarativeText":
                current += f"{elements[i].text}\n" if elements[i].text else ""
                i += 1
            sections.append(current)
            current = ""
        elif type_of == "FigureCaption":
            while i<len(elements) and elements[i].category in ["Table", "ListItem"]:
                current += f"{elements[i].text}\n" if elements[i].text else ""
                i += 1
        else:
            current += f"{element.text}\n" if element.text else ""
            i += 1
        if current:
            sections.append(current)
            current = ""
    return sections