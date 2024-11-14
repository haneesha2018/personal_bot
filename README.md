# Chat with Your Docs App

## Introduction

This repository will allow you to create a GPT powered chatbot app that has your basic ChatGPT chat capabilities, along with an optimized feature to upload large pdf/txt documents to the chat and chat with these documents. This application is built with the `Streamlit` framework and we interact with OpenAI using `LangChain`. Some features of this app include:
- **Conversational Memory**: Ability to remember a certain amount of chat messages when responding to the user.
- **Interactive Chatbot**: Ability to interact in a ChatGPT-like conversation without any prior documents.
- **Document Interaction**: Ability to add Large PDF/txt documents into the conversation and memory, allowing users to ineract with the document.
- **History Clearing**: This application can clear the history of the chat and conversational memory all within the UI.
- **Vector Database**: This application uses Facebook AI Similarity Search (FAISS) to store and search for our text embeddings.
  
![](https://github.com/danplotkin/chat_with_your_docs_app/blob/master/cwyd_demo%20(online-video-cutter.com).gif)

## Prerequisites

Before getting started, ensure you have the following installed on your system:

1. Python: This project is compatible with Python versions below 3.12. It has been tested and works well with the following Python versions:
   - Python 3.11
   - Python 3.10
2. Git
3. [OpenAI API Key](https://platform.openai.com/api-keys)

## Getting Started

### 1. Clone the Repository

Clone this repository to your local machine using the following command:

```bash
git clone https://github.com/danplotkin/chat_with_your_docs_app.git
```

### 2. Create a Vitual Environment
```bash
cd chat_with_your_docs_app
python -m venv myvenv
```

### 3. Activate Virtual Environment
* Windows:

> Using Git Bash:
```bash
source myvenv/Scripts/activate  
```

> Using Command Prompt:
```bash
myvenv\Scripts\activate
```

* macOS/Linux:
```bash
source myvenv/bin/activate
```

### 4. Install Dependencies
 ```bash
pip install -r requirements.txt
```
### 5. Set Up Environment Variables
Navigate to the project .env file. Replace the default values with your varibales.

Environment Variables:

1. `OPENAI_API_KEY`: Your OpenAI API key, granting access to the OpenAI API for language processing tasks like text generation or classification.

2. `OPENAI_TEMPERATURE`: A parameter controlling the randomness of text generation from the OpenAI model. It determines how conservative or creative the model's responses are.

3. `OPENAI_MODEL_NAME`: The specific name or identifier of the OpenAI language model you're using (e.g., GPT-3, GPT-4, etc.).

4. `OPENAI_MAX_TOKEN`: The maximum number of tokens or words the OpenAI model can generate in a single response. It helps limit the length of generated text.

5. `OPENAI_DOCSEARCH_K`: A value representing a parameter for document search functionality within your app. It could control the relevance or specificity of document search results.

6. `BUFFER_MEMORY_TOKEN_LIMIT`: The amount of tokens to store in conversation buffer memory.

7. `CONFIG_PAGE_TITLE`: The title of the configuration page within your app, usually displayed at the top of the page.

8. `APP_NAME`: The name or title of your application.

9. `APP_DESCRIPTION`: A brief description or summary of your application's purpose or functionality.

### 6. Validate OpenAI API Key
Run the following command to validate your OpenAI API Key:
```bash
python scripts/validate_openai_apikey.py
```
If successful, it should return with `This validation test was successful.`

### 7. Run the Streamlit App
Run the streamlit app using the following command:

```bash
streamlit run main.py
```
It will direct yout to a url like `http://localhost:XXXX/` to test out the app.

### 8. Deploy an App to Streamlit
Once everything works and you are satisfied with the testing, you can deploy your app using the [documentation](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app).

## Questions or Support

For any questions, feedback, or support regarding this project, feel free to reach out:

📧 Email: [danmplotkin@gmail.com](mailto:danmplotkin@gmail.com)

I'm available during weekdays from 9 AM to 5 PM (GMT), and I'll do my best to respond to your inquiries as soon as possible.
