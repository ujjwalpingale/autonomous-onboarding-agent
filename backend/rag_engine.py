import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

DB_DIR = "../database/vectordb"

def init_rag_system():
    # Attempt to use local embeddings
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # If the database already exists, just load it
    if os.path.exists(DB_DIR) and os.listdir(DB_DIR):
        print("Loading existing ChromaDB...")
        vectorstore = Chroma(persist_directory=DB_DIR, embedding_function=embeddings)
        return vectorstore

    print("Initializing new ChromaDB from docs/...")
    loader = DirectoryLoader("../docs", glob="**/*.md", loader_cls=TextLoader)
    documents = loader.load()
    
    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = text_splitter.split_documents(documents)
    
    # Create VectorDB
    vectorstore = Chroma.from_documents(documents=docs, embedding=embeddings, persist_directory=DB_DIR)
    # The default behavior of Chroma in recent versions automatically persists to disk based on persist_directory
    
    return vectorstore

# Initialize on import
try:
    vector_db = init_rag_system()
    retriever = vector_db.as_retriever(search_kwargs={"k": 2})
except Exception as e:
    print(f"Failed to initialize RAG: {e}")
    retriever = None

def query_knowledge_base(query: str) -> str:
    """Queries the local chroma DB for relevant context."""
    if not retriever:
        return "Sorry, the knowledge base is currently offline."
    
    docs = retriever.invoke(query)
    if not docs:
        return "No relevant information found in the documentation."
        
    context = "\n\n".join([doc.page_content for doc in docs])
    return context
