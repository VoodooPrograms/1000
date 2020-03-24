import json

from Game.JsonEncoder import JsonEncoder


class MessageWriter:
    def __init__(self, socket):
        self.socket = socket

    def sendMessage(self, message):
        self.socket.write_message(json.dumps(message, cls=JsonEncoder))

    def emitMessage(self, message):
        [client.write_message(json.dumps(message, cls=JsonEncoder)) for client in self.socket.connections]

    def sendError(self, exception):
        jsonResponse = {}
        jsonResponse['response'] = 'exception'
        jsonResponse['resultMessage'] = str(exception)
        self.socket.write_message(jsonResponse, cls=JsonEncoder)

    def closeConnection(self):
        self.socket.close()
