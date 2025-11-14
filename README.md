# RAG Chatbot with FastAPI and Streamlit

A powerful, document-aware chatbot built with Retrieval-Augmented Generation (RAG). This project uses a FastAPI backend for the core logic and a Streamlit frontend for a user-friendly interface.

 <!-- Replace with a real screenshot URL -->

## Overview

This application allows you to create a "smart" chatbot that answers questions based on a specific set of documents you provide. It leverages large language models (LLMs) from OpenAI but grounds their responses in your data, preventing hallucinations and ensuring factual accuracy based on the provided context.

## Key Features

-   **API-First Design:** A robust backend built with FastAPI, exposing endpoints for ingestion and querying.
-   **Flexible Ingestion:** Add knowledge from raw text or local text files.
-   **Interactive UI:** A simple and intuitive web interface created with Streamlit.
-   **Efficient Search:** Uses FAISS for fast and scalable similarity search over document embeddings.
-   **Powered by LangChain:** Orchestrates the entire RAG pipeline, from text splitting to final answer generation.

## Tech Stack

-   **Backend:** FastAPI
-   **Frontend:** Streamlit
-   **Orchestration:** LangChain
-   **LLM & Embeddings:** OpenAI
-   **Vector Store:** FAISS (Facebook AI Similarity Search)
-   **Dependencies:** Pydantic, Uvicorn, python-dotenv

## Project Structure

```
.
├── .env              # Local environment variables (DO NOT COMMIT)
├── .gitignore        # Files to be ignored by Git
├── config.py         # Handles configuration and environment variables
├── main.py           # FastAPI application, defines API routes
├── rag_service.py    # Core RAG logic (ingestion, querying)
├── requirements.txt  # Project dependencies
├── run.py            # Script to run the FastAPI backend
├── schemas.py        # Pydantic models for API request/response
└── ui.py             # Streamlit frontend application
```

## Getting Started

Follow these steps to get the project up and running on your local machine.

### 1. Prerequisites

-   Python 3.8+
-   An OpenAI API Key

### 2. Clone the Repository

```bash
git clone https://github.com/clusterloggs/rag_chatbot.git
cd rag_chatbot
```

### 3. Set Up Environment

Create and activate a virtual environment:

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file in the root directory by copying the example and add your new OpenAI API key:

```
OPENAI_API_KEY="your-new-openai-api-key-goes-here"
```

### 6. Run the Application

You need to run the backend and frontend in two separate terminals.

**Terminal 1: Run the FastAPI Backend**
```bash
python run.py
```

**Terminal 2: Run the Streamlit Frontend**
```bash
streamlit run ui.py
```

Your browser should automatically open to the Streamlit interface.

## Usage

1.  **Ingest Knowledge:** Use the "Ingest Knowledge" section to provide documents. You can either paste raw text or provide comma-separated local file paths.
2.  **Ask a Question:** Once documents are ingested, ask a question in the "Ask a Question" section to get an answer based on the provided context.

## API Endpoints

The FastAPI backend exposes the following endpoints:

-   `POST /ingest`: Ingests documents.
    -   **Body**: `{"texts": ["..."], "files": ["/path/to/file.txt"]}`
-   `POST /query`: Asks a question.
    -   **Body**: `{"query": "Your question here"}`
-   `GET /health`: Checks the service status.
-   `GET /docs`: Access interactive API documentation.