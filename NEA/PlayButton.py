'''

this is the main play button that starts the game and joins the game

'''

from ButtonBase import ButtonBase

class PlayButton(ButtonBase):
    def __init__(self, client):
        super().__init__('PLAY', client, (0,0), 100, 100, (100, 0, 100))

    def pressed(self, client):
        client.mode = 'Game'