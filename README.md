# RAG Chatbot

A powerful, document-aware chatbot built with Retrieval-Augmented Generation (RAG). This project features a robust FastAPI backend for the core logic and an intuitive Streamlit frontend for user interaction, all containerized with Docker for easy deployment and setup.

![RAG Chatbot Screenshot](./assets/screenshot.png)

This application allows you to create a "smart" chatbot that answers questions based on a specific set of documents you provide. It leverages large language models (LLMs) from OpenAI but grounds their responses in your data, preventing hallucinations and ensuring factual accuracy based on the provided context. The vector index is automatically saved to and loaded from the `faiss_index/` directory, providing persistence across sessions.

### Key Features

-   **API-First Design:** A robust backend built with FastAPI, exposing endpoints for ingestion, querying, and health checks.
-   **Flexible Ingestion:** Add knowledge from raw text or by uploading multiple files directly through the UI.
-   **Interactive UI:** A simple and intuitive web interface created with Streamlit that communicates with the backend.
-   **Persistent Vector Store:** Uses FAISS to create and save a searchable index of document embeddings, which is automatically loaded on startup.
-   **Powered by LangChain:** Orchestrates the entire RAG pipeline, from text splitting and embedding to final answer generation.
-   **Containerized:** Fully containerized with Docker for consistent, one-command setup and deployment.

## Project Structure

The project follows a modern `src` layout to separate source code from project configuration.

```
.
├── .env              # Stores secret keys (e.g., OpenAI API key)
├── .gitignore        # Specifies files for Git to ignore
├── Dockerfile        # Defines the Docker container for the application
├── README.md         # This file
├── requirements.txt  # Python dependencies
├── start.sh          # Startup script for running services inside Docker
└── src/
    └── rag_chatbot/
        ├── __init__.py      # Makes 'rag_chatbot' a Python package
        ├── config.py        # Handles configuration from environment variables
        ├── main.py          # FastAPI application: defines API routes
        ├── rag_service.py   # Core RAG logic (ingestion, querying, FAISS)
        ├── schemas.py       # Pydantic models for API request/response validation
        └── ui.py            # Streamlit frontend application
```

## Installation & Setup

The recommended way to run this project is with Docker, which handles all dependencies and setup in a clean, isolated environment.

### Prerequisites

-   Docker
-   An OpenAI API Key

### 1. Configure Environment Variables

Create a file named `.env` in the project's root directory. This file will securely store your OpenAI API key.

```ini
# .env
OPENAI_API_KEY="sk-..."
```

### 2. Build and Run with Docker

Open a terminal in the project's root directory and run the following commands.

**Build the Docker image:**
This command packages the application and its dependencies into an image named `rag-chatbot`.
```bash
docker build -t rag-chatbot .
```

**Run the Docker container:**
This command starts the application. It maps the required ports and securely passes your API key from the `.env` file to the container.
```bash
docker run -p 8000:8000 -p 8501:8501 --env-file .env rag-chatbot
```

### 3. Access the Application

Once the container is running, you can access the services:

-   **Streamlit UI**: http://localhost:8501
-   **FastAPI Docs**: http://localhost:8000/docs

## Usage Guide

1.  **Navigate to the UI:** Open your web browser to http://localhost:8501.
2.  **Ingest Knowledge:** In the "Ingest Knowledge" section, either paste raw text into the text area or use the file uploader to add one or more documents. Click "Ingest Documents".
3.  **Ask a Question:** Once the documents are ingested and the index is ready, type your question into the "Ask a Question" input field and click "Get Answer". The model will respond based on the context of the documents you provided.

## Local Development (Without Docker)

If you prefer to run the services manually for development, we recommend using `uv` for a fast and efficient setup.

### 1. Set Up Python Environment with `uv`

First, install `uv` (a fast Python package installer from Astral):
```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Then, create the virtual environment and install dependencies:
```bash
# Create and activate the virtual environment (.venv is the default)
uv venv
source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`

# Install dependencies using uv
uv pip install -r requirements.txt
```

### 2. Run the Application

You will need two separate terminal windows, with the virtual environment activated in each.

**Terminal 1: Run the FastAPI Backend**
The `--reload` flag enables hot-reloading for development.
```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2: Run the Streamlit Frontend**
```bash
streamlit run app.py
```

## API Documentation

The FastAPI backend provides the following endpoints. You can interact with them via the auto-generated documentation at http://localhost:8000/docs.

### `POST /ingest`

Ingests documents from raw text or file content.

**Request Body:**
```json
{
  "texts": [
    "This is the first document."
  ],
  "files": [
    {
      "filename": "example.txt",
      "content": "This is the content of the uploaded file."
    }
  ]
}
```

**Example `curl`:**
```bash
curl -X POST "http://localhost:8000/ingest" \
-H "Content-Type: application/json" \
-d '{"texts": ["The sky is blue."], "files": []}'
```

### `POST /query`

Asks a question to the RAG model.

**Request Body:**
```json
{
  "query": "What color is the sky?"
}
```

**Example `curl`:**
```bash
curl -X POST "http://localhost:8000/query" \
-H "Content-Type: application/json" \
-d '{"query": "What color is the sky?"}'
```

### `GET /health`

Checks the service status and whether a FAISS index has been loaded.

**Example `curl`:**
```bash
curl -X GET "http://localhost:8000/health"
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.
