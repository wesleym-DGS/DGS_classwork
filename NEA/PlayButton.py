'''

this is the main play button that starts the game and joins the game

'''

from MenuButtonBase import MenuButtonBase

class PlayButton(MenuButtonBase):
    def __init__(self, client):

        #calling the parent init method and passing the needed parameters in
        super().__init__('PLAY', client, (0,0), 100, 100, (100, 0, 100))

    def pressed(self, client):

        #activating the main game
        client.mode = 'Game'

        client.typing = 'G'