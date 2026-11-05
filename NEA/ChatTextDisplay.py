'''

this is the main chat text display class which will display the full text chat

'''

from InGameTextBase import InGameTextBase

class ChatTextDisplay(InGameTextBase):
    def __init__(self, client):
        #passing up the needed vars and also saving the client for later use
        super().__init__(client,(10,10))
        self.client_msg = client.message

    def update(self, renderList, dt, typing):

        #updating the text in the text box and then adding self to the render list
        self.text = self.client_msg
        if self.text != '':
            renderList.append([self.type, self.font, self.text, self.pos])