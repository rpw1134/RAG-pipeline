from .clients import openai_client
from ..types.embeddings import RerankerResponse
from .constants import SYSTEM_PROMPT_BASE
from typing import List
import json

def send_chat_request(query: str, context: RerankerResponse, include_metadatas: bool, model: str = "gpt-4") -> str:
    context_strs: List[str] = []
    if include_metadatas:
        context_strs = construct_context_strings_with_metadatas(context)
    else:
        context_strs = construct_context_strings_without_metadatas(context)
        
    messages = []
    messages.append({"role": "system", "content": SYSTEM_PROMPT_BASE})
    messages.append({"role":"context","content": "Here are the relevant documents:\n" + "\n".join(context_strs)})
    messages.append({"role": "user", "content": query})
    
    response = openai_client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7,
        max_tokens=500
    )
    if not response.choices[0].message.content:
        raise ValueError("No content in chat completion response")
    
    return response.choices[0].message.content


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