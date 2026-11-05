'''

this is the main chat text display class which will display the full text chat

'''

from InGameTextBase import InGameTextBase

class ChatTextDisplay(InGameTextBase):
    def __init__(self, client):
        super().__init__(client)
        self.client = client

    def update(self, renderList, dt, typing):

        #updating the text in the text box and then adding self to the render list
        self.text = self.client.message
        if self.text != '':
            renderList.append([self.type, self.font, self.text, self.pos])