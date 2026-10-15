'''
this is going to be where all the code is brought together and assembled into the main file that gets ran when the player
wants to join the server
'''

from Client import Client
from Render import Render
from Player import Player

client = Client()
render = Render()
player = Player(client)

while client.running:
    client.flush_lists([render.render])
    client.update_all(render)
