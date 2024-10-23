import langroid as lr
import yaml
config = lr.ChatAgentConfig(
    llm = lr.language_models.OpenAIGPTConfig(
        chat_model=lr.language_models.OpenAIChatModel.GPT4,
    ),
    vecdb=None,
)
with open("swagger.yaml") as f:
    raw_spec = yaml.load(f, Loader=yaml.Loader)
    endpoints = [
        (f"{operation_name.upper()} {route}", docs.get("description"), docs)
        for route, operation in raw_spec["paths"].items()
        for operation_name, docs in operation.items()
        if operation_name in ["get", "post", "patch", "put", "delete"]
    ]
    def reduce_endpoint_docs(docs: dict) -> dict:
        out = {}
        if docs.get("description"):
            out["description"] = docs.get("description")
        if docs.get("parameters"):
            out["parameters"] = [
                parameter
                for parameter in docs.get("parameters", [])
                if parameter.get("required")
            ]
        if "200" in docs["responses"]:
            out["responses"] = docs["responses"]["200"]
        if docs.get("requestBody"):
            out["requestBody"] = docs.get("requestBody")
        return out

    endpoints = [
        (name, description, reduce_endpoint_docs(docs))
        for name, description, docs in endpoints
    ]

endpoint_descriptions = [
            f"{name} {description}" for name, description, _ in endpoints
        ]

planner_agent = lr.ChatAgent(config)
final_endpoints = "- " + "- ".join(endpoint_descriptions)
planner_task = lr.Task(
    planner_agent,
    name="Planner",
    system_message=f"""
        You are a planner that plans a sequence of API calls to assist with user queries against an API.

You should:
1) evaluate whether the user query can be solved by the API documentated below. If no, say why.
2) if yes, generate a plan of API calls and say what they are doing step by step.
3) Never include a DELETE request in your plan.
4) For every endpoint generated, make sure to add a slash at the end of the endpoint.

You should only use API endpoints documented below ("Endpoints you can use:").
Some user queries can be resolved in a single API call, but some will require several API calls.
Once you have your plan, pass it to the Controller.

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
{final_endpoints}
    """
)
planner_agent.enable_message(lr.agent.tools.RecipientTool)
planner_task.run()

class GetTool(lr.agent.ToolMessage):
    request : str = "get"
    purpose : str = "send a GET request and parse the response back based on the query"
    

controller_agent = lr.ChatAgent(config)
controller_task = lr.Task(
    controller_agent,
    name="Controller",
    system_message="""
    
    """
)