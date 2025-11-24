from unstructured.documents.elements import Element
from typing import List, Tuple
from langchain_text_splitters import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain_core.documents.base import Document
from fastapi import HTTPException, status
from ..utils.clients import clients
import time

def chunk_document(elements: List[Element], chunk_size: int = 1000, overlap: int = 200, chunking_strategy: str = "simple") -> Tuple[List[Document], float]:
    """
    Chunk parsed document elements using the specified strategy.

    Args:
        elements: List of Element objects from document parsing.
        chunk_size: Maximum size of each chunk in characters.
        overlap: Number of overlapping characters between consecutive chunks.
        chunking_strategy: One of "simple", "recursive", or "structural".

    Returns:
        List of Document objects with page_content and metadata.

    Raises:
        HTTPException: If elements are empty, chunk_size/overlap are invalid,
                       or strategy is unsupported.
    """
    if not elements:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No elements provided for chunking")
    if chunk_size <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="chunk_size must be a positive integer")
    if overlap < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="overlap must be non-negative")
    if overlap >= chunk_size:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="overlap must be less than chunk_size")

    chunks: List[Document] = []
    start_time = time.time()
    match chunking_strategy:
        case "simple":
            chunks = chunk_document_simply(elements, chunk_size, overlap)
        case "recursive":
            chunks = chunk_document_recursively(elements, chunk_size, overlap)
        case "structural":
            chunks = chunk_document_by_structure(elements, chunk_size, overlap)
        case _:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unsupported chunking strategy: {chunking_strategy}")

    if not chunks:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="No chunks could be created from the provided elements")
    end_time = time.time()
    time_taken = end_time - start_time
    return chunks, time_taken
    

def chunk_document_by_structure(elements: List[Element], chunk_size: int = 1000, overlap: int = 200) -> List[Document]:
    """
    Chunk document by semantic structure, grouping related elements together.

    Groups elements by their type (headers with content, tables, lists) before
    applying recursive splitting. Preserves section boundaries where possible.

    Args:
        elements: List of Element objects from document parsing.
        chunk_size: Maximum size of each chunk in characters.
        overlap: Number of overlapping characters between consecutive chunks.

    Returns:
        List of Document objects with section and chunk metadata.
    """
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
    """
    Chunk document using recursive character splitting.

    Attempts to split on paragraph breaks first, then sentences, then words,
    preserving semantic coherence where possible.

    Args:
        elements: List of Element objects from document parsing.
        chunk_size: Maximum size of each chunk in characters.
        overlap: Number of overlapping characters between consecutive chunks.

    Returns:
        List of Document objects with chunk index metadata.
    """
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
    """
    Chunk document using simple character-based splitting.

    Splits text at fixed character intervals with overlap, without considering
    semantic boundaries.

    Args:
        elements: List of Element objects from document parsing.
        chunk_size: Maximum size of each chunk in characters.
        overlap: Number of overlapping characters between consecutive chunks.

    Returns:
        List of Document objects with chunk index metadata.
    """
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
    """
    Group semantically related elements into sections.

    Combines headers with their following content, groups consecutive list items,
    and keeps tables together.

    Args:
        elements: List of Element objects from document parsing.

    Returns:
        List of strings, each representing a logical section of the document.
    """
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