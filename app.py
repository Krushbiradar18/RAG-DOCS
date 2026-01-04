import streamlit as st
from rag_utils import (
    load_and_split_pdf,
    create_vectorstore,
    create_qa_chain
)
import os

# Fix for event loop issues in Streamlit
import asyncio
import sys
if sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
else:
    try:
        asyncio.get_event_loop()
    except RuntimeError:
        asyncio.set_event_loop(asyncio.new_event_loop())

st.set_page_config(page_title="RAG Assistant", layout="wide")

st.title("📚 Document RAG Assistant")
st.write("Ask questions based on your document using AI.")
st.info("💡 **Note:** Using Ollama Qwen2.5:0.5b (400MB - Fast & Light!) + HuggingFace Embeddings")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "qa_chain" not in st.session_state:
    st.session_state.qa_chain = None
if "processed" not in st.session_state:
    st.session_state.processed = False

# -----------------------------
# Sidebar Inputs
# -----------------------------
with st.sidebar:
    st.header("🔐 Configuration")
    
    # Option to use default PDF or upload new one
    use_default = st.checkbox("Use default PDF from data folder", value=True)
    
    if use_default:
        uploaded_pdf = "/Users/krushnali/Desktop/RAG-PAO/data/Uncertainity, Probabilites, Bayes Theorem, Bayesian Belief Network, Hidden Markov Model.pdf"
        st.success("✅ Using: Uncertainity, Probabilites, Bayes Theorem.pdf")
    else:
        uploaded_pdf = st.file_uploader(
            "Upload Document (PDF)",
            type=["pdf"],
            help="Upload a PDF document to analyze"
        )
    
    process_btn = st.button("🚀 Process Document", type="primary")
    
    if st.session_state.processed:
        st.success("✅ Document processed and ready!")
        if st.button("🔄 Clear and Upload New Document"):
            st.session_state.qa_chain = None
            st.session_state.chat_history = []
            st.session_state.processed = False
            st.rerun()

# -----------------------------
# Process PDF
# -----------------------------
if process_btn:
    if not uploaded_pdf:
        st.error("⚠️ Please select or upload a PDF.")
    else:
        try:
            with st.spinner("📄 Loading and processing document..."):
                # Handle both file upload and file path
                if isinstance(uploaded_pdf, str):
                    # Load from file path
                    with open(uploaded_pdf, 'rb') as f:
                        from io import BytesIO
                        pdf_bytes = BytesIO(f.read())
                        chunks = load_and_split_pdf(pdf_bytes)
                else:
                    chunks = load_and_split_pdf(uploaded_pdf)
                    
                st.info(f"✂️ Document split into {len(chunks)} chunks")
                
            with st.spinner("🔮 Creating embeddings and vector store (using local embeddings - fast!)..."):
                # Create vector store
                vectorstore = create_vectorstore(chunks)
                
            with st.spinner("🤖 Setting up QA chain with Ollama..."):
                # Create QA chain
                st.session_state.qa_chain = create_qa_chain(vectorstore)
                st.session_state.processed = True
                
            st.success("✅ Document processed successfully! You can now ask questions.")
            st.balloons()
            
        except Exception as e:
            st.error(f"❌ Error processing document: {str(e)}")
            if "Ollama" in str(e) or "connection" in str(e).lower():
                st.info("💡 **Ollama not running!**\n"
                       "Install: `brew install ollama` (Mac) or download from ollama.ai\n"
                       "Download model: `ollama pull qwen2.5:0.5b` (only 400MB!)\n"
                       "Start server: `brew services start ollama`")
            else:
                st.info("Try uploading a different PDF or check the error message.")

# -----------------------------
# Chat Interface
# -----------------------------
if st.session_state.qa_chain is not None:
    st.divider()
    st.subheader("💬 Ask Questions")
    
    # Display chat history
    for i, (role, message) in enumerate(st.session_state.chat_history):
        with st.chat_message("user" if role == "You" else "assistant"):
            st.write(message)
    
    # Chat input
    user_query = st.chat_input("Ask a question about the document...")
    
    if user_query:
        # Display user message
        with st.chat_message("user"):
            st.write(user_query)
        
        st.session_state.chat_history.append(("You", user_query))
        
        # Get and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    result = st.session_state.qa_chain({"query": user_query})
                    answer = result["result"]
                    st.write(answer)
                    st.session_state.chat_history.append(("Assistant", answer))
                except Exception as e:
                    error_msg = f"Error generating response: {str(e)}"
                    st.error(error_msg)
                    st.session_state.chat_history.append(("Assistant", error_msg))
else:
    st.info("👆 Click 'Process Document' in the sidebar to get started with the default PDF or upload your own!")