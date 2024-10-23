# flake8: noqa
"""All prompts used in various places"""
from langchain_core.prompts.prompt import PromptTemplate
from langchain.prompts import ChatPromptTemplate
from langchain.prompts.few_shot import FewShotPromptTemplate
"""Custom Prompt Templates"""

STARTING_PROMPT_TEMPLATE = """
You are a large language model/chatbot that is trained to answer queries and commands that
users of the Babylon Micro Farms Galleri Farm will send you. Most, if not all of the prompts that come to you will
be questions about a specific group of farms that the user owns. When the user sends their first prompt
about the status of their farm or in your memory, ask for the user's API token first, which will be needed to access user-specific information about the farms.
"""

STARTING_PROMPT = PromptTemplate(input_variables=[], template=STARTING_PROMPT_TEMPLATE)

examples = [
    {
        "question": "Change the water level in my farm",
        "command" : "PATCH",
    },
    {
        "question": "What is the status of my farm",
        "command": "GET",
    },
    {
        "question": "What are the crops in my farm",
        "command": "GET",
    },
    {
        "question": "Set the auto_farmer of my farm to on",
        "command": "PATCH",   
    },
    {
        "question" : "Set the water_valve of my farm to on",
        "command": "PATCH",
    }, 
    {
        "question": "What are the zones of my farm?",
        "command": "GET",
    }
    ]

# Get the prompt and the farm name from the user, if they ask for multiple farms return all of them
API_URL_PROMPT_TEMPLATE = """
Question: {question}
{command}
"""

template = PromptTemplate(
    input_variables=[
        "question",
        "command",
    ],
    template=API_URL_PROMPT_TEMPLATE
)

API_URL_PROMPT = FewShotPromptTemplate(
    examples=examples,
    example_prompt=template,
    prefix="""You are going to return something called 'command', which will either be "GET" or "PATCH". 
            If the prompt is asking for information, set command to "GET", if the prompt seems like 
            it's asking to change something, set command to "PATCH".""",
    suffix="""Prompt : {input}""",
    input_variables=["input"]
    )

first_level_examples = [
    {
        "question": "Change the water level in my farm",
        "command" : "OPERATIONS",
    },
    {
        "question": "What is the status of my farm",
        "command": "OPERATIONS",
    },
    {
        "question": "What are the crops in my farm",
        "command": "PACKS",
    },
    {
        "question": "Set the auto_farmer of my farm to on",
        "command": "OPERATIONS",   
    },
    {
        "question" : "What are the packs in my farm right now",
        "command" : "PACKS",
    },
    {
        "question" : "Do I need to do any actions today?",
        "command" : "PACKS",
    },
    {
        "question" : "Do I need to harvest or transplant today?",
        "command" : "PACKS",
    },
    {
        "question" : "Activate the ec_pump",
        "command" : "OPERATIONS",
    },
    {
        "question" : "Mark that I cleaned the farm today",
        "command" : "PACKS",
    },
    {
        "question" : "Transplant these packs to the next zone",
        "command" : "PACKS",
    },
    {
        "question" : "Change the harvest date to today in _DEV_SPOOKY_FLOWER",
        "command" : "PACKS",
    },
    
]
FIRST_LEVEL_TEMPLATE = """
Question: {question}
Category: {command}
"""

first_level_template = PromptTemplate(
    input_variables=[
        "question",
        "command",
    ],
    template=API_URL_PROMPT_TEMPLATE
)
FIRST_LEVEL_PROMPT = FewShotPromptTemplate(
    examples=first_level_examples,
    example_prompt=first_level_template,
    prefix="""You are a classifier that takes in a prompt and uses your knowledge to determine whether the prompt
    is asking about the OPERATIONS of the farm and its controls, or the PACKS in its farm, i.e the plants. If the
    prompt seems to be about the farm and its properties, set command to "OPERATIONS", if it's instead about 
    the plants in the farm, set command to "PACKS". If you don't think it's in either category, return "NONE".
    
    Note: Although it may seem that some commands related to cleaning the farm may be related to the operations of the farm,
    these should be put considered as a "PACKS".""",
    suffix="Prompt : {input}",
    input_variables=["input"]
)

