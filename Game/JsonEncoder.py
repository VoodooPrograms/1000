from json import JSONEncoder


class JsonEncoder(JSONEncoder):
    def default(self, o):
        # if isinstance(o, Card):
        #     return {'rank': o.rank, 'suit': o.suit}
        return o.__dict__
