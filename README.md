# 📌 INFO-5940 Assignment 1

This repository contains a document-based Q&A chatbot developed as part of the INFO 5940-005 course instructed by Ayham Boucher. The chatbot allows users to upload .txt and .pdf documents and interactively ask questions based on the uploaded content. The application uses OpenAI's API for generating contextually accurate responses and leverages LangChain for document processing and retrieval.

The project runs within a Docker environment for consistent and isolated development, with complete setup instructions provided for VS Code and containerized deployment.

This work references code and materials from the official course repository:

[INFO 5940 Course Repository] (https://github.com/AyhamB/INFO-5940.git) (Branches: lecture-05, lecture-06)

## 💡 Features

✅ Upload and process .txt and .pdf (also .md) files.

✅ Conversational interface using Streamlit.

✅ Supports multi-document uploads and differentiates content between files.

✅ Uses LangChain for document processing and chunking.

✅ Retrieves and ranks relevant document chunks based on user queries.

✅ Provides contextually accurate responses using OpenAI's embeddings and GPT model.

## 🛠️ Prerequisites

Before starting, ensure you have the following installed on your system:

- [Docker](https://www.docker.com/get-started) (Ensure Docker Desktop is running)  
- [VS Code](https://code.visualstudio.com/)  
- [VS Code Remote - Containers Extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)  
- [Git](https://git-scm.com/)  
- OpenAI API Key 

## 🚀 Setup Guide  

### 1️⃣ Clone the Repository  

Open a terminal and run:  

```bash
git clone https://github.com/sydneyci11/INFO-5940-assignment01.git

cd INFO-5940-assignment01
```

---

### 2️⃣ Open in VS Code with Docker  

1. Open **VS Code**, navigate to the `INFO-5940` folder.  
2. Open the Command Palette (`Ctrl+Shift+P` or `Cmd+Shift+P` on Mac) and search for:  
   ```
   Remote-Containers: Reopen in Container
   ```
3. Select this option. VS Code will build and open the project inside the container.  

📌 **Note:** If you don’t see this option, ensure that the **Remote - Containers** extension is installed.  

---

### 3️⃣ Configure OpenAI API Key  

Since `docker-compose.yml` expects environment variables, follow these steps:  

#### ➤ Option 1: Set the API Key in `.env` (Recommended)  

1. Inside the project folder, create a `.env` file:  

   ```bash
   touch .env
   ```

2. Add your API key and base URL:  

   ```plaintext
   OPENAI_API_KEY=your-api-key-here
   OPENAI_BASE_URL=https://api.ai.it.cornell.edu/
   TZ=America/New_York
   ```

3. Modify `docker-compose.yml` to include this `.env` file:  

   ```yaml
   version: '3.8'
   services:
     devcontainer:
       container_name: info-5940-devcontainer
       build:
         dockerfile: Dockerfile
         target: devcontainer
       environment:
         - OPENAI_API_KEY=${OPENAI_API_KEY}
         - OPENAI_BASE_URL=${OPENAI_BASE_URL}
         - TZ=${TZ}
       volumes:
         - '$HOME/.aws:/root/.aws'
         - '.:/workspace'
       env_file:
         - .env
   ```

4. Restart the container:  

   ```bash
   docker-compose up --build
   ```

---

## 🔄 Managing Docker and Devcontainer Setup

The application utilizes Docker and Devcontainer setups:

- **Dockerfile:** Defines the development environment and installs necessary dependencies.

- **docker-compose.yml:** Configures container settings and manages environment variables.

- **.devcontainer/:** Contains configurations for VS Code Remote Containers.

### ✅ Changes Made to original configuration:

Explicitly added pypdf (version ^5.3.0) and scipy (version ^1.14.1) dependencies based on the lecture-05 environment setup.


## ⚙️ Running the Application

Once your environment is set up and the container is running:

Inside the Docker container, run:

1. streamlit run chat_with_pdf.py

2. Open your browser and navigate to the displayed URL (typically http://localhost:8501/).

3. Upload your .txt or .pdf (also accept .md) documents and start asking questions!



## 📜 License

This project is licensed under the MIT License.
