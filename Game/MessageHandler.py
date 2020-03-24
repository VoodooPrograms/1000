
import json

import tornado

from Game.MessageWriter import MessageWriter
from Game.Server import Server


class MessageHandler(tornado.websocket.WebSocketHandler):
    connections = set()
    server = Server()

    def open(self):
            # if len(self.connections) == 4:
            #     self.close()
        # self.server = Server()
        writer = MessageWriter(self)
        self.server.set_writer(writer)

        print("Connections opened")
        self.connections.add(self)

    def on_message(self, message):
        self.server.set_writer(MessageWriter(self))

        decoded_message = json.loads(message)
        message_type = decoded_message["type"]
        if hasattr(self.server, message_type):
            getattr(self.server, message_type)(decoded_message)
        else:
            print(f"There is no {message_type} command")

    def on_close(self):
        self.connections.remove(self)
        print("Connection is down")
