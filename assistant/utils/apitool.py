"""Main API Tool / Router"""
from .assistants import CustomAssistant
from langchain.chains.llm import LLMChain
from openai.types.beta.threads.thread_message import ThreadMessage
from langchain_openai import ChatOpenAI
from langchain_community.utilities.requests import RequestsWrapper
from dataclasses import dataclass
import json
import re
import datetime
from nltk.corpus import wordnet as wn
from nltk import ne_chunk, pos_tag, word_tokenize
import requests
from .prompt import API_RESPONSE_PROMPT, API_URL_PROMPT, FIRST_LEVEL_PROMPT, PARSING_PACKS_PROMPT, PACKS_CLASSIFIER_PROMPT, PACKS_POST_PROMPT
from typing import Dict, Optional, Any, List, Tuple
import yaml
_FARMS_URL = "https://api.dev-babylon.com/api/farms/"
_PACKS_URL = "https://api.dev-babylon.com/api/packs/"
_GENERAL_URL = "https://staging.babylon-service.com/api/farminfo/"
class APITool():
    def __init__(self) -> None:
        self.llm = ChatOpenAI(model_name="gpt-4-turbo-preview")
        self.api_request_chain = LLMChain(llm=self.llm, prompt=API_URL_PROMPT) # sets up LLM config
        self.api_response_chain = LLMChain(llm=self.llm, prompt=API_RESPONSE_PROMPT)
        self.first_level_chain = LLMChain(llm=self.llm, prompt=FIRST_LEVEL_PROMPT)
        self.packs_parsing_chain = LLMChain(llm=self.llm, prompt=PARSING_PACKS_PROMPT)
        self.packs_classifier_chain = LLMChain(llm=self.llm, prompt=PACKS_CLASSIFIER_PROMPT)
        self.packs_post_chain = LLMChain(llm=self.llm, prompt=PACKS_POST_PROMPT)
        self.api_assistant = CustomAssistant("""You are a chatbot that is going to take in prompts related to hydroponic farming and parse them using 
                            the function calling tools you are provided.""", api=True, existing_assistant_id="asst_9S03JE2ExHffNgBwNmejqX1a")
        
        self.constant_attributes = ['version', 'operators', 'resin_uuid', 'farm_uuid',
                                     'hardware_config', 'serial_num']
        self.farm_names : Dict[str, Any] = {}
        self.attributes = set()
        self._farm_parsing()
        
    def _farm_parsing(self):
        r = requests.get(_FARMS_URL, headers=self._create_headers())
        r = r.json()
        for json_object in r:
            self.farm_names[json_object['name']] = json_object['serial_num']
        self.attributes.update(r[0].keys())
    def _text_processing(self, prompt : str):
        # assistant_message = self.api_processor.query(prompt)
        # tool_calls = assistant_message.tool_calls
        list_ = self.api_assistant.ask_assistant(prompt)
        print(list_)
        if type(list_[0]) == ThreadMessage:
            return None, None
        for tool_call in list_:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            function_args["property"] = function_args["property"].lower()
            if function_args["property"]:
                function_args["property"].replace(" ", "_")
            for attribute in self.attributes:
                if function_args["property"] in attribute:
                    # value = 'true' if function_name == 'activate_function' else function_args["value"]
                    return attribute, function_args["value"]
        return None, None
    def _create_headers(self):
        headers = {"Authorization": f"Token REMOVED"}
        return headers
    def _find_farm(self, query):
        names = set(self.farm_names.keys())
        remove_word, ret = None, None
        for word in query.split(" "):
            for name in names:
                # print(word)
                if name.lower() in word.lower(): # if the farm name has been identified
                    ret = name
                    remove_word = word
        if ret:
            return ret, remove_word
        return "NO_NAME", "NO_NAME"
    def invoke(self, query : str):
        info = self.first_level_chain.invoke(input=query)
        print(info)
        if "OPERATIONS" in info:
            return self.operations_invoke(query)
        elif "PACKS" in info:
            return self.packs_invoke(query)
        return {'output' : "Error : please make your query about the micro-farm\'s operations or the packs inside it."}
    
    def packs_invoke(self, query : str):
        farm_name, remove_word = self._find_farm(query)
        if farm_name == "NO_NAME":
            names = " ".join(self.farm_names.keys())
            return {'output' : f"""When making a command to the chatbot, please include your farm name. Here are your farm names: {names}"""}
        classifier = self.api_request_chain.invoke(input=query)
        url = _GENERAL_URL + str(self.farm_names[farm_name])
        query = query.replace(remove_word, "")
        print(classifier)
        if classifier == "GET":
            return self.packs_attributes(query, url)
        elif classifier == "PATCH":
            return self.packs_command(query, url)
        # could combine the harvest germinate and transplant endpoints
    def operations_invoke(self, query : str):
        info = self.api_request_chain.invoke(input=query)
        farm_name, remove_word = self._find_farm(query)
        if farm_name == "NO_NAME":
            names = " ".join(self.farm_names.keys())
            return {'output' : f"""When making a command to the chatbot, please include your farm name. Here are your farm names: {names}"""}
        url = _FARMS_URL + str(self.farm_names[farm_name]) + "/"
        if "GET" in info:
            return self.get_attributes(query, url)
        elif "PATCH" in info:
            query = query.replace(remove_word, "")
            return self.change_attribute(query, url)
        return {'output' : "Error: the chatbot could not process your request as a GET or PATCH please try again."}
    def change_attribute(self, query : str, url : str):
        property, value = self._text_processing(query)
        print(property, value) 
        if not property or not value:
            return {'output' : 'Error identifying the attribute you want to change, please be more specific.'}
        payload = {
            property : value,
        }
        # only if autofarmer is on
        autofarmer_check = requests.request("GET", url, headers=self._create_headers())
        # if autofarmer_check.json()['auto_farmer']:
        requests.request("PATCH", url, headers=self._create_headers(), data={'auto_farmer' : 'false'})
        api_response = requests.request("PATCH", url, headers=self._create_headers(), data=payload)
        # requests.request("PATCH", url, headers=self.create_headers(), data={'auto_farmer' : 'true'})
        if api_response.status_code == 200:
            print(api_response.json()[property])
            return {'output' : "Sucessfully changed"}
        else:
            return {'output' : """Error : Please specify the parameter you want to 
                                change, it might help to explicitly state the parameter name and the value you want to set it to.
                            """}
    def get_attributes(self, query : str, url : str):
        api_response = requests.request("GET", url, headers=self._create_headers())
        answer = self.api_response_chain.invoke(
            question=query,
            category="OPERATIONS",
            api_response=api_response.json())
        return {'output' : answer}
    def extract_temporal_expressions(self, query : str):
        tokens = word_tokenize(query)
        pos_tags = pos_tag(tokens)
        def is_temporal_word(word):
            synsets = wn.synsets(word)
            for synset in synsets:
                if any(lemma.name().startswith('temporal') or lemma.name().startswith('time') for lemma in synset.lemmas()):
                    return True
            return False
        temporal_words = []
        temporal_expressions = []
        current_expression = []

        for i, (token, tag) in enumerate(pos_tags):
            if is_temporal_word(token):
                current_expression.append(token)
            else:
                if current_expression:
                    temporal_expressions.append(' '.join(current_expression))
                    current_expression = []

                if tag.startswith('NNP'):  # Handling named entities
                    named_entity = ne_chunk(pos_tags[i:]).flatten()
                    if any(is_temporal_word(word) for word in named_entity):
                        temporal_expressions.append(' '.join(named_entity))

        if current_expression:
            temporal_expressions.append(' '.join(current_expression))

        return temporal_words, temporal_expressions

    def packs_attributes(self, query : str, url : str):
        # nevermind we're going to use the farminfo endpoint
        farm_info = requests.request("GET", url, headers=self._create_headers())
        packs_response = farm_info.json()['packs']
        activities = farm_info.json()['activities']
        new_obj = {
            'packs' : packs_response,
            'activities' : activities
        }
        final_response = json.dumps(new_obj)
        temporal_words, temporal_expressions = self.extract_temporal_expressions(query)
        
        answer = self.packs_parsing_chain.invoke(
            query=query,
            response=final_response,
            time_tags = " ,".join(temporal_words)
        )
        return {'output' : answer}
    def packs_command(self, query : str, url : str):
        # need to do processing here
        # for now harvest 
        category = self.packs_post_chain.invoke(query=query).lower()
        if "clean" in category:
            requests.request("PATCH", url, data={
                'date_last_clean' : datetime.datetime.now()
            }, headers=self._create_headers())
            return {'output' : "Clean date successfully set."}
        switches = {
            "harvest" : "",
            "transplant" : "",
            "clean" : "",
            "refill_ec": "",
            "refill_ph" : "",
        }
        print(category)
        return {'output' : "Default answer"}

