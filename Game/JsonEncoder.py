from json import JSONEncoder


class JsonEncoder(JSONEncoder):
    """
    This class is for encoding more complex objects than regular json.JSONEncoder

    Let's take for example Deck object, which has list of Card objects as an attribute.
    Regular JSONEncoder can't encode this, but this class can, because it override default encode method.
    Overrided method returns object as a dict which can be translate to JSON object.

    That's all magic here
    """
    def default(self, o):
        # if isinstance(o, Card):
        #     return {'rank': o.rank, 'suit': o.suit}
        return o.__dict__