CHANGE_PROMPT_TEMPLATE = """
Look at the prompt {question}. The prompt is asking to change a property/properties, and an amount should be provided
for each property. Return a list of the properties along with their respective amounts. If an amount isn't listed, return
"NO AMOUNT".
Ansewr List:
"""

CHANGE_PROMPT = PromptTemplate(
    input_variables=[
        "question",
    ],
    template=CHANGE_PROMPT_TEMPLATE
)
API_RESPONSE_PROMPT_TEMPLATE = (
 """ 

Here is the response from the API:

{api_response}


If the response is not in JSON, get the JSON version of the url. IT will contain a lot of information regarding the
farm's operational status. Parse and look through the JSON to find the attribute that matches most similar to what
was asked in {question}.
Here are some guidelines on the JSON object:
If {category} is OPERATIONS:
'name' : The farm's name
version: The farm's version
farm_type : the type of the farm
customer: Farm's customer
operators: Farm's operators
active: If the farm is active and working
auto_farmer : If the farm's autofarmer is on
light: Status of the farm's light
pump : Status of the farm's pump
fan: Status of the farm's fan
water_valve : Status of the farm's water_valve
chiller: status of the farm's chiller
fill_n_does : status of the farm's fill_n_does
activate_ec_pump : Whether the ec pump is on
activate_ph_pump : Whether the ph pump is on
activate_cycling_pump : Whether the cycling pump is on
water_conditioner_pump : Whether the water conditioner pump is on
num_zones : Number of farming zones

Answer to User's Question:"""
)

API_RESPONSE_PROMPT = PromptTemplate(
    input_variables=["api_response", "question", "category"],
    template=API_RESPONSE_PROMPT_TEMPLATE,
)

template = """You are an educational chatbot that is designed to answer questions 
about hydroponic farming, science and Babylon Micro-farms. Your users will mainly be young students.
Use the following pieces of retrieved context to answer the question.
Context: {context}
Answer:"""
RAG_PROMPT = ChatPromptTemplate.from_template(template)




PACKS_CLASSIFIER_PROMPT = PromptTemplate(
    template="""
    You are a classifier that will take in an user prompt, {query} and decide whether the natural language is one of two options:
    1) the user just completed something, or is asking to change something in the farm
    2) the user is asking about some information in the farm or its plants
    If it is 1, return category as "COMMAND". If it is 2, return category as "GET".

    Category:
    """,
    input_variables=["query"],
)

PARSING_PACKS_PROMPT = PromptTemplate(
    template="""Here is a list of JSON object responses containing information about plant packs in the micro-farm : {response}
    Here is a detailed list about what each of the attributes are explaining in the 'crop_info' object.

    crop_name : type of the crop
    common_name : the name the crop usually goes by
    status: whether the plant is planted, transplanted, harvested, etc.
    seed_date : when the plant was seeded, None if not seeded
    plant_date : when the plant was planted, None if not planted
    transplant_date: when the plant was transplanted, None if not transplanted
    target_transplant_date : when the plant should be transplanted
    start_harvest_date : when the plant should start to be harvested
    end_harvest_date : the target date to end harvesting for the plant
    farm_sn : serial number of the farm the plant is in

    The activities object contains different objects with information about events and the most recent date it happened and the next time it happened.

    Here are some rules when designing an answer:
    1) Construct the answer using only the information provided and the original user prompt, {query}
    2) The user may give information about the time periods in {time_tags}. 


    3) Do not mention any of your thoughts, logic or temporal expressions in the output.
    4) If you are going to return a mixture of activities and items in the farm, make sure to separate them with their appropriate category names.
    5) Only include things in the query in your answer, do not include extraneous information.

    Output:
    """,
    input_variables=["query", "response", "time_tags"]
)


PACKS_POST_PROMPT = PromptTemplate(
    template="""
        You are a classifier agent that will take in an user query, {query}, and decide if the prompt is most related to:
        1) Harvest
        2) Transplant
        3) Clean
        4) Refill_EC
        5) Refill_PH
    
    Return one of these options as output.
    Output:
    """,
    input_variables=["query"]
)

