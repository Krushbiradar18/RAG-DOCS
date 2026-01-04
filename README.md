# 📚 RAG Document Assistant

A free, local Retrieval-Augmented Generation (RAG) system for querying PDF documents using AI - no API keys required!

## ✨ Features

- 🆓 **Completely Free** - No API costs, runs entirely locally
- 🚀 **Fast & Lightweight** - Uses Qwen2.5:0.5b (only 400MB model)
- 🔒 **Private** - All processing happens on your machine
- 💬 **Interactive Chat** - Ask questions about your documents
- 📄 **PDF Support** - Upload any PDF or use the default document
- 🧠 **Smart Retrieval** - FAISS vector search for accurate answers

## 🛠️ Technology Stack

- **LLM**: Ollama (Qwen2.5:0.5b) - Local inference
- **Embeddings**: HuggingFace Sentence Transformers - Free local embeddings
- **Vector Store**: FAISS - Fast similarity search
- **Framework**: LangChain - RAG orchestration
- **UI**: Streamlit - Interactive web interface

---

## 📋 Prerequisites

- macOS (Apple Silicon or Intel)
- Python 3.8 or higher
- Homebrew package manager
- At least 2GB free disk space

---

## 🚀 Complete Setup Guide

### Step 1: Create Project Structure

```bash
# Navigate to your desired location
cd ~/Desktop

# Create project directory
mkdir RAG-PAO
cd RAG-PAO

# Create folder structure
mkdir data
mkdir __pycache__

# Your structure should look like:
# RAG-PAO/
# ├── data/
# ├── app.py
# ├── rag_utils.py
# ├── requirements.txt
# └── README.md
```

### Step 2: Install Ollama

```bash
# Install Ollama using Homebrew
brew install ollama

# Start Ollama service
brew services start ollama

# Verify Ollama is running
ollama --version
```

### Step 3: Download AI Model

```bash
# Download the lightweight Qwen2.5 model (400MB)
ollama pull qwen2.5:0.5b

# Verify model is downloaded
ollama list

# Expected output:
# NAME              ID              SIZE    MODIFIED
# qwen2.5:0.5b      c5396e06af29    397 MB  X minutes ago
```

**Alternative Models** (if you have more resources):
```bash
# For better quality (but larger):
ollama pull phi3:mini        # 2.3GB
ollama pull mistral:latest   # 4.1GB
ollama pull llama3.1:latest  # 4.9GB

# Then update rag_utils.py line 69 to use your preferred model
```

### Step 4: Create Python Virtual Environment

```bash
# Make sure you're in the RAG-PAO directory
cd /Users/YOUR_USERNAME/Desktop/RAG-PAO

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Your prompt should now show (venv) at the beginning
```

### Step 5: Install Python Dependencies

```bash
# Make sure venv is activated (you should see (venv) in your prompt)
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt

# This will install:
# - streamlit (UI framework)
# - langchain (RAG framework)
# - langchain-community (LangChain integrations)
# - faiss-cpu (vector database)
# - pypdf (PDF processing)
# - sentence-transformers (embeddings)
# - ollama (Python client for Ollama)
```

**Installation may take 5-10 minutes**

### Step 6: Add Your PDF Documents

```bash
# Place your PDF files in the data folder
# Example:
cp ~/Documents/your-document.pdf data/

# Or use the default PDF that's already included
ls data/
```

### Step 7: Run the Application

```bash
# Make sure you're in the project directory with venv activated
cd /Users/YOUR_USERNAME/Desktop/RAG-PAO
source venv/bin/activate

# Start the Streamlit app
streamlit run app.py
```

The app will open in your browser at: **http://localhost:8502**

---

## 💻 Usage Instructions

### First Time Setup

