import os

import tornado.ioloop
import tornado.web
import tornado.websocket

import json
import datetime
from Game import Game, Deck, MessageHandler
from Game import Player


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        items = ["Andrzej", "Bartek", "Marcin", "Natalia"]
        deck = Deck.Deck()
        self.render("index.html", title="1000 App", items=items, musik=deck.create_musik(), cards=deck.cards)


class GameHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("Templates/instructions.html", title="1000 App")


class InstructionHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("Templates/instructions.html")


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/websocket", MessageHandler.MessageHandler),
        (r"/game", GameHandler),
        (r"/instruction", InstructionHandler),
        (r'/static/css/(.*)', tornado.web.StaticFileHandler, {'path': './static/css'}),
        (r"/static/images/(.*)", tornado.web.StaticFileHandler, {"path": "./static/images"})
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
