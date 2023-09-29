class LLMChatAcess:

    def __init__(self):
        raise NotImplementedError()

    def answerPrompt(self, prompt, LLMChatConv):
        raise NotImplementedError()
    
class LLMChatConversation:

    def __init__(self):
        raise NotImplementedError()
    
    def close(self):
        raise NotImplementedError()