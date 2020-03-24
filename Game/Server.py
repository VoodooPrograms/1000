import datetime
import json

from Game.Game import Game
from Game.MessageWriter import MessageWriter
from Game.Player import Player
from main import MainHandler, GameHandler


class Server:
    def __init__(self):
        self.players = []
        self.writer = None
        self.game = None

    def set_writer(self, writer):
        self.writer = writer

    def join_game(self, message):
        response = {'type': 'set_username'}
        if len(self.players) == 4: # Prevent user from connecting
            response['freeSeats'] = False
            self.writer.sendMessage(response)
            self.writer.closeConnection()
        else:
            self.players.append(Player(message['user']))
            response['user'] = message['user']
            response['message'] = "Connected"
            response['time'] = datetime.datetime.now().strftime('[%H:%M:%S]')
            response['freeSeats'] = True
            self.writer.emitMessage(response)
            if len(self.players) == 4:
                self.start_game()

    def start_game(self):
        self.game = Game(self.players)
        response = {'type': 'start_game'}
        response['musik'] = self.game.deck.create_musik()
        response['hide'] = True
        self.writer.emitMessage(response)

        response = {'type': 'init_hand'}
        for player, connection in enumerate(self.writer.socket.connections):
            response['hand'] = self.players[player].getHand()
            self.set_writer(MessageWriter(connection))
            self.writer.sendMessage(response)

    def ask_for_cards(self, message):
        response = {'type': 'init_hand'}
        for player, connection in enumerate(self.writer.socket.connections):
            response['hand'] = self.players[player].getHand()
            self.set_writer(MessageWriter(connection))
            self.writer.sendMessage(response)

    def init_round(self):
        pass

    def update_chat(self, message):
        print(message)
        now = datetime.datetime.now()
        message["time"] = now.strftime('[%H:%M:%S]')
        self.writer.emitMessage(message)
