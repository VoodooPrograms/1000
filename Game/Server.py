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
        response['musik'] = 4
        response['hide'] = True
        self.writer.emitMessage(response)

        response = {'type': 'init_hand'}
        for player, connection in enumerate(self.writer.socket.connections):
            response['hand'] = self.players[player].getHand()
            self.set_writer(MessageWriter(connection))
            self.writer.sendMessage(response)

        response = {'type': 'init_score_table'}
        response['score_table'] = self.game.score_table
        self.writer.emitMessage(response)

        response = {"type": "init_round"}
        print(self.game.round.CONTRACTS)
        response['pots'] = self.game.round.CONTRACTS
        self.writer.sendDirectMessage(response, self.game.current_player)

    def ask_for_cards(self, message):
        response = {'type': 'init_hand'}
        for player, connection in enumerate(self.writer.socket.connections):
            response['hand'] = self.players[player].getHand()
            self.set_writer(MessageWriter(connection))
            self.writer.sendMessage(response)

    def init_pots(self):
        response = {"type": "init_round"}
        response["pots"] = tuple(self.game.round.get_contracts())
        self.writer.sendDirectMessage(response, self.game.round.current_player)

    def show_musik(self):
        response = {"type": "show_musik"}
        response["musik"] = self.game.deck.create_musik()
        self.writer.sendDirectMessage(response, self.game.round.current_player)

    def set_cards_from_musik(self, message):
        print(message["musik"])
        print(self.game.current_player)
        print(self.game.round.current_player)
        self.game.give_cards(message["musik"])
        response = {"type": "give_card_to_next_player"}
        response["nextPlayer"] = 1
        self.writer.sendDirectMessage(response, 0)

    def init_round(self):
        pass

    def set_pot(self, message):
        self.game.round.set_pot(message["pot_value"])

        if not(self.game.round.is_pot_finished()):
            self.init_pots()
        else:
            self.show_musik()

    def update_chat(self, message):
        print(message)
        now = datetime.datetime.now()
        message["time"] = now.strftime('[%H:%M:%S]')
        self.writer.emitMessage(message)

