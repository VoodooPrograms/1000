# "1000" Card Game

This is a project for Symbolics Languages class

## Getting Started

This project is focused on developing popular card game in Poland called "1000" (or Russian Schnapsen in english)
where communication is made via WebSockets where every player can join to game
from his browser.

Wiki page of this game: https://en.wikipedia.org/wiki/Russian_Schnapsen

Some screenshots:

_TBD_


### Prerequisites

This project requires:
* Python 3.7 or higher
* pip 10.0.x or higher
* Tornado 6 or higher

To install Tornado you can run:
```
pip install -r requirements.txt
```

### Run

Before running you should check configuration.

MessageHandler.js
```
MessageHandler.host = "192.168.8.102"; // or localhost
MessageHandler.port = ":8888";
```
main.py
```
app.listen(8888)
```

If everything is okey run from terminal:
```
python main.py
```

And then go to your favourite browser and type in address bar:
_localhost:8888_

Opening 4 cards allows you to play on localhost, but if you chose your machine address instead of localhost,
 then you should type that address from every other machine.  
## Running the tests

```
python -m unittest discover -s Tests -p 'Test*.py' 
```

## Authors

* **Bartosz Belski** - *Initial work* - [My GitHub](https://github.com/VoodooPrograms)

