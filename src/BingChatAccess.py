from EdgeGPT.EdgeGPT import Chatbot, ConversationStyle
import json, time
import LLMAccess, presaiUtils

class BingChatAccess(LLMAccess):

    def __init__(self, numberOfTries=5):
        self.numberOfTries = numberOfTries
        self.style = ConversationStyle.creative

        # I assume that Bing chat uses GPT-4
        self.possibleModels = [["gpt-4", 4_096]]

        self.chatbots = []

    def chooseModel(self, convIndex, minimumTokens):
        for model, limit in self.possibleModels:
            tokens = presaiUtils.num_tokens_from_messages(self.convs[convIndex], model)
            print(model + " tokens: " + str(tokens) + ", maximum " + str(limit) + " - " + str(minimumTokens))
            if minimumTokens <= limit - tokens:
                return model
        return None

    async def addConv(self):
        tries = 0
        while tries < self.numberOfTries:
            try:
                ## cookies = json.loads(open("cookie.json", encoding="utf-8").read())
                self.chatbots.append(await Chatbot.create())
                self.convs.append([])
                return len(self.convs)-1
            except:
                tries+=1
                time.sleep(1)
        raise ConnectionError("unable to start new chat")

    async def answerPrompt(self, prompt, minimumTokens, convIndex=-1, newConv=False):
        if newConv:
            await self.addConv()
            convIndex = -1
        self.convs[convIndex].append({"role": "user", "content": prompt})

        model = self.chooseModel(convIndex, minimumTokens)

        if model == None:
            raise ValueError("too long chat")
        print("BingChat: Using: " + model)

        tries = 0
        while True:
            try:
                print("BingChat: Sending prompt")
                ret = await self.chatbots[convIndex].ask(prompt=prompt, 
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

        self.convs[convIndex].append({"role": "assistant", "content": ' '.join([ret["text"], ret["sources_text"], *ret["suggestions"]])})        
        
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

class BingChatConversation:
       

