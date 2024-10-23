# Brainstorming

## Different ways to develop a chatbot

Need a pipeline that can take a document, usually needs to be a PDF, but could look at Google Docs integration, and then feed it into the LLM/Chatbot.

Look at embeddings + vector database + OpenAI cookbooks. LangChain and EmbedChain are good existing frameworks for this.

Links:
https://community.openai.com/t/fine-tuning-with-help-of-massive-amount-of-documents/84195/8
https://community.openai.com/t/seeking-advice-uploading-large-pdfs-for-analysis-with-gpt-3-api/325053
https://github.com/openai/openai-cookbook/blob/main/examples/Question_answering_using_embeddings.ipynb

Structure: eventually have an App that is constantly running, or saved, and put a dropbox where more files can be fed into it continously, and put an interface where users can talk with the bot

Need a cloud vector database to store embeddings: Weaviate
Hoster/Provider: either aws instance

Structure: backend: Flask server hosten on AWS + Chroma

https://fastapi.tiangolo.com/deployment/docker/ - for deploying with FastAPI
Webcrawler on the babylon micro-farms website + other sources
Webcrawler doesn't even need to scrape, can put in HTML websites into embedchain, as well as google docs
Use Cosine Similarity to restrict what prompts will be answered by chatbot, also find a way to leverage 
it's more powerful knowledge on the web