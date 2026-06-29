from langchain_community.document_loaders import PyPDFLoader,DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

from typing import List
from langchain_classic.schema import Document


def load_pdf_file(data):
    loader=DirectoryLoader(data,glob="*.pdf",loader_cls=PyPDFLoader)

    documents=loader.load()
    return documents




def filter_to_minimal_docs(docs:List[Document])->List[Document]:
    """Given a list of Document objects, return a new list of a Document objects containing only 'source' in metadata and the original page_content"""
    minimal_docs:List[Document]=[]
    for doc in docs:
        src=doc.metadata.get("source")
        minimal_docs.append(
            Document(
                page_content=doc.page_content,
                metadata={"source":src}
            )
        )

    return minimal_docs


def text_split(minimal_docs):
    text_splitter=RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=30)
    text_chunk=text_splitter.split_documents(minimal_docs)
    return text_chunk

from langchain_huggingface import HuggingFaceEmbeddings

def download_hugging_face_embeddings():
    model_name = "all-MiniLM-L6-V2"

    embeddings = HuggingFaceEmbeddings(
        model_name=model_name,
    )

    return embeddings  