
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
    document.getElementById("chat").appendChild(messageBox);
};

MessageHandler.prototype.start_game = function (evt) {
    console.debug(evt);
    let musikBox = document.getElementById("musik");
    for (i = 0 ; i < evt.musik; i++){
        let cardBox = document.createElement("img");
        cardBox.setAttribute("src", "/static/images/red_back.png");
        cardBox.setAttribute("width", "100");
        musikBox.append(cardBox);
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
        document.getElementById("chat").appendChild(messageBox);
    }
};

MessageHandler.prototype.init_hand = function (evt) {
    console.debug(evt);
    let myCardBox = document.getElementById("my-hand");
    for (let card of evt.hand){
        let cardBox = document.createElement("img");
        cardBox.setAttribute("src", card.filename);
        cardBox.setAttribute("width", "100");
        cardBox.dataset.value = card.value;
        myCardBox.append(cardBox)
    }
};

MessageHandler.prototype.init_score_table = function (evt) {
    console.debug(evt);
    let scoreTableBox = document.getElementById("score-table");
    for (let player in evt.score_table.score_table){
        let scoreBox = document.createElement("div");
        scoreBox.className = "score-table-row";
        scoreBox.innerHTML = player + " : " + evt.score_table.score_table[player];
        scoreTableBox.append(scoreBox);
    }
};


MessageHandler.prototype.init_round = function (evt) {
    console.debug(evt);
    let potsTableBox = document.getElementById("pots-table");
    for (let pot of evt.pots) {
        let potBox = document.createElement("button");
        potBox.innerHTML = pot;
        potsTableBox.append(potBox);

        potBox.addEventListener("click", function () {
            console.log(this.innerHTML);
            message_handler.sendMessage({"type": "set_pot", "pot_value": this.innerHTML});
            potsTableBox.innerHTML = ""
        });
    }
    let passButton = document.createElement("button");
    passButton.innerHTML = "pass";
    passButton.addEventListener("click", function () {
        message_handler.sendMessage({"type": "set_pot", "pot_value": this.innerHTML});
        potsTableBox.innerHTML = ""
    });
    potsTableBox.append(passButton);

    // let modal = document.getElementById("myModal");
    // modal.style.display = "block";
};

MessageHandler.prototype.show_musik = function (evt) {
    console.debug(evt)
    let musikBox = document.getElementById("musik");
    musikBox.innerHTML = "";
    for (let card of evt.musik){
        let cardBox = document.createElement("img");
        cardBox.setAttribute("src", card.filename);
        cardBox.setAttribute("width", "100");
        cardBox.dataset.value = card.value;
        musikBox.append(cardBox);
        cardBox.addEventListener("click", function () {
            cardBox.setAttribute("src", card.filename);
        });
    }
    let buttonGetMusik = document.createElement("button");
    buttonGetMusik.innerHTML = "Weź karty z musika";
    musikBox.append(buttonGetMusik);
    buttonGetMusik.addEventListener("click", function () {
        let musikCards = document.getElementById("musik").childNodes;
        let myCardBox = document.getElementById("my-hand");
        myCardBox.append(...musikCards);
        buttonGetMusik.remove();
        message_handler.sendMessage({"type": "set_cards_from_musik", "musik": evt.musik})
    });
};

MessageHandler.prototype.give_card_to_next_player = function (evt) {
    console.debug(evt)

};