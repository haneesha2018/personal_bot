import streamlit as st
from utils.custom_models import ChatWithYourDocuments
from dotenv import load_dotenv
import os
from langchain.chains import LLMChain
from utils.prompts import LLMCHAIN_QA_PROMPT

load_dotenv()


class App:
    def __init__(self):
        st.set_page_config(page_title=os.getenv('CONFIG_PAGE_TITLE'))
        self.title = st.empty()
        self.title.title(f"{os.getenv('APP_NAME')}\n{os.getenv('APP_DESCRIPTION')}")
        self.file = st.empty()

    @staticmethod
    def _init_session_state():
        if 'messages' not in st.session_state:
            st.session_state.messages = []

        if 'prev_uploaded_file' not in st.session_state:
            st.session_state.prev_uploaded_file = None

        if 'model' not in st.session_state or st.session_state.model is None:
            st.session_state.model = ChatWithYourDocuments()

        if 'memory' not in st.session_state:
            st.session_state.memory = st.session_state.model.qa.memory

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    def _file_upload(self):
        with st.sidebar:
            self.file = st.file_uploader(
                label="Upload a document (.pdf, .txt):",
                type=["pdf", "txt"]
            )

        if self.file:
            if st.session_state.prev_uploaded_file != self.file.name:
                try:
                    with st.spinner('Reading...'):
                        self.title.empty()
                        self.title.markdown(f"# {os.getenv('APP_NAME')}")
                        st.session_state.prev_uploaded_file = self.file.name
                        st.session_state.model.embed_document(self.file)
                        st.success(f'Successfully uploaded {st.session_state.prev_uploaded_file} to chat!')
                except IndexError:
                    st.error(f"Error uploading {self.file.name}. This document may not be suitable.")

        else:
            if st.session_state.messages != []:
                self.title.empty()
                self.title.markdown(f"# {os.getenv('APP_NAME')}")
                
            st.session_state.model.db = None
            st.session_state.model.qa = LLMChain(
                llm=st.session_state.model.llm,
                memory=st.session_state.memory,
                prompt=LLMCHAIN_QA_PROMPT
            )
            if st.session_state.prev_uploaded_file is not None:
                st.info(f'Successfully removed {st.session_state.prev_uploaded_file} from the chat.')
                st.session_state.prev_uploaded_file = None

    def _interact(self):
        user_input = st.chat_input("Your Message:")

        if user_input:
            self.title.empty()
            self.title.markdown(f"# {os.getenv('APP_NAME')}")
            with st.chat_message("user"):
                st.markdown(user_input)
            st.session_state.messages.append({"role": "user", "content": user_input})

            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                with st.spinner('Generating Response...'):
                    try:
                        result = st.session_state.model.generate(user_input)
                        st.session_state.messages.append({"role": "assistant", "content": result})
                        message_placeholder.markdown(result)
                    except Exception as e:
                        st.error(e)

    @staticmethod
    def _clear_history():
        with st.sidebar:
            clear_hist_button = st.button('Clear History')
            if clear_hist_button:
                st.session_state.messages = []
                st.session_state.model.memory.chat_memory.messages.clear()
                st.rerun()

    def run(self):
        self._init_session_state()
        self._file_upload()
        self._interact()
        self._clear_history()
        

if __name__ == "__main__":
    app = App()
    app.run()
