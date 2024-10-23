from langchain_core.language_models import BaseLanguageModel
from openai import OpenAI
from typing import Any, Dict, List, Optional, Type, Union, cast
import time
from utils import *
from config import Config
class MFAPIChain():
    def __init__(self, token : str, 
                 llm : Optional[BaseLanguageModel], 
                grade_level : str,
                history_token_cap : int, config : Config
                ):
        self.token = token
        self.config = config
        self.question_key = "content"
        self.first_prompt = True
        self.history_token_cap = config.context_length
        self.cur_history_length = 0
        self.messages = []
        self.api = APITool()
        self.grade_level = config.grade_level
        self.rag_table = {"dense_search" : DenseSearchRAG(top_k=10), 'assistant' : AssistantRAG(), 'context' : ContextRAG()}
        self.rag = self.rag_table[config.rag_model]
        self.reranker = CrossEncoderRanker("cross-encoder/ms-marco-MiniLM-L-6-v2")
        self.client = OpenAI()
        self.constant_attributes = ['version', 'operators', 'resin_uuid', 'farm_uuid',
                                     'hardware_config', 'serial_num'] # attributes that probably shouldn't be changed
        # self._setup()
    def _setup(self):
        self.rag.add_file('/Users/kingsleykim0319/Desktop/Chatbot/chat-assistant/assistant/files/ExploringHydroponics_04.20_FINAL (1).pdf', file_type='pdf')
        self.rag.add_file('/Users/kingsleykim0319/Desktop/Chatbot/chat-assistant/assistant/files/Galleri Micro-Farm User Guide - 2023.pdf', file_type='pdf')
    def invoke(self, inputs : Union[Dict[str, Any] : Any]):
        query = None
        category = None
        api_response = None
        assistant_response = ""
        start_time = time.time()
        response = None
        if isinstance(inputs, dict):
            query = inputs[self.question_key]
            category = inputs['category']
        else:
            query = inputs
        if category == 'API':
            response = self.api_invoke(query)['output']
        elif category == 'General':
            assistant_response = self.rag_invoke(query)['output']
        # while self.cur_history_length >= self.history_token_cap: # best way to implement history?
        #     length = len(self.messages[0])
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[ # can put in the user grade level here
                    {"role" : "system", "content" : f"""You are a helpful assistant that is going to take
                        in some input from the user and make sure it is understandable for students of grade level {self.grade_level},
                    and rewrite the output if necessary to always less than 5 sentences. Only answer topics related to hydroponic farming, general science and Babylon Micro-farms."""},
                    {"role" : "user", "content" : assistant_response}
                ]
            )
            response = response.choices[0].message.content
        return {'output' : response, 'response_time' : time.time() - start_time}
    def api_invoke(self, query : str):
        return self.api.invoke(query)
    def rag_invoke(self, query : str):
        # Weaviate Retriever
        return self.rag.invoke(query)

# Note: Should include a method to determine to use Get/Post/Update
    

