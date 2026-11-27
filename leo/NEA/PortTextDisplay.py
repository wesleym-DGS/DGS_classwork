'''

this is the menu text display for the server port

'''

from MenuTextBase import MenuTextBase

class PortTextDisplay(MenuTextBase):
    def __init__(self, client):

        #passing up the needed vars and also saving the client for later use
        super().__init__(client,(450, 25))
        self.client = client

    def update(self, renderList, dt, typing, mousePos):

        #updating the text in the text box and then adding self to the render list
        self.text = self.client.portStr

        if self.text != '':
            renderList.append([self.type, self.font, self.text, self.pos])