'''

this is the main play button that starts the game and joins the game

'''

from MenuButtonBase import MenuButtonBase

class PlayButton(MenuButtonBase):
    def __init__(self, client):
        super().__init__('PLAY', client, (0,0), 100, 100, (100, 0, 100))

    def pressed(self, client):
        client.mode = 'Game'