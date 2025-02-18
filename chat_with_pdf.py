import streamlit as st
from openai import OpenAI
from os import environ

from langchain.document_loaders import PyPDFLoader
import tempfile

def extract_text_from_pdf(uploaded_file):
    # Write the uploaded file to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.getbuffer())
        tmp_file_path = tmp_file.name

    # Use PyPDFLoader to load the PDF content from the temp file
    loader = PyPDFLoader(tmp_file_path)
    docs = loader.load()  # This returns a list of document objects
    # Combine text from all pages/documents
    text = "\n".join(doc.page_content for doc in docs)
    return text

st.title("📝 File Q&A with OpenAI")
uploaded_files = st.file_uploader("Upload your documents", 
type=("txt","pdf", "md"),
accept_multiple_files = True # Allow for multiple file selection 
)

question = st.chat_input(
    "Ask something about the uploaded documents",
    disabled=not uploaded_files,
)

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Ask something about the uploaded documents"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if question and uploaded_files:
    documents = [] # to hold the content of each file

    # Read the content of the uploaded files
    for uploaded_file in uploaded_files:
        
        file_extension = uploaded_file.name.split(".")[-1].lower()
        
        if file_extension in ["txt", "md"]:
            file_content = uploaded_file.read().decode("utf-8")
        
        elif file_extension == "pdf":
            file_content = extract_text_from_pdf(uploaded_file)
        
        else:
            st.error(f"Unsupported document type: {uploaded_file.name}")
            continue
        
        documents.append({"name": uploaded_file.name, "content": file_content})
    
    # Combine contents from all documents
    combined_content = "\n\n".join(doc["content"] for doc in documents)
    
    client = OpenAI(api_key=environ['OPENAI_API_KEY'])

    # Append the user's question to the messages
    st.session_state.messages.append({"role": "user", "content": question})

    st.chat_message("user").write(question)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="openai.gpt-4o",  # Change this to a valid model name
            messages=[
                {"role": "system", "content": f"Here's the content of the file:\n\n{combined_content}"},
                *st.session_state.messages
            ],
            stream=True
        )
        response = st.write_stream(stream)

    # Append the assistant's response to the messages
    st.session_state.messages.append({"role": "assistant", "content": response})