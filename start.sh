#!/bin/bash

# Start the FastAPI backend in the background
echo "Starting FastAPI server..."
uvicorn src.rag_chatbot.main:app --host 0.0.0.0 --port 8000 &

# Start the Streamlit frontend in the foreground
echo "Starting Streamlit UI..."
streamlit run src/rag_chatbot/ui.py --server.port 8501 --server.address 0.0.0.0
