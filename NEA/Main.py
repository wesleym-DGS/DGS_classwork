'''

this is going to be where all the code is brought together and assembled into the main file that gets ran when the player
wants to join the server. The idea is that nothing gets declared in this file and no calculations are done here

'''

#importing all the other content from the other classes so they can be created and used
from Client import Client
from ChatButton import ChatButton
from Render import Render
from Player import Player
from PlayButton import PlayButton
from ChatTextDisplay import ChatTextDisplay
from PortTextDisplay import PortTextDisplay
from PortSetectionButton import PortSelectionButton
from IpTextDisplay import IpTextDisplay
from IpSelectionButton import IpSelectionButton

#creating all objects so they can be used in the main loop
client = Client()
render = Render()
player = Player(client)

#creating the buttons so players can open the game and interact
play_button = PlayButton(client)
chat_button = ChatButton(client)
port_button = PortSelectionButton(client)
ip_button = IpSelectionButton(client)

#setting up the text displays so players can see text
text_chat = ChatTextDisplay(client)
port_display = PortTextDisplay(client)
ip_display = IpTextDisplay(client)

#this is the main game loop where all the main game running operations are done
while client.running:

    #flushing all lists to prevent RAM over use
    client.flush_lists([render.renderList, client.sendToServer])

    #updating all objects in the main list so they can be rendered
    client.update_all(render)

    #checking events to make sure windows close and buttons gets pressed
    client.check_events(player.type)

    #rendering all objects to the screen
    render.render()
