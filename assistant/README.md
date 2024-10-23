# Flow: 
User Prompt -> Assistant (finetuned) -> Formulated API Call -> LLM -> API Request -> API Response -> LLM -> Assistant -> User

Assistant will be OpenAI vanilla, will input a prompt into the custom LLMChain with custom tools, and then spit it back to the user after refinement through LLM again to

Stuff to fix:
Farm name processing is still bad, might need to use regex
Patch requests aren't working, try post

// Add functionalities:

TO-do : Add functionality to turn off auto-farmer when on and changing attributes of farm
Also need to find a way for multiple attributes
Create a custom documentation the bot to go off when reading from the get request
Add a chat completions API bot to check all answers before they leave

https://community.openai.com/t/questions-about-assistant-threads/485239/3
https://community.openai.com/t/switching-from-assistants-api-to-chat-completion/663018/2

API Assistant side is not working as well - after it's fixed, look at packs
Demo RAG assistant with curriculum and user manual  - propose alternate architectures, think of sending documents as context, look at how grade level is changing

document searching over curriculum and existing manual
make an excel table over the response times for different configurations for demo


try out keeping context and conversation history by keeping running list of messages
Ways to improve retrieval : SPLADE and Hybrid search, will be much slower than using retrieval but will be more accurate

Looking at the OpenAI Assistant Streaming Option
pack/status update on the different packs, hit the pack endpoint
when to transplant and when to harvest, germinate time and growth time

Architecture Diagram for Demo

Put clean_date into Operations, since that is activities
for plant patch only have the case for harvest transplant and be able to extract the packs UUID
