from .clients import openai_client
from ..types.embeddings import RerankerResponse
from .constants import SYSTEM_PROMPT_BASE, SUPPORTED_MODELS
from typing import List
import json
from fastapi import HTTPException, status


def send_chat_request(query: str, context: RerankerResponse, include_metadatas: bool, model: str = "gpt-4") -> List[str | float]:
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
    context_strs: List[str] = []
    for doc, score in zip(context.documents, context.scores):
        metadata_str: str = json.dumps(doc[1])
        context_strs.append(f"Document: {doc[0]}\nEstimated Relevance Score: {score:.4f}\nMetadata: {metadata_str}\n")
    return context_strs

def construct_context_strings_without_metadatas(context: RerankerResponse) -> List[str]:
    context_strs: List[str] = []
    for doc, score in zip(context.documents, context.scores):
        context_strs.append(f"Document: {doc[0]}\nRelevance Score: {score:.4f}\n")
    return context_strs