import datetime

from Game.Game import Game
from Game.MessageWriter import MessageWriter
from Game.Player import Player


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

        response = {'type': 'init_score_table'}
        response['score_table'] = self.game.score_table
        self.writer.emitMessage(response)

        self.init_round_game()

    """
    Rozpoczynanie nowego rozdania
    """
    def init_round_game(self):
        response = {'type': 'start_game'}
        response['musik'] = 4
        response['hide'] = True
        self.writer.emitMessage(response)

        response = {'type': 'init_hand'}
        for player, connection in enumerate(self.writer.socket.connections):
            response['hand'] = self.players[player].getHand()
            self.set_writer(MessageWriter(connection))
            self.writer.sendMessage(response)

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

    def clear_musik(self):
        response = {"type": "clear_musik"}
        self.writer.emitMessage(response)

    def set_cards_from_musik(self, message):
        print(message["musik"])
        print(self.game.current_player)
        print(self.game.round.current_player)
        self.clear_musik()
        self.game.give_cards(message["musik"])
        response = {"type": "give_card_to_next_player"}
        response["nextPlayer"] = self.game.round.musik_current_player
        self.writer.sendDirectMessage(response, self.game.round.current_player)
        self.game.round.next_musik_player()

    def give_away_card(self, message):
        print(message)
        self.game.transfer_card(self.game.round.current_player, message["for_player"], message["choosen_card"])
        response = {"type": "init_hand"}
        response["hand"] = self.game.round.players[message["for_player"]].hand
        self.writer.sendDirectMessage(response, message["for_player"])

        if (self.game.round.musik_current_player <= 3):
            print("Musik current player", self.game.round.musik_current_player)
            response = {"type": "give_card_to_next_player"}
            response["nextPlayer"] = self.game.round.musik_current_player
            self.writer.sendDirectMessage(response, self.game.round.current_player)
            self.game.round.next_musik_player()
        else:
            print("Start a game...")
            self.init_round()

    def init_round(self):
        print("Choosing a card")
        self.game.round.playing_current_player = self.game.round.current_player
        response = {"type": "choose_card_to_play"}
        self.writer.sendDirectMessage(response, self.game.round.playing_current_player)

    def put_card_on_table(self, message):
        chosen_card = self.game.round.players[self.game.round.playing_current_player].getCardFromHand(message["choosen_card"])
        is_finished = self.game.round.add_to_card_table(chosen_card)
        response = {"type": "show_card"}
        response["card"] = chosen_card
        self.writer.emitMessage(response)

        if is_finished:
            self.clear_card_table()
            if self.game.round.is_round_finished():
                self.game.score_table.update_score_table(self.game.round.score_table)
                if self.game.score_table.winner:
                    self.finish_game()
                self.update_score_table()
                self.game.init_round()  # Nowe rozdanie
                self.init_round_game()
            else:
                self.init_round()
            return

        self.game.round.next_playing_player()
        response = {"type": "choose_card_to_play"}
        self.writer.sendDirectMessage(response, self.game.round.playing_current_player)

    def update_score_table(self):
        response = {"type": "update_score_table"}
        response["score_table"] = self.game.score_table
        self.writer.emitMessage(response)

    def clear_card_table(self):
        response = {"type": "clear_table"}
        response["time_to_clear"] = 3000
        self.writer.emitMessage(response)

    def set_pot(self, message):
        is_pot_finished = self.game.round.set_pot(message["pot_value"])

        if not is_pot_finished:
            self.init_pots()
        else:
            self.show_musik()

    def finish_game(self):
        response = {"type": "finish_game"}
        response["winner"] = self.game.score_table.winner
        self.writer.emitMessage(response)

    def update_chat(self, message):
        print(message)
        now = datetime.datetime.now()
        message["time"] = now.strftime('[%H:%M:%S]')
        self.writer.emitMessage(message)

