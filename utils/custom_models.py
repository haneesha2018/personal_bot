from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationTokenBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.embeddings import OpenAIEmbeddings
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.vectorstores import FAISS
from langchain.chains import LLMChain
from utils.data_loaders import DocumentLoader
from utils.prompts import *
from dotenv import load_dotenv
import os

load_dotenv()


class ChatWithYourDocuments:
    """
    ChatWithYourDocuments: A class that enables users to chat with their documents by loading and embedding them, and then generating responses based on the document content using OpenAI's API.

    Attributes:
        llm (ChatOpenAI): An instance of the ChatOpenAI class for interacting with OpenAI's API.
        embeddings (OpenAIEmbeddings): An instance of the OpenAIEmbeddings class for generating embeddings of the documents.
        db (FAISS): A FAISS index for storing and searching document embeddings.
        memory (ConversationBufferWindowMemory): An instance of the ConversationBufferWindowMemory class for managing the conversation history.
        qa (LLMChain): An instance of the LLMChain class for generating responses based on the document content.

    Methods:
        embed_document(file): Loads and splits the document using the DocumentLoader class, generates embeddings for the document chunks, and stores them in the FAISS index.
        generate(query): Generates a response based on the given query and the document content using the qa instance.
    """
    def __init__(self):
        self.llm = ChatOpenAI(
            openai_api_key=os.getenv('OPENAI_API_KEY'),
            temperature=os.getenv('OPENAI_TEMPERATURE'),
            max_tokens=os.getenv('OPENAI_MAX_TOKEN'),
            model_name=os.getenv('OPENAI_MODEL_NAME'),
            streaming=True,
            callbacks=[StreamingStdOutCallbackHandler()]
        )
        self.embeddings = OpenAIEmbeddings(openai_api_key=os.getenv('OPENAI_API_KEY'))
        self.db = None
        self.memory = ConversationTokenBufferMemory(
            llm=self.llm,
            max_token_limit=os.getenv('BUFFER_MEMORY_TOKEN_LIMIT'),
            memory_key="chat_history",
            return_messages=True
        )
        self.qa = LLMChain(
            llm=self.llm,
            memory=self.memory,
            prompt=LLMCHAIN_QA_PROMPT
        )

    def embed_document(self, file):
        """
        Loads and splits the document using the DocumentLoader class, generates embeddings for the document chunks, and stores them in the FAISS index.
        """
        # load in documents
        loader = DocumentLoader(file)
        documents = loader.load_and_split()

        # create vector store
        self.db = FAISS.from_documents(documents, self.embeddings)

        self.qa = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.db.as_retriever(
                search_kwargs={'k': int(os.getenv('OPENAI_DOCSEARCH_K'))}
            ),
            memory=self.memory,
            chain_type='stuff',
            condense_question_prompt=CONDENSE_QA_PROMPT
        )
        self.qa.combine_docs_chain.llm_chain.prompt = QA_GENERATOR_PROMPT

    def generate(self, query):
        """
        Generates a response based on the given query and the document content using the qa object instance.
        """
        generator = self.qa.stream({'question': query})
        result = next(generator)
        try:
            return result['answer'].strip()
        except KeyError:
            return result['text'].strip()
