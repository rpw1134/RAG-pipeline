from .clients import openai_client
from ..types.embeddings import RerankerResponse
from .constants import SYSTEM_PROMPT_BASE, SUPPORTED_MODELS
from typing import List
import json
from fastapi import HTTPException, status


def send_chat_request(query: str, context: RerankerResponse, include_metadatas: bool, model: str = "gpt-4") -> List[str | float]:
    """
    Send a chat request to an LLM with retrieved context documents.

    Args:
        query: The user's query to answer.
        context: RerankerResponse containing ranked documents and scores.
        include_metadatas: Whether to include document metadata in the prompt.
        model: The LLM model to use (default: "gpt-4").

    Returns:
        A list containing [response_text, confidence_score].

    Raises:
        HTTPException: If query is empty, no context provided, model unsupported,
                       or API error occurs.
    """
    if not query or not query.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No query provided")
    if not context.documents:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No context documents provided")
    if model not in SUPPORTED_MODELS:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unsupported model: {model}. Supported models: {SUPPORTED_MODELS}")

    context_strs: List[str] = []
    if include_metadatas:
        context_strs = construct_context_strings_with_metadatas(context)
    else:
        context_strs = construct_context_strings_without_metadatas(context)

    messages = []
    messages.append({"role": "system", "content": SYSTEM_PROMPT_BASE})
    messages.append({"role": "user", "content": "Here are the relevant documents:\n" + "\n".join(context_strs) + "\n\nQuery: " + query})

    try:
        response = openai_client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,
            max_tokens=1000
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=f"OpenAI API error: {str(e)}")

    if not response.choices or not response.choices[0].message.content:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="No content in chat completion response")

    res = response.choices[0].message.content
    confidence_score = res.split("Confidence Score:")[-1].strip().split("\n")[0].strip()
    res = res.split("Confidence Score:")[0].strip()
    try:
        score_value = float(confidence_score)
    except ValueError:
        score_value = -1.0
    return [res, score_value]


def construct_context_strings_with_metadatas(context: RerankerResponse) -> List[str]:
    """
    Format context documents with their metadata for LLM prompts.

    Args:
        context: RerankerResponse containing documents and relevance scores.

    Returns:
        List of formatted strings with document content, score, and metadata.
    """
    context_strs: List[str] = []
    for doc, score in zip(context.documents, context.scores):
        metadata_str: str = json.dumps(doc[1])
        context_strs.append(f"Document: {doc[0]}\nEstimated Relevance Score: {score:.4f}\nMetadata: {metadata_str}\n")
    return context_strs

def construct_context_strings_without_metadatas(context: RerankerResponse) -> List[str]:
    """
    Format context documents without metadata for LLM prompts.

    Args:
        context: RerankerResponse containing documents and relevance scores.

    Returns:
        List of formatted strings with document content and score only.
    """
    context_strs: List[str] = []
    for doc, score in zip(context.documents, context.scores):
        context_strs.append(f"Document: {doc[0]}\nRelevance Score: {score:.4f}\n")
    return context_strs

def generate_synthetic_query_prompt(num_documents: int) -> str:
    """
    Generate a prompt for synthetic query generation based on provided documents.

    Args:
        documents: List of document strings.
        """
    return f"You will be provided a number of documents. You will then generate 2 queries per document that should return the given document as part of a semantic search. For example, a document outlining how to cook steak should be returned for questions like: ['How do I prepare a steak dinner?', 'What are some good recipes for cooking steak?']. Your response must include exactly 2 queries per document in a JSON array format. For example, if num_documents==2: [['query1 for doc1', 'query2 for doc1'], ['query1 for doc2', 'query2 for doc2']]. You must ensure that the number of query groups matches the number of documents given to you. That is, len(response) == {num_documents} and len(res)==2 for res in response. It is IMPERATIVE that the length of the list you return is the same length as the documents I provide to you; that is, you generate a list of length {num_documents} where each entry is of length 2. Here are the documents:"