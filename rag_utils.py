from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.llms import Ollama
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import tempfile
import os


# -----------------------------
# Load PDF & split into chunks
# -----------------------------
def load_and_split_pdf(pdf_file):
    """Load and split PDF into chunks"""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(pdf_file.read())
        pdf_path = tmp.name

    try:
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100,
            length_function=len,
        )

        chunks = splitter.split_documents(documents)
        return chunks
    finally:
        if os.path.exists(pdf_path):
            os.remove(pdf_path)


# ------------------------------------
# Create FAISS with embeddings
# ------------------------------------
def create_vectorstore(chunks, gemini_api_key=None):
    """Create FAISS vector store from document chunks using local embeddings"""
    try:
        # Use local HuggingFace embeddings - much faster and no API limits!
        # Set cache folder to avoid issues
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={
                'normalize_embeddings': True,
                'batch_size': 32
            },
            cache_folder=os.path.join(os.path.expanduser('~'), '.cache', 'huggingface')
        )
        
        # Create vector store from all documents at once
        # Local embeddings are fast, no need for batching
        vectorstore = FAISS.from_documents(chunks, embeddings)
        
        return vectorstore
    
    except Exception as e:
        raise RuntimeError(f"Failed to create vector store: {str(e)}")


# -----------------------------
# Create RAG QA Chain
# -----------------------------
def create_qa_chain(vectorstore, api_key=None):
    """Create RAG QA chain with Ollama LLM (FREE!)"""
    
    # Use Ollama with a small model - only 400MB!
    llm = Ollama(
        model="qwen2.5:0.5b",  # Tiny 400MB model - fast and light!
        temperature=0.3,
    )

    # Custom prompt for documents
    prompt_template = """You are a helpful assistant. Use the following pieces of context from the document to answer the question. 
    If you don't know the answer based on the context, just say "I cannot find this information in the provided document."
    
    Context: {context}
    
    Question: {question}
    
    Answer:"""
    
    PROMPT = PromptTemplate(
        template=prompt_template, 
        input_variables=["context", "question"]
    )

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5}
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=False,
        chain_type_kwargs={"prompt": PROMPT}
    )
    
    return qa_chain