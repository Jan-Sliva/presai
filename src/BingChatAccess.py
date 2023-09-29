from EdgeGPT.EdgeGPT import Chatbot, ConversationStyle
import json, time
import LLMChatAccess

class BingChatAccess(LLMChatAccess.LLMChatAcess):

    def __init__(self, style = ConversationStyle.creative, numberOfTries=5):
        self.numberOfTries = numberOfTries
        self.style = style

    async def answerPrompt(self, prompt, bingChatConv):
        if bingChatConv.isCLosed:
            raise ConnectionError("BingChat conversation os closed")
        
        bingChatConv.conv.append({"role": "user", "content": prompt})

        tries = 0
        while True:
            try:
                print("BingChat: Sending prompt")
                ret = await bingChatConv.chatbot.ask(prompt=prompt, 
                            conversation_style=self.style, 
                            simplify_response=True)
                break
            except Exception as e:
                print(e)
                tries+=1
                if tries >= self.numberOfTries:
                    raise ConnectionError("unable to get chat response")
                print("BingChat: The try wasn't succesful, trying again")
                time.sleep(1)

        bingChatConv.conv.append({"role": "assistant", "content": ' '.join([ret["text"], ret["sources_text"], *ret["suggestions"]])})        
        
        return {'text' : ret['text'], 'suggestions' : ret['suggestions'], 'messages_left' : ret['messages_left'],
                'max_messages' : ret['max_messages'], 'sources' : BingChatAccess.getSources(ret['sources'])}
    
    @staticmethod
    def getSources(resp):
        ret = []
        lines = resp.split("\n")
        for line in lines:
            words = line.split(" ")
            if (len(words) < 2) or (len(words[0]) == 0) or (words[0][0] != "["):
                return ret
            ret.append(words[1])

class BingChatConversation(LLMChatAccess.LLMChatConversation):
       
    async def __init__(self, numberOfTries=5, cookiesLocation = None) -> None:
        self.conv = []
        self.isClosed = False

        tries = 0
        while tries < numberOfTries:
            try:
                cookies = None
                if cookiesLocation:
                    cookies = json.loads(open(cookiesLocation, encoding="utf-8").read())

                self.chatbot = await Chatbot.create(cookies=cookies)
                break
            except Exception as e:
                print(e)

                tries+=1
                if tries >= numberOfTries:
                    raise ConnectionError("unable to start new chat")
                time.sleep(1)
    
    def close(self):
        self.chatbot.close()
        self.isClosed = True


