'''

this is the chat text display class for what the local player is typing

'''

from InGameTextBase import InGameTextBase

class SelfChatTextDisplay(InGameTextBase):
    def __init__(self, client):

        #passing up the needed vars and also saving the client for later use
        super().__init__(client,(8, 8), 320, 42)
        self.client = client

    def update(self, renderList, dt, typing, mousePos):

        #showing the current draft straight from the chat input
        self.text = self.client.message

        if self.text != '':
            renderList.append([self.type, self.font, [self.text], self.rect])