1. **Open the app** in your browser (http://localhost:8502)
2. In the sidebar, you'll see "Use default PDF from data folder" is checked
3. Click **"🚀 Process Document"**
4. Wait for processing to complete (30 seconds - 2 minutes depending on PDF size)
5. Once you see "✅ Document processed successfully!", you can start asking questions!

### Asking Questions

Simply type your question in the chat input at the bottom:

**Example Questions:**
- "What is this document about?"
- "Summarize the main points"
- "Explain [specific topic] from the document"
- "What are the key takeaways?"

### Uploading Your Own PDF

1. Uncheck "Use default PDF from data folder"
2. Click "Browse files" and select your PDF
3. Click "🚀 Process Document"
4. Start asking questions!

---

## 🔧 Terminal Commands Reference

### Starting/Stopping Services

```bash
# Start Ollama service
brew services start ollama

# Stop Ollama service
brew services stop ollama

# Restart Ollama service
brew services restart ollama

# Check if Ollama is running
brew services list | grep ollama
```

### Virtual Environment Commands

```bash
# Activate venv (do this every time you open a new terminal)
source venv/bin/activate

# Deactivate venv
deactivate

# Check if venv is active (should show venv path)
which python
```

### Running the App

```bash
# Full command sequence
cd /Users/YOUR_USERNAME/Desktop/RAG-PAO
source venv/bin/activate
streamlit run app.py

# Stop the app
# Press Ctrl+C in the terminal
```

### Managing Ollama Models

```bash
# List installed models
ollama list

# Download a model
ollama pull MODEL_NAME

# Remove a model
ollama rm MODEL_NAME

# Test a model directly
ollama run qwen2.5:0.5b
```

---

## 📁 Project Structure

```
RAG-PAO/
│
├── app.py                  # Main Streamlit application
├── rag_utils.py           # RAG logic (PDF loading, embeddings, QA chain)
├── requirements.txt       # Python dependencies
├── README.md             # This file
│
├── data/                 # Place your PDF files here
│   └── *.pdf            # Your documents
│
├── venv/                # Python virtual environment (auto-generated)
│   ├── bin/
│   ├── lib/
│   └── ...
│
└── __pycache__/         # Python cache (auto-generated)
```

---

## 🐛 Troubleshooting

### "Command not found: ollama"

```bash
# Reinstall Ollama
brew reinstall ollama
brew services start ollama
```

### "Connection refused" error

```bash
# Ollama service is not running
brew services start ollama

# Wait a few seconds, then try again
sleep 3
streamlit run app.py
```

### "Module not found" errors

```bash
# Make sure venv is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### "Port already in use"

```bash
# Streamlit is already running
# Kill existing Streamlit processes
pkill -9 streamlit

# Or use a different port
streamlit run app.py --server.port 8503
```

### Model download is too slow

```bash
# Cancel current download
Ctrl+C

# Use a smaller model
ollama pull qwen2.5:0.5b

# Or use a mirror/proxy if available in your region
```

### Out of memory errors

```bash
# Use a smaller model
ollama pull qwen2.5:0.5b

# Update rag_utils.py line 69:
# model="qwen2.5:0.5b"
```

---

## 🔄 Daily Usage Workflow

```bash
# 1. Open Terminal

# 2. Navigate to project
cd /Users/YOUR_USERNAME/Desktop/RAG-PAO

# 3. Activate virtual environment
source venv/bin/activate

# 4. Make sure Ollama is running
brew services list | grep ollama

# 5. Start the app
streamlit run app.py

# 6. Open browser to http://localhost:8502

# 7. When done, press Ctrl+C to stop
```

---

## 📊 Performance Tips

1. **Smaller PDFs work better** - Try to keep PDFs under 50 pages for optimal speed
2. **Close other apps** - Free up RAM for better performance
3. **Use smaller models** - Qwen2.5:0.5b is recommended for most laptops
4. **Process once, query many times** - Once a document is processed, you can ask unlimited questions

---

## 🆕 Updating the App

```bash
# Navigate to project
cd /Users/YOUR_USERNAME/Desktop/RAG-PAO

# Activate venv
source venv/bin/activate

# Pull latest code (if using git)
git pull

# Update dependencies
pip install --upgrade -r requirements.txt

# Restart the app
streamlit run app.py
```

---

## 📝 Requirements File Content

Your `requirements.txt` should contain:

```txt
streamlit>=1.28.0
langchain>=0.1.0
langchain-community>=0.0.13
faiss-cpu>=1.7.4
pypdf>=3.17.0
sentence-transformers>=2.2.0
ollama
```

---

## 🤝 Contributing

Feel free to:
- Add more PDF documents to the `data/` folder
- Customize the UI in `app.py`
- Experiment with different models in `rag_utils.py`
- Adjust chunk sizes and retrieval parameters

---

## 📄 License

Free to use for personal and educational purposes.

---

## 🆘 Need Help?

**Common Issues:**
1. **App won't start**: Make sure venv is activated and Ollama is running
2. **Slow responses**: Use a smaller model or reduce PDF size
3. **Inaccurate answers**: Try adjusting the chunk_size in rag_utils.py (line 28)

**System Requirements:**
- Minimum: 8GB RAM, 5GB free disk space
- Recommended: 16GB RAM, 10GB free disk space

---

## 🎯 Quick Start Checklist

- [ ] Ollama installed (`brew install ollama`)
- [ ] Ollama service running (`brew services start ollama`)
- [ ] Model downloaded (`ollama pull qwen2.5:0.5b`)
- [ ] Virtual environment created (`python3 -m venv venv`)
- [ ] Virtual environment activated (`source venv/bin/activate`)
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] PDF added to data folder
- [ ] App running (`streamlit run app.py`)
- [ ] Browser opened to http://localhost:8502

**You're all set! Happy querying! 🚀**
