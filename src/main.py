from fastapi import FastAPI, HTTPException
from openai import APIError
from langchain.docstore.document import Document
 
from .schemas import IngestPayload, QueryPayload
from .rag_service import rag_service

app = FastAPI(title="RAG Chatbot Service")

@app.on_event("startup")
def startup_event():
    """Load the index on application startup."""
    rag_service.load_index()

@app.post("/ingest")
async def ingest(payload: IngestPayload):
    """Ingest texts and uploaded files into the vectorstore."""
    documents_to_process = []

    if not payload.texts and not payload.files:
        raise HTTPException(status_code=400, detail="No documents provided for ingestion")
    
    # Process raw texts if provided
    if payload.texts:
        for i, text in enumerate(payload.texts):
            doc = Document(page_content=text, metadata={"source": f"text_input_{i}"})
            documents_to_process.append(doc)

    # Process uploaded files if provided
    if payload.files:
        for file_data in payload.files:
            # Use the content directly from the payload instead of reading a file path
            doc = Document(
                page_content=file_data.content,
                metadata={"source": file_data.filename}
            )
            documents_to_process.append(doc)

    try:
        # The rag_service.ingest method now receives a list of LangChain Document objects
        num_chunks = rag_service.ingest_documents(documents_to_process)
        return {"message": "Ingestion successful", "chunks": num_chunks}
    except (APIError, ValueError) as e:
        # Catch potential errors from embedding (APIError) or empty docs (ValueError)
        raise HTTPException(status_code=500, detail=f"An error occurred during ingestion: {e}")


@app.post("/query")
async def query(payload: QueryPayload):
    """Query the RAG model."""
    try:
        answer = rag_service.query(payload.query)
        return {"answer": answer}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok", "index_exists": rag_service.vectorstore is not None}