# Babylon Micro-Farms Chatbot and API Tool

This repository contains a Babylon Micro-Farms intern and feasibility project on a multipurpose pipeline that can answer both general questions on science and hydroponic farming as well as query the Babylon API through natural language commands. On the RAG side, most of the code is built on top of Langchain's Chains and Prompt Engineering. The API Tool was built from scratch, and specifically engineered for the Babylon API.

## To Reproduce
Install all needed packages in the requirements.txt at the root of the repo. Ensure `streamlit` is installed, then run the below commands from the repo to start a simple Streamlit app with the chatbot embedded.
```console
cd assistant
streamlit run streamlit_runner.py
```
To run the terminal version:
```console
cd assistant
python runner.py
```

## Config and Codebase Info
`/assistant` will contains all of the working codebase, ignore demo and scrap as they contain previous iterations and quick demos. The `chatbot.py` file contains the combined chatbot and API tool, and all the different tools/components are in the `utils` folder.