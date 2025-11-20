from unstructured.documents.elements import Element
from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain_core.documents.base import Document

def chunk_document(elements: List[Element], chunk_size: int = 1000, overlap: int = 200, chunking_strategy:str = "simple") -> List[Document]:
    chunks: List[Document] = []
    match chunking_strategy:
        case "simple":
            chunks = chunk_document_simply(elements, chunk_size, overlap)
        case "recursive":
            chunks = chunk_document_recursively(elements, chunk_size, overlap)
        case "semantic":
            chunks = chunk_document_semantically(elements, chunk_size, overlap)
        case _:
            raise ValueError(f"Unsupported chunking strategy: {chunking_strategy}")
    return chunks

def chunk_document_semantically(elements: List[Element], chunk_size: int = 1000, overlap: int = 200) -> List[Document]:
    sections: List[str] = group_related_elements(elements=elements)
    documents: List[Document] = []
    splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", " ", ""],
        chunk_size=chunk_size,
        chunk_overlap=overlap,
    )
    for i, section in enumerate(sections):
        if len(section.strip())<=chunk_size:
            doc = Document(page_content=section, metadata={"section": i, "total_sections": len(sections), "chunk_of_section": 0, "total_chunks_in_section": 1})
            documents.append(doc)
            continue
        chunks = splitter.split_text(section)
        num_chunks = len(chunks)
        for j, chunk in enumerate(chunks):
            doc = Document(page_content=chunk, metadata={"section": i, "total_sections": len(sections), "chunk_of_section": j+1, "total_chunks_in_section": num_chunks})
            documents.append(doc)
    
    return documents
        
def chunk_document_recursively(elements: List[Element], chunk_size: int = 1000, overlap: int = 200) -> List[Document]:
    document: str = "\n\n".join([str(element.text) for element in elements if element.text])
    splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", " ", ""],
        chunk_size=1000,
        chunk_overlap=200,
    )
    chunks = splitter.split_text(document)
    num_chunks = len(chunks)
    documents: List[Document] = []
    for i, chunk in enumerate(chunks):
        doc = Document(page_content=chunk, metadata={"chunk": i+1, "total_chunks": num_chunks})
        documents.append(doc)
    return documents

def chunk_document_simply(elements: List[Element], chunk_size: int = 1000, overlap: int = 200)  -> List[Document]:
    document: str = "\n\n".join([str(element.text) for element in elements if element.text])
    splitter = CharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
    )
    chunks = splitter.split_text(document)
    num_chunks = len(chunks)
    documents: List[Document] = []
    for i, chunk in enumerate(chunks):
        doc = Document(page_content=chunk, metadata={"chunk": i+1, "total_chunks": num_chunks})
        documents.append(doc)
    
    return documents


def group_related_elements(elements: List[Element]) -> List[str]:
    sections: List[str] = []
    i = 0
    while i<len(elements):
        element: Element = elements[i]
        type_of: str = element.category
        current = f"{element.text}\n\n" if element.text else ""
        i+=1
        if type_of in ["Title", "Header"]:
            while i<len(elements) and elements[i].category in ["NarrativeText", "ListItem", "Table"]:
                current += f"{elements[i].text}\n" if elements[i].text else ""
                i += 1
        elif type_of == "FigureCaption":
            while i<len(elements) and elements[i].category in ["Table", "ListItem"]:
                current += f"{elements[i].text}\n" if elements[i].text else ""
                i += 1
        elif type_of == "Table":
            while i<len(elements) and elements[i].category == "Table":
                current += f"{elements[i].text}\n" if elements[i].text else ""
                i += 1
        elif type_of == "ListItem":
            while i<len(elements) and elements[i].category == "ListItem":
                current += f"{elements[i].text}\n" if elements[i].text else ""
                i += 1
        if current:
            sections.append(current)
            current = ""
    return sections