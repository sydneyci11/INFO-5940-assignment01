# INFO 5940-005 Assignment 1
# Author: Sydney Chien
# This project was developed as part of INFO 5940-005 course
# Instructor: Ayham Boucher
# References: https://github.com/AyhamB/INFO-5940.git (Branch: lecture-05, lecture-06)
# This script allows users to upload .txt, .pdf, and .md files and ask questions about their content.
# The chatbot utilizes OpenAI's API and LangChain for document processing and response generation.

import streamlit as st
from openai import OpenAI
from os import environ

from langchain.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from scipy.spatial.distance import cosine
import tempfile

# Set up Streamlit app title
st.title("📝 File Q&A with OpenAI")

# Allow users to upload multiple documents (.txt, .pdf, .md)
uploaded_files = st.file_uploader("Upload your documents", 
type=("txt","pdf", "md"),
accept_multiple_files = True # Allow for multiple file selection 
)

# User input field for questions
question = st.chat_input(
    "Ask something about the uploaded documents",
    disabled=not uploaded_files,
)

# Initialize chat session history
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Ask something about the uploaded documents"}]

# Display previous messages in chat
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Function to extract text from uploaded documents
def extract_text(uploaded_file):
    file_extension = uploaded_file.name.split(".")[-1].lower()
    
    if file_extension in ["txt", "md"]:
        file_content = uploaded_file.read().decode("utf-8")
        return file_content

    elif file_extension == "pdf":
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.getbuffer())
            tmp_file_path = tmp_file.name
        loader = PyPDFLoader(tmp_file_path)
        docs = loader.load()
        text = "\n".join(doc.page_content for doc in docs)
        file_content = text
        
        return file_content
    else:
        st.error(f"Unsupported document type: {uploaded_file.name}")
        return None

# Only run if there's a question and uploaded files    
if question and uploaded_files:
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    
    # Process each file separately and store chunks with file metadata.
    chunks = []
    for uploaded_file in uploaded_files:
        file_text = extract_text(uploaded_file)
        if file_text:
            file_chunks = text_splitter.split_text(file_text)
            for chunk in file_chunks:
                chunks.append({"file": uploaded_file.name, "content": chunk})

    # Initialize the OpenAIEmbeddings model
    openai_embeddings = OpenAIEmbeddings(model="openai.text-embedding-3-large")

    # Compute the embedding for the user's question
    query_vector = openai_embeddings.embed_documents([question])[0]
    
    # Precompute embeddings for all document chunks
    chunk_embeddings = []
    for chunk_dict in chunks:
        chunk_vector = openai_embeddings.embed_documents([chunk_dict["content"]])[0]  
        chunk_embeddings.append({
            "file": chunk_dict["file"],
            "content": chunk_dict["content"],
            "embedding": chunk_vector
        })

    # Compare query embedding with stored chunk embeddings
    ranked_chunks = []
    for chunk in chunk_embeddings:
        similarity = 1 - cosine(query_vector, chunk["embedding"])
        ranked_chunks.append({"file": chunk["file"], "content": chunk["content"], "similarity": similarity})

    # Sort chunks by similarity (highest first)
    ranked_chunks.sort(key=lambda x: x["similarity"], reverse=True)

    # Select **top 5 chunks** to provide more context (more context, better response)
    top_chunks = ranked_chunks[:5]

    # Prepare relevant context for OpenAI response
    if top_chunks:
        context_message = "The most relevant context from uploaded files:\n\n"
        for chunk in top_chunks:
            context_message += f"📄 **File:** {chunk['file']}\n---\n{chunk['content']}\n\n"

    else:
        context_message = "No relevant context found in the uploaded files."

    client = OpenAI(api_key=environ['OPENAI_API_KEY'])

    # Append the user's question to the messages
    st.session_state.messages.append({"role": "user", "content": question})

    st.chat_message("user").write(question)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="openai.gpt-4o",  
            messages=[
                {"role": "system", "content": f"Here's the content of the file:\n\n{context_message}"},
                *st.session_state.messages
            ],
            stream=True
        )
        response = st.write_stream(stream)

    # Append the assistant's response to the messages
    st.session_state.messages.append({"role": "assistant", "content": response})