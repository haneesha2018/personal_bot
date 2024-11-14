from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pypdf import PdfReader
from abc import abstractmethod, ABC


class BaseLoader(ABC):
    """
    An abstract base class for implementing document loaders for different file formats.

    Attributes:
        streamlit_file (UploadedFile): The file uploaded by the user.

    Methods:
        read(): An abstract method that should be implemented by subclasses to read the contents of the file.
        load(): Reads the file using the read() method and returns a LangChain Document object with the file's content.
    """
    def __init__(self, streamlit_file):
        self.streamlit_file = streamlit_file

    @abstractmethod
    def read(self):
        pass

    def load(self):
        data = self.read()
        return Document(page_content=data)


class PDFLoader(BaseLoader):
    """
    A class that inherits from BaseLoader and implements the read() method for loading PDF files.

    Methods:
        read(): Reads the contents of a PDF file and returns the text as a string.
    """
    def read(self):
        pdf = PdfReader(self.streamlit_file)
        output = []
        for page in pdf.pages:
            text = page.extract_text()
            output.append(text)

        return "".join(output)


class TextFileLoader(BaseLoader):
    """
    A class that inherits from BaseLoader and implements the read() method for loading text files.

    Methods:
        read(): Reads the contents of a text file and returns the text as a string.
    """
    def read(self):
        output = []
        for line in self.streamlit_file:
            output.append(line.decode('utf-8'))
        return "".join(output)


class DocumentLoader:
    """
    A class that handles loading and splitting of documents in various formats such as PDF and text files. It uses the RecursiveCharacterTextSplitter to split the documents into smaller chunks.

    Attributes:
        text_splitter (RecursiveCharacterTextSplitter): An instance of the RecursiveCharacterTextSplitter class used for splitting documents.
        loader_configs (dict): A dictionary containing the mapping of file extensions to their respective loader classes.
        streamlit_file (UploadedFile): The file uploaded by the user.

    Methods:
        load_and_split(): Loads the document using the appropriate loader class based on the file extension and splits it into smaller chunks using the text_splitter.
    """
    def __init__(self, streamlit_file):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=250
        )
        self.loader_configs = {
            "pdf": PDFLoader,
            "txt": TextFileLoader
        }
        self.streamlit_file = streamlit_file

    def load_and_split(self):
        path = self.streamlit_file.name
        extension = path.split(".")[-1]
        loader_class = self.loader_configs[extension]
        loader = loader_class(self.streamlit_file)
        document = loader.load()
        docs = self.text_splitter.split_documents([document])
        return docs
