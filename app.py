import streamlit as st
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ollama import ChatOllama
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
import os


from dotenv import load_dotenv
load_dotenv()

os.environ['LANGSMITH_API_KEY']=os.getenv("LANGSMITH_API_KEY")
os.environ['LANGSMITH_TRACING_URL']=os.getenv("LANGSMITH_TRACING_URL")
os.environ['LANGCHAIN_PROJECT']=os.getenv("LANGCHAIN_PROJECT")
os.environ['LANGSMITH_TRACING']=os.getenv("LANGSMITH_TRACING")

st.title("📘 Chat with your PDF")
st.write("Upload a PDF and chat with its content.")

session_id = st.text_input("Session ID", value="default_session")

# Use localhost because Ollama runs in the same container
llm = ChatOllama(model="gemma3:1b", base_url="http://127.0.0.1:11434")
embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url="http://127.0.0.1:11434")


if "store" not in st.session_state:
    st.session_state.store = {}

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file:
    temppdf = "./temp.pdf"
    with open(temppdf, "wb") as f:
        f.write(uploaded_file.getvalue())

    loader = PyPDFLoader(temppdf)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=4000, chunk_overlap=500)
    splits = text_splitter.split_documents(documents)
    vectorstore = Chroma.from_documents(splits, embedding=embeddings)
    retriever = vectorstore.as_retriever()

    contextualize_q_prompt = ChatPromptTemplate.from_messages([
        ("system", "Given a chat history and the latest user question "
                   "which might reference context in the chat history, "
                   "formulate a standalone question. Do NOT answer it."),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ])

    history_aware_retriever = create_history_aware_retriever(llm, retriever, contextualize_q_prompt)

    system_prompt = (
        "You are an assistant for question-answering tasks. "
        "Use the following retrieved context to answer the question. "
        "If you don't know, say you don't know. "
        "Keep the answer concise.\n\n{context}"
    )

    qa_prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ])

    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

    def get_session_history(session: str) -> BaseChatMessageHistory:
        if session not in st.session_state.store:
            st.session_state.store[session] = ChatMessageHistory()
        return st.session_state.store[session]

    conversational_rag_chain = RunnableWithMessageHistory(
        rag_chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer"
    )

    user_input = st.text_input("Your question:")
    if user_input:
        session_history = get_session_history(session_id)
        response = conversational_rag_chain.invoke(
            {"input": user_input},
            config={"configurable": {"session_id": session_id}}
        )
        st.success(f"Assistant: {response['answer']}")
        st.write("Chat History:", session_history.messages)
