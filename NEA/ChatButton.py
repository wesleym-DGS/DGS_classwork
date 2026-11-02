'''

this is the main button that allows for the player to open the chat mode and start talking to other players

'''

from InGameButtonBase import InGameButtonBase

class ChatButton(InGameButtonBase):
    def __init__(self, client):
        super().__init__('CHAT', client, (0,0), 100, 60, (100, 0, 100))

    def pressed(self):
        print('pressed')