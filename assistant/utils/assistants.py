"""Chatbot using OpenAI Assistant on backend"""
from langchain.agents.openai_assistant import OpenAIAssistantRunnable
from langchain.agents import AgentExecutor
from typing_extensions import override
from langchain_core.agents import AgentFinish
from .retriever import Retriever
from typing import Optional, List, Tuple
import os
import yaml
from openai import OpenAI
class CustomAssistant():
    def __init__(self, instructions : Optional[str], retrieval=False, api=False, existing_assistant_id=""):
        self.instructions = instructions
        
        self.tools = []
        if retrieval:
            # tools.append({"type" : "retrieval"})
            self.retriever = Retriever()
            self.retriever.process_files()
            self.tools.append(self.retriever.get_tool())
        if api:
            self.tools.extend(self._tools())
        if existing_assistant_id != "":
            self.agent = OpenAIAssistantRunnable(assistant_id=existing_assistant_id)
        else:
            
            self.agent = OpenAIAssistantRunnable.create_assistant(
                name="Babylon Chatbot",
                instructions=self.instructions,
                model="gpt-4-turbo-preview",
                tools=self.tools,
                # file_ids=[x.id for x in self.process_files()] if retrieval else None,
                # as_agent=(True if retrieval else False)
        )

    def process_files(self):
        path = os.getcwd() + "/files/"
        return_files = []
        client = OpenAI()
        for files in os.listdir(path):
            file_split = files.split(".")
            if file_split[1] == "txt":
                pass
                # f = open(path + files, 'r')
                # for line in f:
                #     line = line[0:-1]

                #     app.add(line, data_type="web_page")
            else:
                file = client.files.create(
                    file=open(path + files, "rb"),
                    purpose="assistants"
                )
                return_files.append(file)
        return return_files

    def add_thread(self):
        # TO-DO: if multiple users
        pass
    def ask_assistant(self, query : str, thread_id="", run_id=None):
        # thread, run_id are passed in as keys
        build_dict = {"content" : query}
        if thread_id:
            build_dict["thread_id"] = thread_id
        output = self.agent.invoke(build_dict)
        return output
    
    # Use the first assistant to convert user given prompts into API calls that are then fed into the APIChain, then finetune it nad 
    # agent = OpenAIAssistantRunnable(assistant_id="asst_AOk1WPnaXRt3u8yWBWlwY8iu", as_agent=True)
    # need to create tools for the agent
    def _tools(self):
        return [
            {
                "type" : "function",
                "function" : {
                    "name":  "boolean_property_switcher",
                    "description": "Turn farm's properties/attributes on or off, or in other words true or false",
                    "parameters" : {
                        "type" : "object",
                        "properties": {
                            "property": {
                                "type" : "string",
                                "description" : "The property of the micro-farm to change.",
                            },
                            "value" : {
                                "type": "string",
                                "description" : """The new value of the property of the micro-farm to be changed. """,
                            }
                        },
                        "required" : ["property", "value"],
                    }
                }
            },
            {
                "type" : "function",
                "function" : {
                    "name" : "value_property_changer",
                    "description" : "Change a farm's property to a certain number or string that is provided in the prompt",
                    "parameters" : {
                        "type" : "object",
                        "properties" : {
                            "property" : {
                                "type" : "string",
                                "description" : "The property of the micro-farm to change",
                            },
                            "value" : {
                                "type" : "string",
                                "description" : "A number or string value that is the new value of the property to be changed",
                            }
                        },
                        "required" : ["property", "value"]
                    }
                }
            },
            {
                "type" : "function",
                "function" : {
                    "name" : "all_but_one_property",
                    "description" : "The prompt will say to keep one property on and turn all the others off, or in other words keep one property true and all others false.",
                    "parameters" : {
                        "type" : "object",
                        "properties" : {
                            "property" : {
                                "type" : "string",
                                "description" : "The property of the micro-farm to change"
                            }
                        },
                        "required" : ["property"],
                }
            }
            },
            {
                "type" : "function",
                "function" : {
                    "name" : "activate_function",
                    "description" : "The prompt will be a command to either activate/deactivate an attribute of a farm",
                    "parameters" : {
                        "type" : "object",
                        "properties": {
                            "property" : {
                                "type" : "string",
                                "description" : "The property of the micro-farm to change",
                            },
                            "value": {
                                "type" : "string",
                                "description" : "Should be true if the prompt is saying to activate, and false is the prompt means to deactivate."
                            }
                        },
                        "required" : ["property"],

                    }
                }
            },
        ]