API_ORCHESTRATOR_PROMPT = """You are an agent that assists with user queries against API, things like querying information or creating resources.
Some user queries can be resolved in a single API call, particularly if you can find appropriate params from the OpenAPI spec; though some require several API calls.
You should always plan your API calls first, and then execute the plan second.
If the plan includes a DELETE call, be sure to ask the User for authorization first unless the User has specifically asked to delete something.
You should never return information without executing the api_controller tool.


Here are the tools to plan and execute API requests: {tools}


Starting below, you should follow this format:

User query: the query a User wants help with related to the API
Thought: you should always think about what to do
Action: the action to take, should be one of the tools [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I am finished executing a plan and have the information the user asked for or the data the user asked to create
Final Answer: the final output from executing the plan


Example:
User query: can you add some trendy stuff to my shopping cart.
Thought: I should plan API calls first.
Action: api_planner
Action Input: I need to find the right API calls to add trendy items to the users shopping cart
Observation: 1) GET /items/ with params 'trending' is 'True' to get trending item ids
2) GET /user/ to get user
3) POST /cart/ to post the trending items to the user's cart
Thought: I'm ready to execute the API calls.
Action: api_controller
Action Input: 1) GET /items params 'trending' is 'True' to get trending item ids
2) GET /user to get user
3) POST /cart to post the trending items to the user's cart
...

Begin!

User query: {input}
Thought: I should generate a plan to help with this query and then copy that plan exactly to the controller.
{agent_scratchpad}"""

API_CONTROLLER_PROMPT = """You are an agent that gets a sequence of API calls and given their documentation, should execute them and return the final response.
If you cannot complete them and run into issues, you should explain the issue. If you're unable to resolve an API call, you can retry the API call. When interacting with API objects, you should extract ids for inputs to other API calls but ids and names for outputs returned to the User.


Here is documentation on the API:
Base url: {api_url}
Endpoints:
{api_docs}


Here are tools to execute requests against the API: {tool_descriptions}


Starting below, you should follow this format:

Plan: the plan of API calls to execute
Thought: you should always think about what to do
Action: the action to take, should be one of the tools [{tool_names}]
Action Input: the input to the action
Observation: the output of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I am finished executing the plan (or, I cannot finish executing the plan without knowing some other information.)
Final Answer: the final output from executing the plan or missing information I'd need to re-plan correctly.


Begin!

Plan: {input}
Thought:
{agent_scratchpad}
"""

API_PLANNER_PROMPT = """You are a planner that plans a sequence of API calls to assist with user queries against an API.

You should:
1) evaluate whether the user query can be solved by the API documentated below. If no, say why.
2) if yes, generate a plan of API calls and say what they are doing step by step.
3) Never include a DELETE request in your plan.
4) For every endpoint generated, make sure to add a slash at the end of the endpoint.
You should only use API endpoints documented below ("Endpoints you can use:").
You can only use the DELETE tool if the User has specifically asked to delete something. Otherwise, you should return a request authorization from the User first.
Some user queries can be resolved in a single API call, but some will require several API calls.
The plan will be passed to an API controller that can format it into web requests and return the responses.
If a farm's serial num is provided, make sure to only use endpoints that explicitly have the serial_num endpoints, since using the serial num means we are specific to one farm.

----

Here are some examples:

Fake endpoints for examples:
GET /api/farms/ to get a list of the current farms belonging to a user
GET /api/farminfo/?serial_num=<serial_num>/ to get all the info about a certain farm
PUT /api/farms/serial_num/ to update properties about the farm
GET /api/packstatus/ to get a list of all the packs the user has
GET /api/transplant/ to get a list of all the packs that need to be transplanted
GET /api/harvest/ to get a list of all the packs that need to be harvested
GET /api/germinate/ to get a list of all the packs that need to be germinated

User query: tell me a joke
Plan: Sorry, this API's domain is shopping, not comedy.

User query: Do I need to take any actions today?
Plan: 1. Get /api/transplant/ to get a list of all packs 

User query: Turn the water valve off in farm serial_num 1
Plan: 1. PUT /api/farms/serial_num/ with serial_num 1 with the parameters water_valve : 'false' to turn off water_valve

User query: What packs are ready for harvesting?
Plan: 1. GET /api/harvest/ to get a list of all packs ready for harvesting

User query: Do I have any packs that need to be germinated or transplanted
Plan: 1. GET /api/germinate/ to get all the packs ready to be germinated
2. GET /api/transplant/ to get all the packs ready to be transplanted


----

Here are endpoints you can use. Do not reference any of the endpoints above.

{endpoints}

----
User query: {query}
Plan:"""
