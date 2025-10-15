FROM python:3.11-slim

WORKDIR /app

# Install dependencies + Ollama
RUN apt-get update && apt-get install -y curl && \
    curl -fsSL https://ollama.com/install.sh | sh && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

EXPOSE 8501

ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Startup script
CMD bash -c "ollama serve & sleep 10 && \
    ollama pull gemma3:1b && \
    ollama pull nomic-embed-text:latest && \
    streamlit run app.py --server.port 8501 --server.address 0.0.0.0"
