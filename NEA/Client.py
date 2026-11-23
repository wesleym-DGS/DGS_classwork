
'''
this class contains the high level game logic and also is used to direct the other classes to where they need to be used
the main point of this class is to act as a director and high level manager, so it doesn't use any pygame vectors or pygame logic
as that is handled by each class via their own internal methods
'''

import json
import socket
import threading
import pygame

from DrawElipse import DrawElipse
from DrawRect import DrawRect
from DrawnObjectBase import DrawnObjectBase


class Client:
    def __init__(self, host='127.0.0.1', port=8080):

        #this is going to decide weather or not the game is in the room mode or in main menu mode
        self.mode = 'Menu'

        #the main list is going to store all objects in the game that can be modified by the client
        self.mainList = []

        self.sendToServer = []

        self.objectBeingDrawn = None

        #main on/off state for the game so it knows when the player has quit
        self.running = True

        #making a time delta so all objects and moving things can move per frame
        self.dt = 60

        #adding a time clock so the time delta can be updated correctly
        self.clock = pygame.time.Clock()

        #this dictates whether key inputs are for typing or movement
        self.typing = 'G'

        #this is the main variable for when the player is drawing on the screen
        self.drawing = False

        #this is the current chat message being typed
        self.message = ''

        #this is the game state shared with the server
        self.host = host
        self.port = port
        self.portStr = str(self.port)
        self.outgoingState = [[], '']
        self.remoteObjects = []
        self.chatMessages = []
        self.networkConnected = False

        #keeping network operations away from the pygame main loop
        self.networkLock = threading.Lock()
        self.networkStop = threading.Event()

        self.networkThread = threading.Thread(target=self.network_loop,daemon=True)
        self.networkThread.start()

    def update_all(self, render):

        #updating the time delta so the players movement doesn't change with frame rate
        self.dt = self.clock.tick(60) / 1000
        gameText = []

        #going though all items in the main list and telling them to update themselves
        for item in self.mainList:

            if self.mode == 'Menu' and item.type in ('B', 'TDM'):
                item.update(render.renderList,self.dt,self.typing,pygame.mouse.get_pos())

            elif self.mode == 'Game' and item.type in ('E', 'R'):
                item.update(self.sendToServer,self.dt,self.typing,pygame.mouse.get_pos())

            elif self.mode == 'Game' and item.type in ('DRAW', 'CB'):
                item.update(render.renderList,self.dt,self.typing,pygame.mouse.get_pos())

            elif self.mode == 'Game' and item.type == 'TD':
                item.update(gameText,self.dt,self.typing,pygame.mouse.get_pos())

        if self.mode == 'Game':
            #saving a fresh snapshot before Main clears sendToServer next frame
            with self.networkLock:
                self.outgoingState = [[item.copy() for item in self.sendToServer], self.message]
                remoteObjects = self.remoteObjects

            #rendering the chat after the game objects so it stays visible
            render.renderList.extend(self.sendToServer)
            render.renderList.extend(remoteObjects)
            render.renderList.extend(gameText)

        else:
            #the server should not show this player while they are in the menu
            with self.networkLock:
                self.outgoingState = [[], '']

        #only using valid port numbers for network connections
        if self.portStr.isascii() and self.portStr.isdecimal() and len(self.portStr) <= 5:
            newPort = int(self.portStr)

            if 1 <= newPort <= 65535:
                self.port = newPort

    def network_loop(self):

        #this method exchanges game objects and chat messages with the server
        connectionErrorReported = False

        #keeping the thread alive even when the player is still in the menu
        while not self.networkStop.is_set():

            #only connecting once the player has pressed PLAY
            if self.mode != 'Game':
                self.networkStop.wait(0.1)
                continue

            try:
                #trying to connect without freezing the pygame window
                with socket.create_connection((self.host, self.port),timeout=2) as conn:

                    conn.settimeout(5)

                    #using a persistent reader to receive one complete JSON line
                    with conn.makefile('rb') as reader:

                        self.networkConnected = True
                        connectionErrorReported = False

                        print('connected to server')

                        #the connection stays open while the player remains in game
                        while not self.networkStop.is_set() and self.mode == 'Game':

                            #getting the latest local objects and message from the main thread
                            with self.networkLock:
                                outgoingState = self.outgoingState

                            #sending one newline-terminated JSON list
                            payload = json.dumps(outgoingState).encode('utf-8') + b'\n'
                            conn.sendall(payload)

                            #the server replies with remote objects and current messages
                            receivedData = reader.readline(1_000_001)

                            if not receivedData:
                                raise ConnectionError('server closed connection')

                            if len(receivedData) > 1_000_000 or not receivedData.endswith(b'\n'):
                                raise ValueError('invalid server message')

                            receivedList = json.loads(receivedData)

                            if not isinstance(receivedList, list) or len(receivedList) != 2:
                                raise ValueError('invalid server update')

                            remoteObjects, chatMessages = receivedList

                            #checking the basic format before sending it to the renderer
                            if not isinstance(remoteObjects, list) or any(
                                not isinstance(item, list) or len(item) != 6 or
                                item[0] not in ('E', 'R') or
                                not isinstance(item[1], list) or len(item[1]) != 3
                                for item in remoteObjects
                            ):
                                raise ValueError('invalid server object list')

                            if not isinstance(chatMessages, list) or any(
                                not isinstance(item, list) or len(item) != 2 or
                                not all(isinstance(part, str) and part.isprintable() for part in item)
                                for item in chatMessages
                            ):
                                raise ValueError('invalid server chat list')

                            #the pygame loop will read these lists on its next frame
                            with self.networkLock:
                                self.remoteObjects = remoteObjects
                                self.chatMessages = chatMessages

                            #aiming for up to roughly 60 updates per second
                            self.networkStop.wait(1 / 60)

            except (OSError, ValueError, TypeError, UnicodeError) as error:

                if not connectionErrorReported and not self.networkStop.is_set():
                    print(f'network unavailable: {error}')
                    connectionErrorReported = True

            finally:

                self.networkConnected = False

                #clearing remote players and chat when the connection is closed
                with self.networkLock:
                    self.remoteObjects = []
                    self.chatMessages = []

            #reconnecting after the server comes back online
            if self.mode == 'Game':
                self.networkStop.wait(1)

    def flush_lists(self, lists):

        #here I am flushing all the lists that need to be flushed to prevent rapid RAM filling
        for item in lists:
            item.clear()

    def check_events(self, playerType):

        #doing the normal checks for a pygame instance to make sure it can be closed
        for event in pygame.event.get():

            #searching though every event that has happened
            if event.type == pygame.QUIT:
                self.running = False
                self.networkStop.set()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:

                    #checking whether the player has clicked a button
                    buttonPressed = False

                    for item in self.mainList:

                        if item.type in ('B', 'CB') and item.rect.collidepoint(event.pos):

                            #only allowing buttons in the current mode to be pressed
                            if ((self.mode == 'Menu' and item.type == 'B') or (self.mode == 'Game' and item.type == 'CB')):
                                item.pressed(self)
                                buttonPressed = True
                                break

                    #only drawing objects when the player is in game mode
                    if not buttonPressed and self.mode == 'Game':

                        if not self.drawing:

                            if playerType == 'E':
                                self.objectBeingDrawn = DrawElipse(event.pos,event.pos,self)

                            elif playerType == 'R':
                                self.objectBeingDrawn = DrawRect(event.pos,event.pos,self)

                            self.drawing = True

                        else:

                            newObject = DrawnObjectBase(self,self.objectBeingDrawn.pos,self.objectBeingDrawn.typeS,self.objectBeingDrawn.colour,self.objectBeingDrawn.rect.copy())

                            #removing the temporary drawing object
                            self.mainList.remove(self.objectBeingDrawn)

                            self.objectBeingDrawn = None
                            self.drawing = False

            if event.type == pygame.KEYDOWN and self.drawing:

                #checking if the player wants to cancel the current drawing
                if event.key == pygame.K_ESCAPE:

                    #removing the temporary object from the main list
                    if self.objectBeingDrawn is not None:
                        self.mainList.remove(self.objectBeingDrawn)

                    #clearing the object reference and drawing state
                    self.objectBeingDrawn = None
                    self.drawing = False

            if event.type == pygame.KEYDOWN and self.typing == 'C':

                #checking the chat input
                if event.key == pygame.K_BACKSPACE:
                    self.message = self.message[:-1]

                elif event.key == pygame.K_RETURN:
                    self.message = ''
                    self.typing = 'G'

                elif event.unicode.isprintable():
                    self.message = (self.message + event.unicode)[:500]

            if event.type == pygame.KEYDOWN and self.typing == 'P':

                #allowing the player to change the server port
                if event.key == pygame.K_BACKSPACE:
                    self.portStr = self.portStr[:-1]

                elif event.key == pygame.K_RETURN:
                    self.typing = 'G'

                elif (event.unicode in '0123456789' and event.unicode and len(self.portStr) < 5):
                    self.portStr += event.unicode

            if event.type == pygame.KEYDOWN and self.typing == 'IP':

                #allowing the player to change the server IP address
                if event.key == pygame.K_BACKSPACE:
                    self.host = self.host[:-1]

                elif event.key == pygame.K_RETURN:
                    self.typing = 'G'

                elif event.unicode.isprintable() and not event.unicode.isspace():
                    if len(self.host) < 253:
                        self.host += event.unicode
