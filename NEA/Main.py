'''
this is going to be where all the code is brought together and assembled into the main file that gets ran when the player
wants to join the server. The idea is that nothing gets declared in this file and no calculations are done here
'''

#importing all the other content from the other classes so they can be created and used
from Client import Client
from Render import Render
from Player import Player

#creating all objects so they can be used in the main loop
client = Client()
render = Render()
player = Player(client)

#this is the main game loop where all the main game running operations are done
while client.running:

    #flushing all lists to prevent RAM over use
    client.flush_lists([render.renderList])

    #updating all objects in the main list so they can be rendered
    client.update_all(render)

    #checking events to make sure windows close and buttons gets pressed
    client.check_events()

    #rendering all objects to the screen
    render.render()
