# PDF Chatbot

A **PDF Chatbot** that allows users to upload PDF documents and chat with their content using an AI-powered assistant. Built using **Streamlit**, **LangChain**, and **Ollama embeddings**, and deployed on **AWS Fargate**.

---

## **Features**

- **PDF Upload & Parsing**: Upload single PDF documents for processing.  
- **Contextual Q&A**: Ask questions about the PDF content; the chatbot provides concise answers.  
- **History-Aware Conversations**: Maintains chat history to answer follow-up questions intelligently.  
- **Embeddings & Retrieval**: Uses Ollama embeddings and Chroma vector store for semantic search.  
- **Deployment-Ready**: Fully containerized and deployable on AWS Fargate.  
- **Secure Access**: Works with custom security groups allowing controlled access.

---

## **Tech Stack**

- **Frontend:** Streamlit  
- **Backend / AI:** Python, LangChain, Ollama  
- **Vector Database:** Chroma  
- **Deployment:** Docker, AWS Fargate, ECS  
- **Others:** PyPDFLoader for PDF processing, RecursiveCharacterTextSplitter for text splitting  

---

## **How It Works**

1. User uploads a PDF.  
2. The PDF is split into chunks and embedded using Ollama embeddings.  
3. A vector store (Chroma) stores the embeddings.  
4. User can ask questions about the PDF.  
5. The chatbot retrieves relevant chunks, reformulates questions if needed, and answers concisely.  
6. Conversation history is maintained for context-aware answers.  

---

## **Setup & Run Locally**

### **Prerequisites**

- Python 3.11+  
- Docker (optional, if using containerized deployment)  
- Streamlit  
- Required Python libraries (see `requirements.txt`)  

### **Steps**

1. **Clone the repository**

```bash
git clone <your-repo-url>
cd pdf-chatbot
```
2. **run the command to install requirements**
```
pip install -r requirements.txt
```
3. **to run the streamlit app**
```
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```
4. **Go to this url to access chatbot**
```
http://localhost:8501
```
