import requests
import os
import yaml
from langchain_community.agent_toolkits.openapi.spec import reduce_openapi_spec
import json
import datetime
# base_url = "http://api.dev-babylon.com/api/"
# babylon_api_key = "REMOVED"

# retriever = Retriever()
# retriever.add_file('/Users/kingsleykim0319/Desktop/Chatbot/chat-assistant/assistant/files/ExploringHydroponics_04.20_FINAL (1).pdf', file_type='pdf')
# retriever.add_file('/Users/kingsleykim0319/Desktop/Chatbot/chat-assistant/assistant/files/Galleri Micro-Farm User Guide - 2023.pdf', file_type='pdf')
# headers = {"Authorization": f"Token {babylon_api_key}"}
# # r = requests.get(f"{base_url}/farms", headers=headers)
# r = requests.post(f"{base_url}/farms/1/", headers=headers, data={'fan' : True})
# # print(r.reason, r.status_code)
# r = requests.get(f"{base_url}farms/1/", headers=headers)
# print(r.json())

# assistant = CustomAssistant(instructions="You are an educational chatbot that is designed to teach young students about hydroponic farming, who are also using a Babylon micro-farm to learn. Answer only questions related to farming, science, or Babylon Micro-farms.", retrieval=True)
# agent_Executor = AgentExecutor(agent=assistant, tools=assistant.tools)
# agent_Executor.invoke({"content" : "how do i set up my micro-farm"})
# # # array of threadmessages, which have an array of content
# print(assistant_message[0].content[0].text.value)
# for thread_message in assistant_message:
#     for content in thread_message:
#         print(content)
    # print(message.content.text)


base_url = "https://api.dev-babylon.com/api/"
# base_url = "https://staging.babylon-service.com/api/"
babylon_api_key = "REMOVED"
headers = {"Authorization": f"Token {babylon_api_key}"}
r = requests.request("PATCH", f"{base_url}farms/1/", data={

                'date_last_clean' : datetime.datetime.now()
            }, headers=headers)
print(r.json())
# # payload = {'activate_ec_pump': 'true', 'activate_ph_pump' : 'true'}
# # requests.request("PATCH", base_url, headers=headers, data={'auto_farmer' : 'false'})
# # r2 = requests.request("PATCH", f"{base_url}", headers=headers, data=payload)
# # requests.request("PATCH", base_url, headers=headers, data={'auto_farmer' : 'true'})
# # r1 = requests.request("GET", f"{base_url}", headers=headers)
# r = requests.get(f"{base_url}harvest", headers=headers)
# print(r.json())
from langchain_community.agent_toolkits.openapi import planner
# from langchain_openai import ChatOpenAI
# from langchain.requests import RequestsWrapper

# api_spec = reduce_openapi_spec(raw_spec)

# api_agent = planner.create_openapi_agent(api_spec, requests_wrapper, llm)
# user_query = "do I need to germinate any plants in farm with serial_num 1"
# api_agent.run(user_query)

# agent = OpenAPIAgent("swagger.yaml")
# specs = agent.get_raw_specs()

# get_agent = agent.create_openapi_agent(specs, requests_wrapper)
# get_agent_chain = agent._create_api_planner_tool(specs)
# print(get_agent_chain.predict(query="what are packs are in my farms"))
# print(get_agent.run({"input" : "What packs are in my farms?"}))
# print(r1.json()['fan'])
# import spacy
# client = OpenAI()

# url = "https://api.openai.com/v1/threads"
# token = "REMOVED"
# org = "REMOVED"
# headers = {
#     "Authorization": f"Bearer {token}", 
#     "Openai-Organization": f"{org}", 
#     "OpenAI-Beta": "assistants=v1"
# }

# resp = requests.get(url, headers=headers)
# print(resp.json())
# ids = [t['id'] for t in resp.json()['data']]

# while len(ids) > 0:
#     for tid in alive_it(ids, force_tty=True):
#         client.beta.threads.delete(tid)
#         time.sleep(1)
#     resp = requests.get(url, headers=headers)
#     ids = [t['id'] for t in resp.json()['data']]
# # Load the spaCy English model with dependency parsing capabilities
# nlp = spacy.load("en_core_web_sm", disable=["ner"])  # Disable named entity recognition

# # Define a function to process the text
# def process_text(text):
#   """
#   This function takes a text prompt and uses spaCy to identify the target property and its desired value.

#   Args:
#       text: The text prompt describing the property change (e.g., "Set the target_moisture to 70").

#   Returns:
#       A dictionary containing the identified property and its desired value, or None if not found.
#   """
#   # Parse the text using spaCy
#   doc = nlp(text)

#   # Find the property and value based on dependency parsing
#   property_name = None
#   value = None
#   for chunk in doc.noun_chunks:
#     if chunk.root.dep_ in ["attr", "nmod"]:  # Check for attribute or modifier dependency
#       property_name = chunk.text.strip()
#       # Identify numerical values within the same sentence (adjust based on your data)
#       for token in doc:
#         if token.pos_ == "NUM" and token.head == chunk.root:
#           value = token.text
#           break

#   # Return the results
#   return {property_name.lower(): value} if property_name and value else None

# # Example usage
# text = "Set the moisture level to 70"
# results = process_text(text)

# if results:
#   print(f"Property: {results.keys()[0]}")
#   print(f"Value: {results.values()[0]}")
# else:
#   print("No property change found in the text.")

# from custom_tools import APITool

# api = APITool()
# message = api.query("Activate cycling pump")
# print(message.tool_calls[0].function.arguments)

# r = Retriever()
# r.process_files()
# retriever = r.get_tool()
# model = ChatOpenAI(model="gpt-4", temperature=0)
# template = """You are an educational chatbot that is designed to answer questions 
# about hydroponic farming, science and Babylon Micro-farms. Your users will mainly be young students.
# Use the following pieces of retrieved context to answer the question.
# Context: {context}
# Answer:"""
# prompt = ChatPromptTemplate.from_template(template)
# combine_docs_chain = create_stuff_documents_chain(model, prompt)
# retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)
# print(retrieval_chain.invoke({"input" : "How do i start my micro-farm"})["answer"])

# rag_chain = (
#     {"context": r,  "question": RunnablePassthrough()} 
#     | prompt 
#     | model
#     | StrOutputParser() 
# )

# rag_assistant = CustomAssistant("""You are a chatbot designed to answer questions about hydroponic farming, general science and chemistry and Babylon Micro-Farms and it's products.
#                         Do not deviate from these topics unless it is to educate the user, and keep in mind most users will be young children. You will also use your given files
#                                              to construct curriculums on hydroponic farming.""", existing_assistant_id="asst_AOk1WPnaXRt3u8yWBWlwY8iu")
# print(rag_assistant.ask_assistant("How to start my micro-farm?"))