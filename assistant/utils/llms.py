"""Class Wrappers for Different LLMs from Service Providers"""
from langchain_openai import ChatOpenAI
from openai import OpenAI
import google.generativeai as genai
class LangchainOpenAI():
    def __init__(self, model_name : str):
        self.model = ChatOpenAI(model_name="gpt-4-turbo-preview", temperature=0.0)
    def get_model(self):
        return self.model
    
class OpenAIClient():
    def __init__(self, model_name : str) -> None:
        self.model = OpenAI(model_name, api_key="REMOVED")
    def get_model(self):
        return self.model

class GeminiClient():
    def __init__(self, model_name : str = 'gemini-pro', temp : int = 0.1) -> None:
        self.model = genai.GenerativeModel(model_name,
                        generation_config=genai.GenerationConfig(
                            max_output_tokens=2000,
                            temperature=temp,
                        ))
        self.cur_chat = None
        self.create_chat()
    
    def model_type():
        return "Google"
    def invoke(self, query : str):
        if self.cur_chat:
            return self.cur_chat.send_message(query).text
        raise ValueError("Start chat before sending messages")
    def create_chat(self):
        self.cur_chat = self.model.start_chat(history=[])
        self.cur_chat.send_message("""
            You are an informational chatbot that will use your chat history and provided knowledge from the user to
                answer any queries the user has about hydroponic farming and science in general.
            """)
    

