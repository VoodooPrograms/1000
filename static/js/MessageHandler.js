
function MessageHandler(){}

MessageHandler.prototype.ws = new WebSocket("ws://localhost:8888/websocket");

MessageHandler.prototype.connect = function(){

    let self = this;
    this.ws.onopen = function() {
        console.debug("Connection opened");
        self.sendMessage({"type": "add_player"})
        //self.sendMessage({"type": "setUsername", "user": "bartek", "message": "wiadomosc"});
    };

    this.ws.onclose = function() {
        console.debug("Connection closed");
    };

    this.ws.onmessage = function(evt) {
        self.resolveMessage(evt.data);
    };
};

MessageHandler.prototype.resolveMessage = function(message){
    console.debug("Received: " + message);

    let json = JSON.parse(message);
    let handlerName = json.type;
    let functionCall = this[handlerName];


    //check whether handler function exists
    if (typeof functionCall != 'function') {
        console.error('Unknown response: ' + handlerName);
    } else {
        console.debug('Calling method handler: ' + handlerName);
    }

    //call handler function
    this[handlerName](json);
};

MessageHandler.prototype.sendMessage = function (message) {
    let messageStr = JSON.stringify(message);
    this.ws.send(messageStr);

    console.debug("Sent: " + messageStr);
};

MessageHandler.prototype.update_chat = function(evt) {
    console.debug(evt);
    // let messageDict = JSON.parse(evt);
    // Create a div with the format `user: message`.
    let messageBox = document.createElement("div");
    messageBox.innerHTML = evt.time + evt.user + ": " + evt.message;
    document.getElementById("messages").appendChild(messageBox);
};

MessageHandler.prototype.start_game = function (evt) {
    console.debug(evt);
    for (let card of evt.deck.cards){
        let cardBox = document.createElement("img");
        cardBox.setAttribute("src", card.filename);
        cardBox.setAttribute("width", "100");
        document.body.append(cardBox)
    }
};

MessageHandler.prototype.set_username = function (evt) {
    console.debug(evt);
    if (evt.freeSeats === false) {
        prompt("There are no more seats");
    } else {
        let messageBox = document.createElement("div");
        messageBox.innerHTML = evt.time + evt.user + ": " + evt.message;
        document.getElementById("messages").appendChild(messageBox);
    }
};