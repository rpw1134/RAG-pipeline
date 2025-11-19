"""
Simple test script to manually verify embedding functions work properly.
Run this to test embedding small documents.
"""

import dotenv
dotenv.load_dotenv()

from langchain_core.documents.base import Document
from ..utils.embedding import embed_chunks, embed_openai, embed_hugging_face

print("Loaded environment variables from .env file")
def main():
    # Create two small test documents
    test_documents = [
        Document(
            page_content="The quick brown fox jumps over the lazy dog.",
            metadata={"source": "test1"}
        ),
        Document(
            page_content="Machine learning is a subset of artificial intelligence.",
            metadata={"source": "test2"}
        )
    ]

    print("=" * 60)
    print("Testing Embedding Functions")
    print("=" * 60)
    print(f"\nTest documents created: {len(test_documents)}")
    print("\nDocument 1:", test_documents[0].page_content)
    print("Document 2:", test_documents[1].page_content)

    # Test embed_chunks with OpenAI small model
    print("\n" + "=" * 60)
    print("Testing embed_chunks() with 'openai_small'")
    print("=" * 60)
    try:
        embeddings = embed_chunks(test_documents, embedding_model="openai_small")
        print(f"✅ Success! Generated {len(embeddings)} embeddings")
        if len(embeddings) > 0:
            print(f"   Embedding dimension: {len(embeddings[0])}")
            print(f"   First embedding (first 10 values): {embeddings[0][:10]}")
    except Exception as e:
        print(f"❌ Error: {e}")

    # Test embed_openai directly
    print("\n" + "=" * 60)
    print("Testing embed_openai() with 'text-embedding-3-small'")
    print("=" * 60)
    try:
        embeddings = embed_openai(test_documents, model="text-embedding-3-small")
        print(f"✅ Success! Generated {len(embeddings)} embeddings")
        if len(embeddings) > 0:
            print(f"   Embedding dimension: {len(embeddings[0])}")
            print(f"   First embedding (first 10 values): {embeddings[0][:10]}")
            print(f"   Second embedding (first 10 values): {embeddings[1][:10]}")
    except Exception as e:
        print(f"❌ Error: {e}")

    # Test with different model
    print("\n" + "=" * 60)
    print("Testing embed_openai() with 'text-embedding-3-large'")
    print("=" * 60)
    try:
        embeddings = embed_openai(test_documents, model="text-embedding-3-large")
        print(f"✅ Success! Generated {len(embeddings)} embeddings")
        if len(embeddings) > 0:
            print(f"   Embedding dimension: {len(embeddings[0])}")
            print(f"   First embedding (first 10 values): {embeddings[0][:10]}")
    except Exception as e:
        print(f"❌ Error: {e}")

    # Test HuggingFace Small Model
    print("\n" + "=" * 60)
    print("Testing embed_chunks() with 'small_hugging_face'")
    print("=" * 60)
    try:
        embeddings = embed_chunks(test_documents, embedding_model="small_hugging_face")
        print(f"✅ Success! Generated {len(embeddings)} embeddings")
        if len(embeddings) > 0:
            print(f"   Model: BAAI/bge-small-en-v1.5")
            print(f"   Embedding dimension: {len(embeddings[0])}")
            print(f"   First embedding (first 10 values): {embeddings[0][:10]}")
    except Exception as e:
        print(f"❌ Error: {e}")

    # Test HuggingFace Base Model
    print("\n" + "=" * 60)
    print("Testing embed_chunks() with 'base_hugging_face'")
    print("=" * 60)
    try:
        embeddings = embed_chunks(test_documents, embedding_model="base_hugging_face")
        print(f"✅ Success! Generated {len(embeddings)} embeddings")
        if len(embeddings) > 0:
            print(f"   Model: BAAI/bge-base-en-v1.5")
            print(f"   Embedding dimension: {len(embeddings[0])}")
            print(f"   First embedding (first 10 values): {embeddings[0][:10]}")
    except Exception as e:
        print(f"❌ Error: {e}")

    # Test HuggingFace Large Model
    print("\n" + "=" * 60)
    print("Testing embed_chunks() with 'large_hugging_face'")
    print("=" * 60)
    try:
        embeddings = embed_chunks(test_documents, embedding_model="large_hugging_face")
        print(f"✅ Success! Generated {len(embeddings)} embeddings")
        if len(embeddings) > 0:
            print(f"   Model: BAAI/bge-large-en-v1.5")
            print(f"   Embedding dimension: {len(embeddings[0])}")
            print(f"   First embedding (first 10 values): {embeddings[0][:10]}")
    except Exception as e:
        print(f"❌ Error: {e}")

    # Test HuggingFace function directly
    print("\n" + "=" * 60)
    print("Testing embed_hugging_face() directly with 'small_hugging_face'")
    print("=" * 60)
    try:
        embeddings = embed_hugging_face(test_documents, model="small_hugging_face")
        print(f"✅ Success! Generated {len(embeddings)} embeddings")
        if len(embeddings) > 0:
            print(f"   Embedding dimension: {len(embeddings[0])}")
            print(f"   First embedding (first 10 values): {embeddings[0][:10]}")
            print(f"   Second embedding (first 10 values): {embeddings[1][:10]}")
    except Exception as e:
        print(f"❌ Error: {e}")

    print("\n" + "=" * 60)
    print("Testing complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
