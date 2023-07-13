import LLMAccess, presaiUtils

class ChatGPTlike(LLMAccess.LLMAcess):

    def __init__(self, numberOfTries=5):
        super().__init__()
        self.numberOfTries = numberOfTries

    def chooseModel(self, convIndex, minimumTokens):
        for model, limit in self.possibleModels:
            tokens = presaiUtils.num_tokens_from_messages(self.convs[convIndex], model)
            print("Tokens: " + str(tokens))
            if minimumTokens <= limit - tokens:
                return model
        return None

    