from ChatGPTlike import ChatGPTlike
import openai, tiktoken, time, presaiUtils

class ChatGPTAccess(ChatGPTlike):

    def __init__(self, numberOfTries=5):
        super().__init__(numberOfTries)
        with open(".ChatGPTtoken", "r") as f:
            openai.api_key = f.read()

        # see https://platform.openai.com/docs/models/gpt-3-5
        self.possibleModels = [["gpt-3.5-turbo", 4_096], ["gpt-3.5-turbo-16k", 16_384]]

    def addConv(self):
        self.convs.append([])
        return len(self.convs)-1
    
    def answerPropt(self, prompt, minimumTokens, convIndex=-1, newConv=False, temp=0.5, model=None):
        if newConv:
            self.addConv()
            convIndex = -1
        self.convs[convIndex].append({"role": "user", "content": prompt})

        if model == None:
            model = self.chooseModelAndShorten(convIndex, minimumTokens)
        print("ChatGPT: Using: " + model)

        tries = 0
        while True:
            try:
                print("ChatGPT: Sending prompt")
                chat = openai.ChatCompletion.create(
                    model=model, messages=self.convs[convIndex], temperature=temp
                )
                break
            except Exception as e:
                print(e)
                tries+=1
                if tries >= self.numberOfTries:
                    raise ConnectionError("unable to get chat response")
                print("ChatGPT: The try wasn't succesful, trying again")
                time.sleep(1)
        
        reply = chat.choices[0].message.content
        self.convs[convIndex].append({"role": "assistant", "content": reply})

        return reply
    
    def chooseModelAndShorten(self, convIndex, minimumTokens):
        ret = self.chooseModel(convIndex, minimumTokens)
        while ret == None:
            del self.convs[convIndex][0]
            ret = self.chooseModel(convIndex, minimumTokens)
        
        if len(self.convs[convIndex]) == 0:
            raise Exception("Too long prompt")
        
        return ret

    