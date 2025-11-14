import os
from typing import List

from langchain.chains import RetrievalQA
from langchain.docstore.document import Document
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.llms import OpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

from src import config


class RAGService:
    def __init__(self):
        self.vectorstore = None
        self.qa_chain = None
        self.embeddings = OpenAIEmbeddings(openai_api_key=config.OPENAI_API_KEY)
        self.llm = OpenAI(temperature=0, openai_api_key=config.OPENAI_API_KEY)
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    def load_index(self):
        """Loads an existing FAISS index from disk."""
        try:
            if os.path.exists(config.INDEX_PATH):
                self.vectorstore = FAISS.load_local(config.INDEX_PATH, self.embeddings, allow_dangerous_deserialization=True)
                self.qa_chain = RetrievalQA.from_chain_type(
                    llm=self.llm,
                    chain_type="stuff",
                    retriever=self.vectorstore.as_retriever(search_kwargs={"k": 4})
                )
                print("Loaded existing FAISS index.")
            else:
                print("No existing index found. Create one via /ingest.")
        except Exception as e:
            print(f"Failed to load index: {e}")
            self.vectorstore = None
            self.qa_chain = None

    def ingest_documents(self, documents: List[Document]) -> int:
        """
        Ingests a list of LangChain Document objects into the FAISS vectorstore.
        This involves splitting, embedding, and storing them.
        """
        if not documents:
            raise ValueError("No documents provided for ingestion")

        chunks = self.text_splitter.split_documents(documents)

        if self.vectorstore is None:
            self.vectorstore = FAISS.from_documents(chunks, self.embeddings)
        else:
            self.vectorstore.add_documents(chunks)

        self.vectorstore.save_local(config.INDEX_PATH)
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(search_kwargs={"k": 4})
        )
        return len(chunks)

    def query(self, query: str) -> str:
        """Performs a query against the QA chain."""
        if self.qa_chain is None:
            raise ValueError("No index available. Please ingest documents first.")
        return self.qa_chain.run(query)

rag_service = RAGService()