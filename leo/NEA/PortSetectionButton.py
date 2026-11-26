'''

this is the main play button that starts the game and joins the game

'''

from MenuButtonBase import MenuButtonBase

class PortSelectionButton(MenuButtonBase):
    def __init__(self, client):

        #calling the parent init method and passing the needed parameters in
        super().__init__('PORT', client, (350,0), 100, 50, (100, 0, 100))

    def pressed(self, client):
        if client.typing != 'P':

            # changing the client to typing mode so the player doesn't move
            client.typing = 'P'
        else:

            # changing the typing back to Game on second press so the player can leave the typing mode
            client.typing = 'G'
