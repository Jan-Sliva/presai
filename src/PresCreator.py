from BingChatAccess import BingChatAccess
from ChatGPTAccess import ChatGPTAccess
import json

def presCreator(options):
    
    with open('src/prompts.json') as f:
        prompts = json.load(f)

    first = prompts["topics"].format(options["len"], options["adj"], options["top"])

    chatGPT = ChatGPTAccess()

    answer = chatGPT.answerPropt(first, 500, newConv=True)

    topics  = json.loads(answer)
    topics = topics[list(topics.keys())[0]]
    print(topics)



options = {"len" : 20, "adj" : "geographical", "top" : "Central asia"}

presCreator(options)