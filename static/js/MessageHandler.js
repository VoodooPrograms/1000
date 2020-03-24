
function MessageHandler(){}

MessageHandler.prototype.ws = new WebSocket("ws://localhost:8888/websocket");

MessageHandler.prototype.connect = function(){

    let self = this;
    this.ws.onopen = function() {
        console.debug("Connection opened");
        self.sendMessage({"type": "add_player"})
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
    let messageBox = document.createElement("div");
    messageBox.innerHTML = evt.time + evt.user + ": " + evt.message;
    document.getElementById("messages").appendChild(messageBox);
};

MessageHandler.prototype.start_game = function (evt) {
    console.debug(evt);
    let musikBox = document.getElementById("musik");
    for (let card of evt.musik){
        let cardBox = document.createElement("img");
        cardBox.setAttribute("src", (evt.hide) ? "/static/images/red_back.png" : card.filename);
        cardBox.setAttribute("width", "100");
        cardBox.dataset.value = card.value;
        musikBox.append(cardBox);
        cardBox.addEventListener("click", function () {
            cardBox.setAttribute("src", card.filename);
        });
    }
    // this.sendMessage({'type': 'ask_for_cards'});
};

MessageHandler.prototype.set_username = function (evt) {
    console.debug(evt);
    if (evt.freeSeats === false) {
        alert("There are no more seats");
    } else {
        let messageBox = document.createElement("div");
        messageBox.innerHTML = evt.time + evt.user + ": " + evt.message;
        document.getElementById("messages").appendChild(messageBox);
    }
};

MessageHandler.prototype.init_hand = function (evt) {
    console.debug(evt);
    let myCardBox = document.getElementById("my-hand")
    for (let card of evt.hand){
        let cardBox = document.createElement("img");
        cardBox.setAttribute("src", card.filename);
        cardBox.setAttribute("width", "100");
        cardBox.dataset.value = card.value;
        myCardBox.append(cardBox)
    }
};