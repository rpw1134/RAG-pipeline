# RAG Pipeline

A comprehensive RAG (Retrieval-Augmented Generation) pipeline designed to explore the importance of document parsing, chunking strategies, and response validation. This project includes a FastAPI backend for processing documents and running diagnostics, plus a Next.js visualizer for analyzing results.

## Table of Contents

- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Backend Setup (Pipeline API)](#backend-setup-pipeline-api)
- [Frontend Setup (RAG Visualizer)](#frontend-setup-rag-visualizer)
- [Configuration](#configuration)
- [Understanding the Metrics](#understanding-the-metrics)
- [Usage Examples](#usage-examples)

---

## Quick Start

### Prerequisites

- Python 3.12+
- Node.js 20+
- Poetry (Python package manager)
- npm or yarn

### Installation & Running

```bash
# 1. Clone the repository
git clone https://github.com/rpw1134/RAG-pipeline.git
cd RAG-pipeline

# 2. Setup and start the backend
cd pipeline
poetry install
cp .env.sample .env
# Edit .env and add your OPENAI_API_KEY (if using OpenAI models)
poetry run dev

# 3. In a new terminal, setup and start the frontend
cd ../rag-visualizer
npm install
npm run dev
```

The API will be available at `http://localhost:8000` and the visualizer at `http://localhost:3000`.

---

## Project Structure

```
RAG-pipeline/
├── pipeline/              # FastAPI backend
│   ├── src/
│   │   └── pipeline_api/
│   │       ├── routers/   # API endpoints
│   │       ├── utils/     # Core utilities (chunking, embeddings, etc.)
│   │       └── schemas/   # Pydantic models
│   ├── pyproject.toml
│   └── .env.sample
└── rag-visualizer/        # Next.js frontend
    ├── app/               # Next.js app directory
    ├── components/        # React components
    └── package.json
```

---

## Backend Setup (Pipeline API)

### 1. Install Dependencies

Navigate to the `pipeline` directory and install dependencies using Poetry:

```bash
cd pipeline
poetry install
```

### 2. Configure Environment Variables

Copy the sample environment file and add your API keys:

```bash
cp .env.sample .env
```

Edit `.env` and add your OpenAI API key:

```dotenv
OPENAI_API_KEY=your_openai_api_key_here
```

**Note:** The OpenAI API key is only required if you want to:

- Use OpenAI embedding models (e.g., `text-embedding-3-small`)
- Use OpenAI LLM models (e.g., `gpt-4o`, `gpt-4`)
- Run synthetic query diagnostics (requires GPT-4 for query generation)

If you only use HuggingFace models, the API key is optional.

### 3. Run the Development Server

```bash
poetry run dev
```

The API will start on `http://localhost:8000`.

### Available Scripts

- `poetry run dev` - Start development server

---

## Frontend Setup (RAG Visualizer)

### 1. Install Dependencies

Navigate to the `rag-visualizer` directory and install dependencies:

```bash
cd rag-visualizer
npm install
```

### 2. Run the Development Server

```bash
npm run dev
```

The visualizer will be available at `http://localhost:3000`.

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm start` - Start production server
- `npm run lint` - Run linter

---

## Configuration

### Embedding Models

The pipeline supports multiple embedding models:

- **HuggingFace Models:**

  - `huggingface_small` - BGE small model (no API key needed)
  - `huggingface_base` - BGE base model (no API key needed)
  - `huggingface_large` - BGE large model (no API key needed)

- **OpenAI Models** (requires API key):
  - `openai_small` - text-embedding-3-small
  - `openai_large` - text-embedding-3-large

### Chunking Strategies

- **Recursive** - Splits text recursively by paragraphs, sentences, then characters
- **Semantic** - Groups semantically similar content together
- **Simple** - Splits by token count

### LLM Models

- **GPT-4o** - Latest OpenAI model (requires API key)
- **GPT-4** - Standard GPT-4 (requires API key)

---

## Understanding the Metrics

The pipeline provides comprehensive diagnostics to evaluate your RAG system's performance. Here's what each metric measures and how to use it:

### 📊 Chunk Diagnostics

#### **Chunk Length**

- **What it measures:** The character count of each text chunk
- **Why it matters:** Extreme lengths can indicate poor chunking and unreliable cohesion/separation scores
- **Ideal range:** 500-1500 characters
- **How to use it:**
  - Too small: May lack context for meaningful retrieval
  - Too large: May mix multiple topics, reducing precision
  - High variance: Indicates inconsistent chunking strategy

#### **Cohesion Score** (0.0 - 1.0)

- **What it measures:** How semantically similar sentences within a chunk are to each other using cosine similarity
- **Why it matters:** High cohesion means the chunk discusses a coherent topic
- **Ideal range:** 0.6-1.0
- **How to use it:**
  - **High (0.7-1.0):** Good - chunk covers a focused topic
  - **Medium (0.5-0.7):** Moderate - chunk may cover related but distinct concepts
  - **Low (<0.5):** Poor - chunk likely mixes unrelated topics
  - Use this to tune your chunking strategy for better topical coherence

#### **Separation Score** (0.0 - 1.0)

- **What it measures:** How semantically different consecutive chunks are from each other using cosine similarity
- **Why it matters:** Good separation prevents redundant chunks and ensures diversity
- **Ideal range:** 0.1-0.6
- **How to use it:**
  - **Low (0.1-0.4):** Good - chunks are distinct from each other
  - **Medium (0.4-0.6):** Moderate - some overlap between chunks
  - **High (>0.6):** Poor - chunks are too similar, likely redundant
  - Balance with cohesion: aim for high cohesion but low separation

### 🎯 Retrieval Quality Diagnostics (Synthetic Queries)

These metrics evaluate how well your retrieval system finds relevant documents:

#### **Hit Rate** (0.0 - 1.0)

- **What it measures:** Percentage of synthetic queries that successfully retrieved the expected document
- **Why it matters:** Directly measures retrieval accuracy
- **How to use it:**
  - **High (>0.8):** Excellent retrieval performance
  - **Medium (0.5-0.8):** Acceptable, but room for improvement
  - **Low (<0.5):** Poor retrieval, consider different embeddings or chunking
  - Compare across different embedding models and chunking strategies

#### **MRR (Mean Reciprocal Rank)** (0.0 - 1.0)

- **What it measures:** Average of 1/rank where rank is the position of the correct document
- **Why it matters:** Measures not just if you find the document, but how highly you rank it
- **How to use it:**
  - **High (>0.7):** Correct documents appear at top of results
  - **Medium (0.4-0.7):** Correct documents found but not prioritized
  - **Low (<0.4):** Correct documents buried in results
  - Important for user experience - users typically only check top results

#### **Redundancy Score** (0.0 - 1.0)

- **What it measures:** Average pairwise similarity between retrieved documents
- **Why it matters:** High redundancy means you're returning similar/duplicate information
- **How to use it:**
  - **Low (<0.5):** Good - diverse results covering different aspects
  - **Medium (0.5-0.7):** Moderate - some repeated information
  - **High (>0.7):** Poor - results are too similar, wasting context window. Note, this is not always a bad thing.
  - Use reranking or diversity-focused retrieval to reduce redundancy

### ⏱️ Timing Diagnostics

Track performance bottlenecks in your pipeline:

- **Parsing Time:** Time to extract text from documents (PDF, etc.)
- **Chunking Time:** Time to split documents into chunks
- **Embedding Time:** Time to generate vector embeddings
- **Add Time:** Time to store vectors in the database
- **Total Time:** Sum of all processing steps

---

## Usage Examples

### Running Diagnostics Mode

1. Open the visualizer at `http://localhost:3000`
2. Select **Diagnostics** mode
3. Upload a PDF document
4. Configure settings:
   - Choose embedding model
   - Select chunking strategy
   - Enable chunk diagnostics
   - Enable synthetic query diagnostics (requires OpenAI API key)
   - Configure reranking options
5. Click **Submit**
6. View results in the tabs:
   - **Timing:** Processing performance
   - **Chunk Diagnostics:** Cohesion and separation metrics
   - **Retrieval Quality:** Hit rate, MRR, and redundancy

### Running Query Mode

1. Switch to **Query** mode
2. Enter your question
3. Configure settings:
   - Choose embedding model (must match your uploaded collection)
   - Select LLM model
   - Set number of results to retrieve
   - Enable reranking if desired
4. Click **Submit**
5. View:
   - LLM-generated response
   - Confidence score
   - Retrieved context chunks with scores

---

## API Endpoints

### POST `/embeddings/documents`

Upload and process documents with diagnostics.

**Request (multipart/form-data):**

- `file`: PDF file
- `config`: JSON configuration object

### POST `/queries`

Submit a query and get AI-generated responses.

**Request (application/json):**

```json
{
  "query": "Your question here",
  "embedding_model": "huggingface_small",
  "llm_model": "gpt-4o",
  "rerank": true,
  "num_queries": 10,
  "num_results": 5
}
```

### GET `/collections`

List available vector collections and their metadata.

---

## Tips for Best Results

1. **Start with diagnostics:** Run chunk diagnostics first to ensure your chunking strategy produces high-quality chunks
2. **Compare strategies:** Test multiple embedding models and chunking strategies to find what works best for your documents
3. **Use reranking:** Enable reranking to improve result quality, especially when retrieving more candidates
4. **Monitor metrics:** Track cohesion, separation, hit rate, and MRR across experiments
5. **Balance trade-offs:** Consider speed vs. quality based on your use case

---

## Contributing

Contributions welcome! Please open an issue or submit a pull request.
