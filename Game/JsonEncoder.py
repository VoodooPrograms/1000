from json import JSONEncoder

from Game.Card import Card


class JsonEncoder(JSONEncoder):
    def default(self, o):
        # if isinstance(o, Card):
        #     return {'rank': o.rank, 'suit': o.suit}
        return o.__dict__
