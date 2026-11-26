
'''
this is going to be the main server class that will handle multiplayer functionality
the server receives objects and chat messages, merges them and sends them back to clients
'''

import json
import socket
import threading


class Server:
    def __init__(self):

        #this is the main dictionary where all players info is stored
        self.connected_players = {}
        self.banned_players = []

        #this is the main server information like the address and the port
        self.host = '0.0.0.0'
        self.port = 8080
        self.lock = threading.Lock()

        #setting up the main server socket
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))
        self.server.listen()

        print(f"Server started on {self.host}:{self.port}")

    def send_to_players(self, conn):

        #collecting every player's objects in join order, including the player receiving them
        with self.lock:
            worldObjects = []
            chatMessages = []

            for playerID, (objects, message) in self.connected_players.items():
                worldObjects.extend(objects)

                if message:
                    chatMessages.append([playerID, message])

        #converting the object and chat lists into JSON
        payload = json.dumps([worldObjects, chatMessages]).encode('utf-8') + b'\n'

        #sending the combined list back to the client
        conn.sendall(payload)

    def check_data(self, data):

        #checking that the received data is a list
        if not isinstance(data, list) or len(data) > 5000:
            return False

        for item in data:

            #checking the expected six-part object format
            if not isinstance(item, list) or len(item) != 6:
                return False

            #checking the object type
            if item[0] not in ('E', 'R'):
                return False

            #checking that the colour contains three valid values
            colour = item[1]

            if not isinstance(colour, list) or len(colour) != 3:
                return False

            if any(type(value) is not int or not 0 <= value <= 255 for value in colour):
                return False

            #checking the four rectangle values
            for value in item[2:6]:
                if type(value) not in (int, float):
                    return False

                if not -100000 <= value <= 100000:
                    return False

        return True

    def handle_connection(self, conn, addr):

        #creating an identifier for the connected player
        addrStr = f'{addr[0]}:{addr[1]}'

        #adding the new player to the main dictionary
        if addrStr in self.banned_players:
            conn.close()
            return

        with self.lock:
            self.connected_players[addrStr] = [[], '']

        print(f"{addrStr} joined ")

        try:
            with conn:

                #creating a reader for receiving complete JSON messages
                with conn.makefile('rb') as reader:

                    while True:

                        #receiving one complete message
                        receivedData = reader.readline(1_000_001)

                        #checking whether the player disconnected
                        if not receivedData:
                            break

                        #preventing excessively large messages
                        if len(receivedData) > 1_000_000:
                            raise ValueError('message to long!')

                        if not receivedData.endswith(b'\n'):
                            raise ValueError('message not finished')

                        #converting the JSON back into a Python list
                        receivedList = json.loads(receivedData)

                        #checking the received data before storing it
                        if not isinstance(receivedList, list) or len(receivedList) != 2:
                            raise ValueError('invalid player update')

                        objects, message = receivedList

                        if not self.check_data(objects):
                            raise ValueError('the object list was wrongun')

                        if not isinstance(message, str) or len(message) > 500 or (message and not message.isprintable()):
                            raise ValueError('invalid chat message')

                        #updating the stored objects and current message for this player
                        with self.lock:
                            self.connected_players[addrStr] = [objects, message]

                        #sending the merged objects and messages back to the player
                        self.send_to_players(conn)

        except (ConnectionError, OSError, ValueError, UnicodeError) as error:
            print(f" player {addrStr}, {error}")

        finally:

            #removing the player's objects and message when they disconnect
            with self.lock:
                self.connected_players.pop(addrStr, None)

            print(f"{addrStr} got disconnected")

    def run(self):

        #continuously accepting new player connections
        try:
            while True:

                #waiting for a new player to connect
                conn, addr = self.server.accept()

                #creating a new thread for the connected player
                clientThread = threading.Thread(target=self.handle_connection,args=(conn, addr),daemon=True)

                clientThread.start()

        except KeyboardInterrupt:
            print("server closing down")

        finally:
            self.server.close()


server = Server()
server.run()
