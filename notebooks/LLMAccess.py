class LLMAcess:

    def __init__(self):
        self.convs = []

    def addConv(self):
        raise NotImplementedError()
    
    def answerPropt(self, prompt, convIndex=-1, newConv=False):
        raise NotImplementedError()
    
