import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_pinecone import PineconeVectorStore
from langchain_core.prompts import PromptTemplate
from langchain import hub
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_community.vectorstores import FAISS

load_dotenv()

if __name__ == '__main__':
    print("Ingesting...")
    loader = TextLoader("./resume.txt")
    document = loader.load()

    print("splitting...")
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
    texts = text_splitter.split_documents(document)
    print(f"created {len(texts)} chunks")

    embeddings = OllamaEmbeddings(model="znbang/bge:small-en-v1.5-q8_0")

    print("ingesting...")

    vectorstore = FAISS.from_documents(
                                        texts,
                                        embedding=embeddings,)


    vectorstore.save_local("faiss_index_react")

    print("done")