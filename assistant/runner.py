from chatbot import MFAPIChain
from config import Config
from langchain_openai import OpenAI
import os
def main():
    # token = input("What is your token?")
    grade_level = input("Grade level of student: ")
    history_token_length = 2000
    llm = OpenAI( openai_api_key="REMOVED")
    chatbot = MFAPIChain("REMOVED", llm, grade_level, history_token_length, Config())
    while True:
        category = input("Would you like to use the chatbot to interact with your farm's API or general questions? Please input \"API\" or \"General\" ")
        while not (category == "API" or category == "General"):
            category = input("Please either input \"API\" or \"General\"")
        prompt = input("Enter prompt: ")
        output = chatbot.invoke({"content": prompt, 'category' : category})
        print(output['output'], output['response_time'])

def test_times(chatbot):
    response_times = []
    queries = [
        'What is hydroponic farming',
        'How do plants use photosynthesis',
        'how does babylon use hydroponic farming',
        'Why do plants need sunlight to grow',
        'What plants are the easiest to grow',
        'How can i grow a plant in a babylon micro-farm',
        'How do i set up my micro-farm',
        'How is hydroponic farming different from regular farming',
        'Who created farming',
        'What does a plant need to grow',
        'What plants can grow in the desert',
    ]
    for query in queries:
        output = chatbot.invoke({"content" : query, 'category' : 'General'})
        response_times.append(output['response_time'])
    print(response_times)
if __name__ == '__main__':
    main()