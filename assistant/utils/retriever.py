"""Custom Retriever class built on top of Langchain with custom logic for vector db retrieval"""
import os
import fitz
from langchain_community.vectorstores import Weaviate
import weaviate
from weaviate.embedded import EmbeddedOptions
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from typing import Optional, Type
from langchain_community.document_loaders import TextLoader, PyPDFLoader

class Retriever():
    def __init__(self, chunk_size=25, chunk_overlap=20):
        self.chunker = CharacterTextSplitter(separator='.\n', chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        self.embeddings = OpenAIEmbeddings()
        self.db_created = False
        self.num_files = 0
        self.db = None
        self.client = weaviate.Client(
            embedded_options=EmbeddedOptions()
        )
    def chunk_file(self, file_path : str, file_type : str):
        encoding : Optional[str] = None
        loader = None
        if file_type == 'txt':
            loader = TextLoader(file_path, encoding)
        elif file_type == 'pdf':
            loader = PyPDFLoader(file_path) 
        documents = loader.load()
        return documents
    def add_file(self, file_path : str, file_type : str): # Or actual file in BytesIO, don't know yet
        docs = self.chunk_file(file_path, file_type)
        print(docs[0])
        texts = self.chunker.split_documents(docs)
        if not self.db_created:
            self.db_created = True
            self.db = Weaviate.from_documents(
                client=self.client,
                documents=texts,
                embedding=OpenAIEmbeddings(),
                by_text=False
            )
        else:
            self.db.add_documents(texts)
    def process_files(self): # process them all into .txt files
        path = os.getcwd() + "/files/"
        return_files = []
        for files in os.listdir(path):
            file_split = files.split(".")
            if file_split[1] == "txt":
                self.add_file(path + files, 'txt')
            elif file_split[1] == 'pdf':
                # with fitz.open(path + files) as doc:

                #     text = ""
                #     for page in doc:
                #         text += page.get_text()
                #     file_name = path + file_split[0] + ".txt"
                #     with open(file_name, "w") as f:
                #         f.write(text)
                self.add_file(path + files, 'pdf')
                # file = client.files.create(
                #     file=open(path + files, "rb"),
                #     purpose="assistants"
                # )
                # return_files.append(file)
    def convert_any_file_text(self, file_path : str, file_type : str):
        if file_type == 'pdf':
            with fitz.open(file_path) as doc:
                text = ""
                for page in doc:
                    text += page.get_text()
                return text
    def similarity_search_by_score(query: str, num_documents=4):
        pass
    def get_tool(self, num_k : int):
        retriever = self.db.as_retriever(search_kwargs={'k' : num_k, 'score_threshold' : 0.6})
        return retriever
        