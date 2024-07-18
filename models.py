import os
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFaceEndpoint
from dotenv import load_dotenv

load_dotenv()


def llm():
    mistral_model = "mistralai/Mistral-7B-Instruct-v0.2"

    llm = HuggingFaceEndpoint(repo_id=mistral_model,
                              temperature=0.7)
    return llm


def embeddings():
    return HuggingFaceEmbeddings()
