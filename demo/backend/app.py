from fastapi import FastAPI
from pydantic import BaseModel

from typing import BinaryIO, List, Tuple
from io import BytesIO
import tempfile
import threading
import queue
import os

# keep track of the chroma db embeddings
# how to track files that are added
# Add functionality to add google docs into app automatically - this can be solved by just people doing it
# add web crawler for hydroponic farming - this can as well, but web crawler might be better

from embedchain import App
from embedchain.config import BaseLlmConfig
from embedchain.helpers.callbacks import (StreamingStdOutCallbackHandlerYield,
                                          generate)

OPENAI_API_KEY = 'REMOVED'
file_type_dictionary = {
    "pdf" : "pdf_file",
    "csv" : "csv",
    "txt" : 'text',
    "md" : "mdx",
}
class File(BaseModel):
    name : str
    content : BytesIO
    file_type : str

class Chatbot(BaseModel):
    openapi_key : str
    db_file_path : str

app = FastAPI()

@app.get("/")
async def root():
    return {"message" : "Welcome to the API for the Chatbot" }
@app.post("/")
def startup():
    global chatbot
    chatbot : App = embedchain_bot('db', OPENAI_API_KEY)


@app.post("/file")
async def add_file(body : File):
    file_name = body.name
    content = body.content
    file_type = body.file_type
    with tempfile.NamedTemporaryFile(mode="wb", delete=False, prefix=file_name) as f:
        f.write(content.getvalue())
        temp_file_name = f.name
        if temp_file_name:
            chatbot.add(temp_file_name, data_type=file_type)

@app.get("/query")
def get_response(prompt : str):
    q = queue.Queue()
        # response = await llm.arun(message, callbacks=[NiceGuiLogElementCallbackHandler(log)])
    def app_response(result):
        llm_config = app.llm.config.as_dict()
        llm_config["callbacks"] = [StreamingStdOutCallbackHandlerYield(q=q)]
        config = BaseLlmConfig(**llm_config)
        answer, citations = app.chat(prompt, config=config, citations=True)
        result["answer"] = answer
        result["citations"] = citations
    results = {}
    thread = threading.Thread(target=app_response, args=(results,))
    thread.start()
    full_response = ""
    for answer_chunk in generate(q):
        full_response += answer_chunk
    return full_response


def embedchain_bot(db_path, api_key):
    return App.from_config(
        config={
            "llm": {
                "provider": "openai",
                "config": {
                    "model": "gpt-3.5-turbo-1106",
                    "temperature": 0.5,
                    "max_tokens": 1000,
                    "top_p": 1,
                    "stream": True,
                    "api_key": api_key,
                },
            },
            "vectordb": {
                "provider": "chroma",
                "config": {"collection_name": "chat-pdf", "dir": db_path, "allow_reset": True},
            },
            "embedder": {"provider": "openai", "config": {"api_key": api_key}},
            "chunker": {"chunk_size": 1000, "chunk_overlap": 0, "length_function": "len"},
        }
    )