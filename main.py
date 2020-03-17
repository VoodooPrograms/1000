import os

import tornado.ioloop
import tornado.web
import tornado.websocket

import json
import datetime
from Game import Game, Deck
from Game import Player


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        items = ["Andrzej", "Bartek", "Marcin", "Natalia"]
        deck = Deck.Deck()
        self.render("index.html", title="1000 App", items=items, musik=deck.create_musik(), cards=deck.cards)


class SimpleWebSocket(tornado.websocket.WebSocketHandler):
    connections = set()
    players = set()

    def open(self):
        if len(self.connections) == 4:
            self.close()

        print("Connections opened")
        self.connections.add(self)

    def on_message(self, message):
        decoded_message = json.loads(message)
        now = datetime.datetime.now()
        decoded_message["time"] = now.strftime('[%H:%M:%S]')
        message = json.dumps(decoded_message)
        self.players.add(Player.Player(decoded_message["user"]))

        print(f'Message sent arrived: "{decoded_message["message"]}" from {decoded_message["user"]} at {now}')
        [client.write_message(message) for client in self.connections]

        if len(self.connections) == 1:
            print("All players are connected")
            Game.Game(self.players)

    def on_close(self):
        self.connections.remove(self)
        print("Connection is down")


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/websocket", SimpleWebSocket),
        (r'/static/css/(.*)', tornado.web.StaticFileHandler, {'path': './static/css'}),
        (r"/static/images/(.*)", tornado.web.StaticFileHandler, {"path": "./static/images"})
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
