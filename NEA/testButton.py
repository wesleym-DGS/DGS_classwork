'''

this is a simple test button to make sure the other code works

'''

from Button import Button

class testButton(Button):
    def __init__(self, client):
        super().__init__('PLAY', client, (0,0), 100, 100, (100, 0, 100))

    def pressed(self, client):
        client.mode = 'Game'
        print('test')