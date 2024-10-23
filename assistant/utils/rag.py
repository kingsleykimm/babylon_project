"""All RAG modes/classes built for the pipeline, BaseRAG is the abstract base class"""

from abc import ABC, abstractmethod
from typing import Optional
from io import StringIO
from .assistants import CustomAssistant
from .retriever import Retriever
from .ranker import CrossEncoderRanker
from .splade import SPLADEEmbeddings
from .llms import OpenAIClient, LangchainOpenAI, GeminiClient
from .prompt import RAG_PROMPT
from .splitter import CharacterTokenSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_openai import ChatOpenAI
from markdown import Markdown
import fitz
class BaseRAG():
    def __init__(self, instructions : Optional[str] = None ) -> None:
        self.instructions = instructions
        self.agent = None
    @abstractmethod
    def invoke(query : str):
        raise NotImplementedError
    @abstractmethod
    def add_file(file_path : str, file_type : str):
        raise NotImplementedError
    

class AssistantRAG(BaseRAG):
    def __init__(self, instructions : Optional[str] = ""):
        super().__init__(instructions)
        self.agent = CustomAssistant("""You are a chatbot designed to answer questions about hydroponic farming, general science and chemistry and Babylon Micro-Farms and it's products.
                        Do not deviate from these topics unless it is to educate the user, and keep in mind most users will be young children. You will also use your given files
                                             to construct curriculums on hydroponic farming.""", existing_assistant_id="asst_AOk1WPnaXRt3u8yWBWlwY8iu")
    def invoke(self, query : str):
        assistant_message = self.agent.ask_assistant(query, thread_id="thread_aOJGYbzvrfSciq2b6zYWUXLZ")
        if not assistant_message:
            raise ValueError("Assistant does not return any valid message")
        most_recent_message = assistant_message[-1]
        content = most_recent_message.content[0].text.value
        return {'output' : content}
    
class DenseSearchRAG(BaseRAG):
    def __init__(self, top_k : int, instructions : Optional[str] = None):
        super().__init__(instructions)
        self.top_k = top_k
        self.retriever = Retriever()
        # TODO: replace this without explicit file paths later
        self.retriever.add_file('/Users/kingsleykim0319/Desktop/Chatbot/chat-assistant/assistant/files/ExploringHydroponics_04.20_FINAL (1).pdf', file_type='pdf')
        self.retriever.add_file('/Users/kingsleykim0319/Desktop/Chatbot/chat-assistant/assistant/files/Galleri Micro-Farm User Guide - 2023.pdf', file_type='pdf')
        
        self.reranker = CrossEncoderRanker("cross-encoder/ms-marco-MiniLM-L-6-v2")
        self.model = ChatOpenAI(model_name="gpt-4-turbo-preview", temperature=0)
        self.chain = create_stuff_documents_chain(self.model, RAG_PROMPT)
        self.tool = self.retriever.get_tool(num_k=self.top_k)
    def add_file(self, file_path : str, file_type : str):
        self.retriever.add_file(file_path, file_type)
    def invoke(self, query : str):
        
        docs = self.tool.invoke(query)
        scores_with_docs = self.reranker.rerank(query, docs)
        final_documents = [scores_with_docs[i] for i in range(5)]
        content = self.chain.invoke({"context" : final_documents})
        """I felt the input was too constrained, so I added a call to the base OpenAI model, but I realized this 
        was causing the call to be 40 seconds long"""
        # base_chain_answer = self.model.predict(query)
        # res = self.reranker.preferred_answer(content, base_chain_answer, query)
        return {'output' : content}

class HybridSearchRAG(DenseSearchRAG):
    def __init__(self, top_k : int, instructions : Optional[str] = None, chunk_size : Optional[int] = 30) -> None:
        super().__init__(top_k, instructions)
        self.splitter = CharacterTokenSplitter(chunk_size)
        self.splade = SPLADEEmbeddings()
        self.add_file('/Users/kingsleykim0319/Desktop/Chatbot/chat-assistant/assistant/files/ExploringHydroponics_04.20_FINAL (1).pdf', file_type='pdf')
        self.add_file('/Users/kingsleykim0319/Desktop/Chatbot/chat-assistant/assistant/files/Galleri Micro-Farm User Guide - 2023.pdf', file_type='pdf') 
        
        
        
    def add_file(self, file_path : str, file_type : str):
        f_text = self.convert_any_file_text(file_path, file_type)
        doc_list = self.splitter.split_text_into_docs(f_text)
        self.splade.generate_embeddings_from_docs(doc_list, True)
        # self.splade.add_embeddings(doc_list)
    def convert_any_file_text(self, file_path : str, file_type : str):
        if file_type == 'pdf':
            with fitz.open(file_path) as doc:
                text = ""
                for page in doc:
                    text += page.get_text()
                return text
        elif file_type == 'txt':
            with open(file_path) as f:
                return f.read()
    def invoke(self, query : str):
        dense_docs = self.tool.invoke(query)
        return_docs = self.splade.search(self.top_k, query)
        union = list(set(return_docs + dense_docs))
        scores_with_docs = self.reranker.rerank(query, union)
        final_documents = [scores_with_docs[i] for i in range(self.top_k)]
        content = self.chain.invoke({"context" : final_documents})
        return {'output' : content}

class ContextRAG(BaseRAG):
    def __init__(self):
        self.client = GeminiClient()
        self.create_context()
        # self.client = OpenAIClient('gpt-4-turbo-preview')
        
    def create_context(self):
        self.file_text = ""
        # self.file_text += self.convert_any_file_text('/Users/kingsleykim0319/Desktop/Chatbot/chat-assistant/assistant/files/ExploringHydroponics_04.20_FINAL (1).pdf')
        # self.file_text += self.convert_any_file_text('/Users/kingsleykim0319/Desktop/Chatbot/chat-assistant/assistant/files/Galleri Micro-Farm User Guide - 2023.pdf')
        self.file_text += self.convert_any_file_text('/Users/kingsleykim0319/Desktop/Chatbot/chat-assistant/assistant/files/curriculum.md', file_type='md')
        self.client.invoke(self.file_text)
    def unmark_element(self, element, stream=None):
        if stream is None:
            stream = StringIO()
        if element.text:
            stream.write(element.text)
        for sub in element:
            self.unmark_element(sub, stream)
        if element.tail:
            stream.write(element.tail)
        return stream.getvalue()
    def convert_any_file_text(self, file_path : str, file_type : str = 'pdf'):
        if file_type == 'pdf':
            with fitz.open(file_path) as doc:
                text = ""
                for page in doc:
                    text += page.get_text()
                return text
        elif file_type == 'md':
            Markdown.output_formats["plain"] = self.unmark_element
            md = Markdown(output_format="plain")
            md.stripTopLevelTags = False
            f = open(file_path, 'r')
            res = md.convert(f.read())
            f.close()
            return res
    def invoke(self, query : str):
        return {'output' : self.client.invoke(query)}
        # response = self.client.chat.completions.create(
        #     model="gpt-4-turbo-preview",
        #     messages=[
        #         {"role" : "user", "content" : self.file_text},
        #         {"role" : "user", "content" : "Use the given context I provided to answer this next question: "},
        #         {"role" : "user", "content" : query}
        #     ]
        # )
        # return {'output' : response.choices[0].message.content}