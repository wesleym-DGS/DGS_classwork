'''

this is the main button that allows for the player to open the chat mode and start talking to other players

'''

from InGameButtonBase import InGameButtonBase

class ChatButton(InGameButtonBase):
    def __init__(self, client):

        #calling the parent init method and passing in the needed parameters
        super().__init__('CHAT', client, (0,100), 100, 60, (100, 0, 100))

    def pressed(self, client):

        #this method will be called to activate the chat talking mode
        print('pressed')

        if not client.typing:

            #changing the client to typing mode so the player doesn't move
            client.typing = True
        else:

            #changing the typing back to False on second press so the player can leave the typing mode
            client.typing = False