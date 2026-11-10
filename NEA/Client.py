
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
from DrawnObjectBase import DrawnObjectBase

class Client:
    def __init__(self, host='127.0.0.1', port=8080):

        #this is going to decide weather or not the game is in the room mode or in main menu mode
        self.mode = 'Menu'

        #the main list is going to store all objects in the game that can be modified by the client, e.g the player and all created objects
        self.mainList = []

        self.sendToServer = []

        self.objectBeingDrawn = None

        #main on/off state for the game so it knows when the player has quit
        self.running = True

        #making a time delta so all objects and moving things can move per frame
        self.dt = 60

        #adding a time clock so the time delta can be updated correctly
        self.clock = pygame.time.Clock()

        #this dictates whether key inputs for typing out a message or for movement
        self.typing = 'C'

        #this is the main variable for when the player is drawing on the screen
        self.drawing = False

        #this is the message, and it gets cleared when it is sent
        self.message = ''

        #these are the object lists shared with the server
        self.host = host
        self.port = port
        self.portStr = str(self.port)
        self.outgoingObjects = []
        self.remoteObjects = []
        self.networkConnected = False

        #keeping network operations away from the pygame main loop
        self.networkLock = threading.Lock()
        self.networkStop = threading.Event()
        self.networkThread = threading.Thread(target=self.network_loop, daemon=True)
        self.networkThread.start()

    def update_all(self, render):

        #updating the time delta so the players movement doesn't change with frame rate
        self.dt = self.clock.tick(60)/1000

        #going though all items in the main list and telling them to update themselves so they can be sent to the server or sent directly to the render list
        for item in self.mainList:
            if self.mode == 'Menu' and (item.type == 'B' or item.type == 'TDM'):
                item.update(render.renderList, self.dt, self.typing, pygame.mouse.get_pos())

            elif self.mode == 'Game' and (item.type == 'E' or item.type == 'R'):
                item.update(self.sendToServer, self.dt, self.typing, pygame.mouse.get_pos())

            elif self.mode == 'Game' and (item.type == 'DRAW' or item.type == 'CB' or item.type == 'TD'):
                item.update(render.renderList, self.dt, self.typing, pygame.mouse.get_pos())

        #rendering the local player and confirmed objects as well as remote ones
        if self.mode == 'Game':
            render.renderList.extend(self.sendToServer)

            #saving a fresh snapshot before Main clears sendToServer next frame
            with self.networkLock:
                self.outgoingObjects = [item.copy() for item in self.sendToServer]
                remoteObjects = self.remoteObjects

            render.renderList.extend(remoteObjects)
        else:
            #the server should not show this player while they are in the menu
            with self.networkLock:
                self.outgoingObjects = []

        if len(self.message[self.message.rfind('|')+1:]) >= 10:
            self.message += '|'

        if self.portStr != '':
            self.port = int(self.portStr)

        else:
            self.port = 0

    def network_loop(self):

        #this method sends object lists and receives the latest remote objects
        connectionErrorReported = False

        while not self.networkStop.is_set():
            try:
                #trying to connect without freezing the pygame window
                with socket.create_connection((self.host, self.port), timeout=2) as conn:
                    conn.settimeout(5)

                    #using a persistent reader to receive one complete JSON line
                    with conn.makefile('rb') as reader:
                        self.networkConnected = True
                        connectionErrorReported = False
                        print('Connected to server')

                        while not self.networkStop.is_set():

                            #getting the latest local objects from the main thread
                            with self.networkLock:
                                objects = self.outgoingObjects

                            #sending one newline-terminated JSON list
                            payload = json.dumps(objects).encode('utf-8') + b'\n'
                            conn.sendall(payload)

                            #the server replies with the other players objects
                            receivedData = reader.readline(1_000_001)

                            if not receivedData:
                                raise ConnectionError('server closed forcibly')

                            if len(receivedData) > 1_000_000 or not receivedData.endswith(b'\n'):
                                raise ValueError('server not right')

                            remoteObjects = json.loads(receivedData)

                            #checking the basic format before sending it to the renderer
                            if not isinstance(remoteObjects, list) or any(
                                not isinstance(item, list) or len(item) != 6 or
                                item[0] not in ('E', 'R') or
                                not isinstance(item[1], list) or len(item[1]) != 3
                                for item in remoteObjects
                            ):
                                raise ValueError('object not right')

                            #the pygame loop will read this list on its next frame
                            with self.networkLock:
                                self.remoteObjects = remoteObjects

                            #networking runs at roughly 60 updates per second
                            self.networkStop.wait(0.016)

            except (OSError, ValueError, TypeError, UnicodeError) as error:
                if not connectionErrorReported and not self.networkStop.is_set():
                    print(f'{error} network not there')
                    connectionErrorReported = True

            finally:
                self.networkConnected = False

                #clearing remote players when the server is unavailable
                with self.networkLock:
                    self.remoteObjects = []

            #reconnecting after the server comes back online
            self.networkStop.wait(1)

    def flush_lists(self, lists):

        #here I am flushing all the lists that need to be flushed to prevent rapid RAM filling
        for item in lists:
            item.clear()

    def check_events(self):

        #doing the normal checks for a pygame instance to make sure it can be closed, and so I can check for things like pressing buttons
        for event in pygame.event.get():

            #searching though every event that has happened
            if event.type == pygame.QUIT:
                self.running = False
                self.networkStop.set()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:

                    # checking whether the player has clicked a button
                    buttonPressed = False

                    for item in self.mainList:
                        if item.type in ('B', 'CB') and item.rect.collidepoint(event.pos):

                            # only allowing buttons in the current mode to be pressed
                            if (self.mode == 'Menu' and item.type == 'B') or (self.mode == 'Game' and item.type == 'CB'):
                                item.pressed(self)
                                buttonPressed = True
                                break

                    # only drawing objects when the player is in game mode
                    if not buttonPressed and self.mode == 'Game':

                        if not self.drawing:
                            self.objectBeingDrawn = DrawElipse(event.pos, event.pos, self)
                            self.drawing = True

                        else:
                            newObject = DrawnObjectBase(self,self.objectBeingDrawn.pos,self.objectBeingDrawn.typeS,self.objectBeingDrawn.colour,self.objectBeingDrawn.rect.copy())

                            # removing the temporary drawing object
                            self.mainList.remove(self.objectBeingDrawn)
                            self.objectBeingDrawn = None
                            self.drawing = False

            if event.type == pygame.KEYDOWN and self.drawing:

                # checking if the player wants to cancel the current drawing
                if event.key == pygame.K_ESCAPE:

                    # removing the temporary object from the main list
                    if self.objectBeingDrawn is not None:
                        self.mainList.remove(self.objectBeingDrawn)

                    # clearing the object reference and drawing state
                    self.objectBeingDrawn = None
                    self.drawing = False

            if event.type == pygame.KEYDOWN and self.typing == 'C':

                #performing checks for key edge cases and also checking for length of string so I can add a \n
                if event.key == pygame.K_BACKSPACE:
                    if self.message[len(self.message)-1:] == '|':
                        self.message = self.message[:-2]
                    else:
                        self.message = self.message[:-1]

                elif event.key == pygame.K_RETURN:
                    self.message = ''
                    self.typing = False

                else:
                    self.message += event.unicode

            if event.type == pygame.KEYDOWN and self.typing == 'P':
                if event.key == pygame.K_BACKSPACE:
                    self.portStr = self.portStr[:-1]
                else:
                    try:
                        int(event.unicode)
                        self.portStr += event.unicode
                    except ValueError:
                        pass

            if event.type == pygame.KEYDOWN and self.typing == 'IP':
                if event.key == pygame.K_BACKSPACE:
                    self.host = self.host[:-1]
                else:
                    self.host += event.unicode
