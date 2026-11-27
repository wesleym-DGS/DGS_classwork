
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
        self.portStr = str(self.port) if self.port else ''
        self.outgoingState = [[], '']
        self.worldObjects = None
        self.chatMessages = []
        self.networkConnected = False

        #keeping network operations away from the pygame main loop
        self.networkLock = threading.Lock()
        self.networkStop = threading.Event()
        self.networkThread = threading.Thread(target=self.network_loop,daemon=True)
        self.networkThread.start()

    def update_checks(self, item, render, gameText):

        if self.mode == 'Menu' and item.type in ('B', 'TDM'):
            item.update(render.renderList, self.dt, self.typing, pygame.mouse.get_pos())

        elif self.mode == 'Game' and item.type in ('E', 'R'):
            item.update(self.sendToServer, self.dt, self.typing, pygame.mouse.get_pos())

        elif self.mode == 'Game' and item.type in ('DRAW', 'CB'):
            item.update(render.renderList, self.dt, self.typing, pygame.mouse.get_pos())

        elif self.mode == 'Game' and item.type == 'TD':
            item.update(gameText, self.dt, self.typing, pygame.mouse.get_pos())

    def update_renderer(self, worldObjects, gameText, render):
        # use the local objects while waiting for a world update from the server
        if worldObjects is None:
            worldObjects = self.sendToServer

        # rendering the chat after the game objects so it stays visible
        render.renderList.extend(worldObjects)
        render.renderList.extend(gameText)

    def update_port(self):

        newPort = int(self.portStr or '0')
        self.port = newPort if 1 <= newPort <= 65535 else 0

    def update_all(self, render):

        #updating the time delta so the players movement doesn't change with frame rate
        self.dt = self.clock.tick(60) / 1000
        gameText = []

        #going though all items in the main list and telling them to update themselves
        for item in self.mainList:
            self.update_checks(item, render, gameText)

        if self.mode == 'Game':
            #saving a fresh snapshot before Main clears sendToServer next frame
            with self.networkLock:
                self.outgoingState = [[item.copy() for item in self.sendToServer], self.message]
                worldObjects = self.worldObjects

            self.update_renderer(worldObjects, gameText, render)

        else:
            #the server should not show this player while they are in the menu
            with self.networkLock:
                self.outgoingState = [[], '']

    def send_network_update(self, conn):

        #getting the latest local objects and message from the main thread
        with self.networkLock:
            outgoingState = self.outgoingState

        #sending one newline-terminated JSON list
        payload = json.dumps(outgoingState).encode('utf-8') + b'\n'
        conn.sendall(payload)

    def receive_network_update(self, reader):

        #the server replies with the full world in draw order and current messages
        receivedData = reader.readline(1_000_001)

        if not receivedData:
            raise ConnectionError('server closed connection')

        if len(receivedData) > 1_000_000 or not receivedData.endswith(b'\n'):
            raise ValueError('invalid server message')

        receivedList = json.loads(receivedData)

        if not isinstance(receivedList, list) or len(receivedList) != 2:
            raise ValueError('invalid server update')

        worldObjects, chatMessages = receivedList

        #checking the basic format before sending it to the renderer
        if not isinstance(worldObjects, list) or any(not isinstance(item, list) or len(item) != 6 or item[0] not in ('E', 'R') or not isinstance(item[1], list) or len(item[1]) != 3 for item in worldObjects):
            raise ValueError('invalid server object list')

        if not isinstance(chatMessages, list) or any(not isinstance(item, list) or len(item) != 2 or not all(isinstance(part, str) and part.isprintable() for part in item) for item in chatMessages):
            raise ValueError('invalid server chat list')

        #the pygame loop will read these lists on its next frame
        with self.networkLock:
            self.worldObjects = worldObjects
            self.chatMessages = chatMessages

    def exchange_network_updates(self, conn, reader):

        #the connection stays open while the player remains in game
        while not self.networkStop.is_set() and self.mode == 'Game':
            self.send_network_update(conn)
            self.receive_network_update(reader)

            #aiming for up to roughly 60 updates per second
            self.networkStop.wait(1 / 60)

    def network_loop(self):

        connectionErrorReported = False

        #keeping the thread alive even when the player is still in the menu
        while not self.networkStop.is_set():

            #only connecting in game when a valid port has been entered
            if self.mode != 'Game' or self.port == 0:
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
                        self.exchange_network_updates(conn, reader)

            except (OSError, ValueError, TypeError, UnicodeError) as error:

                if not connectionErrorReported and not self.networkStop.is_set():
                    print(f'network unavailable: {error}')
                    connectionErrorReported = True

            finally:

                self.networkConnected = False

                #clearing the world snapshot and chat when the connection is closed
                with self.networkLock:
                    self.worldObjects = None
                    self.chatMessages = []

            #reconnecting after the server comes back online
            if self.mode == 'Game':
                self.networkStop.wait(1)

    def flush_lists(self, lists):

        #here I am flushing all the lists that need to be flushed to prevent rapid RAM filling
        for item in lists:
            item.clear()

    def check_for_buttons(self, event):
        buttonPressed = False

        for item in self.mainList:

            if item.type in ('B', 'CB') and item.rect.collidepoint(event.pos):

                # only allowing buttons in the current mode to be pressed
                if ((self.mode == 'Menu' and item.type == 'B') or (self.mode == 'Game' and item.type == 'CB')):
                    item.pressed(self)
                    buttonPressed = True
                    break

        return buttonPressed

    def start_stop_drawing(self, buttonPressed, event, playerType):
        # only drawing objects when the player is in game mode
        if not buttonPressed and self.mode == 'Game':

            if not self.drawing:

                if playerType == 'E':
                    self.objectBeingDrawn = DrawElipse(event.pos, event.pos, self)

                elif playerType == 'R':
                    self.objectBeingDrawn = DrawRect(event.pos, event.pos, self)

                self.drawing = True

            else:
                newObject = DrawnObjectBase(self, self.objectBeingDrawn.pos, self.objectBeingDrawn.typeS, self.objectBeingDrawn.colour, self.objectBeingDrawn.rect.copy())

                # removing the temporary drawing object
                self.mainList.remove(self.objectBeingDrawn)

                self.objectBeingDrawn = None
                self.drawing = False

    def cancel_shape(self, event):
        if self.drawing:
            # checking if the player wants to cancel the current drawing
            if event.key == pygame.K_ESCAPE:

                # removing the temporary object from the main list
                if self.objectBeingDrawn is not None:
                    self.mainList.remove(self.objectBeingDrawn)

                # clearing the object reference and drawing state
                self.objectBeingDrawn = None
                self.drawing = False

    def typing_check_chat(self, event):
        if self.typing == 'C':

            # checking the chat input
            if event.key == pygame.K_BACKSPACE:
                self.message = self.message[:-1]

            elif event.key == pygame.K_RETURN:
                self.message = ''
                self.typing = 'G'

            elif event.unicode.isprintable():
                self.message = (self.message + event.unicode)[:500]

    def typing_check_port(self, event):
        if self.typing != 'P':
            return

        # allowing the player to change the server port
        if event.key == pygame.K_BACKSPACE:
            self.portStr = self.portStr[:-1]

        elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            self.typing = 'G'
            return

        elif len(self.portStr) < 5:
            digit = event.unicode
            keypadKeys = (
                pygame.K_KP0, pygame.K_KP1, pygame.K_KP2, pygame.K_KP3, pygame.K_KP4,
                pygame.K_KP5, pygame.K_KP6, pygame.K_KP7, pygame.K_KP8, pygame.K_KP9
            )
            if event.key in keypadKeys:
                digit = str(keypadKeys.index(event.key))

            if len(digit) == 1 and digit in '0123456789':
                self.portStr += digit

        self.update_port()

    def typing_check_ip(self, event):
        if self.typing == 'IP':

            # allowing the player to change the server IP address
            if event.key == pygame.K_BACKSPACE:
                self.host = self.host[:-1]

            elif event.key == pygame.K_RETURN:
                self.typing = 'G'

            elif event.unicode.isprintable() and not event.unicode.isspace():
                if len(self.host) < 253:
                    self.host += event.unicode

    def check_events(self, playerType):

        #doing the normal checks for a pygame instance to make sure it can be closed
        for event in pygame.event.get():

            #searching though every event that has happened
            if event.type == pygame.QUIT:
                self.running = False
                self.networkStop.set()

            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:
                    buttonPressed = self.check_for_buttons(event)
                    self.start_stop_drawing(buttonPressed, event, playerType)

            if event.type == pygame.KEYDOWN:
                self.cancel_shape(event)
                self.typing_check_chat(event)
                self.typing_check_port(event)
