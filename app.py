import streamlit as st
import requests

FASTAPI_URL = "http://localhost:8000"

# UI Setup
st.set_page_config(page_title="RAG Chatbot", layout="wide")
st.title("RAG Chatbot")
st.markdown("Interact with your RAG service. ingest your document(s), then ask questions.")

# Health Check
st.sidebar.title("Service Status")
try:
    health_response = requests.get(f"{FASTAPI_URL}/health")
    if health_response.status_code == 200:
        health_status = health_response.json()
        st.sidebar.success(f"Status: **{health_status.get('status', 'N/A').upper()}**")
        st.sidebar.info(f"Index Exists: **{health_status.get('index_exists', 'N/A')}**")
    else:
        st.sidebar.error(f"Service Unreachable (Code: {health_response.status_code}). Is the backend running?")
except requests.exceptions.ConnectionError:
    st.sidebar.error("Service Unreachable. Is the backend running?")


# Ingestion Section
st.header("1. Ingest Knowledge")
with st.expander("Ingest new documents into the knowledge base"):
    ingest_texts_input = st.text_area("Enter raw text to ingest (one document per line)", height=150)
    uploaded_files = st.file_uploader(
        "Or upload documents directly",
        accept_multiple_files=True,
        help="The backend will process these in-memory."
    )

    if st.button("Ingest Documents"):
        payload = {}
        if ingest_texts_input:
            payload["texts"] = [text for text in ingest_texts_input.split('\n') if text.strip()]
        if uploaded_files:
            # The backend needs to be adapted to handle this payload format
            payload["files"] = [{"filename": f.name, "content": f.read().decode('utf-8', errors='ignore')} for f in uploaded_files]

        if not payload:
            st.warning("Please provide text or upload files to ingest.")
        else:
            with st.spinner("Ingesting documents..."):
                try:
                    response = requests.post(f"{FASTAPI_URL}/ingest", json=payload)
                    if response.status_code == 200:
                        st.success(f"Ingestion successful! Added {response.json().get('chunks', 0)} new chunks.")
                    else:
                        try:
                            # Try to parse the JSON error from FastAPI for a cleaner message
                            error_detail = response.json().get("detail", response.text)
                            st.error(f"Ingestion failed: {error_detail}")
                        except requests.exceptions.JSONDecodeError:
                            st.error(f"Ingestion failed with non-JSON response: {response.text}")
                except Exception as e:
                    st.error(f"An error occurred: {e}")

# Querying Section
st.header("2. Ask a Question")
query_text = st.text_input("Enter your question:", key="query_input")

if st.button("Get Answer", key="get_answer_btn"):
    if not query_text:
        st.warning("Please enter a question.")
    else:
        with st.spinner("Searching for an answer..."):
            try:
                response = requests.post(f"{FASTAPI_URL}/query", json={"query": query_text})
                if response.status_code == 200:
                    st.success("Answer:")
                    st.write(response.json().get("answer", "No answer found."))
                else:
                    try:
                        # Also apply the cleaner error handling here
                        error_detail = response.json().get("detail", response.text)
                        st.error(f"Query failed: {error_detail}")
                    except requests.exceptions.JSONDecodeError:
                        st.error(f"Query failed with non-JSON response: {response.text}")
            except Exception as e:
                st.error(f"An error occurred: {e}")