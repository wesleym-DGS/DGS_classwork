'''

this is the chat text display class for the messages received from the server

'''

from InGameTextBase import InGameTextBase

class ChatTextDisplay(InGameTextBase):
    def __init__(self, client):

        #passing up the needed vars and also saving the client for later use
        super().__init__(client,(8, 54), 320, 42)
        self.client = client

    def update(self, renderList, dt, typing, mousePos):

        #getting the latest messages from the network thread
        with self.client.networkLock:
            chatMessages = self.client.chatMessages

        if chatMessages:
            lines = [f'{address}: {message}' for address, message in chatMessages]
            renderList.append([self.type, self.font, lines, self.rect])
