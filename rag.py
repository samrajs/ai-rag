import os

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate

from langchain import hub
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings, ChatOllama

load_dotenv()


if __name__ == "__main__":
    print(" Retrieving...")

    embeddings = OllamaEmbeddings(model="znbang/bge:small-en-v1.5-q8_0")
    llm = ChatOllama(model="llama3.2", temperature=0)

    query = "when is Hayden Smith available?"

    vectorstore = FAISS.load_local("faiss_index_react", embeddings=embeddings, allow_dangerous_deserialization=True) 

    print("Loaded vector store")

    retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
    combine_docs_chain = create_stuff_documents_chain(llm, retrieval_qa_chat_prompt)
    retrival_chain = create_retrieval_chain(
        retriever=vectorstore.as_retriever(), combine_docs_chain=combine_docs_chain
    )

    result = retrival_chain.invoke(input={"input": query})

    print(result['answer'])
