import asyncio, json
from EdgeGPT.EdgeGPT import Chatbot, ConversationStyle
import pprint 
pp = pprint.PrettyPrinter(indent=1)


def getSources(resp):
    ret = []
    lines = resp.split("\n")
    for line in lines:
        words = line.split(" ")
        if (len(words) < 2) or (len(words[0]) == 0) or (words[0][0] != "["):
            return ret
        ret.append(words[1])


async def main():
    cookies = json.loads(open("./bing_cookies_1.json", encoding="utf-8").read())
    bot = await Chatbot.create() # Passing cookies is optional

    while True:
        question = input("Question: ")
        if question == "!end":
            break
        ret = await bot.ask(prompt=question, conversation_style=ConversationStyle.creative, simplify_response=True)

        pp.pprint(ret)

        # for i in range(len(ret['item']['messages'][1]['adaptiveCards'][0]['body'])):
        #     cont = False
        #     try:
        #         resp = ret['item']['messages'][1]['adaptiveCards'][0]['body'][i]['text']
        #     except:
        #         cont = True
        #     if not cont:
        #         break

        print(ret['text'])
        print(getSources(ret['sources']))
        print((ret['messages_left'], ret['max_messages']))
        print(ret['suggestions'])


    await bot.close()

if __name__ == "__main__":
    asyncio.run(main())
