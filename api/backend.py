from flask import Flask, request
import random

from card_scripting import cardPlayer, cards

app = Flask(__name__)
num_games = 0
games = []


class Game:
    def __init__(self):
        """Initializes game, for now this just assumes 1 player and a starting deck
        TODO: support for more than one player"""
        self.nextCardID = 0
        deck = ['village', 'village', 'village', 'village', 'village', 'copper', 'copper', 'copper', 'copper', 'copper']
        self.deck = [self.make_card(c) for c in deck]
        #self.deck = ["copper", "copper", "copper", "copper", "copper", "copper", "copper", "estate", "estate", "estate"]
        self.hand = []
        self.discard = []
        self.in_play = []
        self.phase = "action"
        self.actions = 1
        self.buys = 1
        self.coins = 0
        global num_games
        self.id = num_games
        num_games += 1
        self.shuffle()
        self.draw_cards(5)

    def make_card(self, name):
        """returns a card object with the given name"""
        card = cards.getCard(name).copy()
        card['id'] = self.nextCardID
        card['name'] = name
        self.nextCardID += 1
        return card

    def draw_cards(self, num_to_draw):
        """draws cards while attempting to catch edge cases. I may have forgotten one, but this may be final."""
        for i in range(num_to_draw):
            if len(self.deck) == 0 and len(self.discard) == 0:
                break
            if len(self.deck) == 0:
                self.deck = self.discard
                self.discard = []
                self.shuffle()
            self.hand.append(self.deck.pop())

    def shuffle(self):
        """shuffles deck"""
        random.shuffle(self.deck)

    def end_turn(self):
        """Discards all cards in hand and in front of player"""
        while len(self.hand) > 0:
            self.discard.append(self.hand.pop())
        while len(self.in_play) > 0:
            self.discard.append(self.in_play.pop())
        self.draw_cards(5)
        self.actions = 1
        self.buys = 1
        self.coins = 0
        self.phase = 'action'
        


@app.route("/cardbought/<int:game_id>/<card_name>/")
def card_bought(game_id, card_name):
    game = games[game_id]
    cost = cards.getCard(card_name)['cost']
    if game.coins >= cost and game.buys >= 1:
        card = game.make_card(card_name)
        game.discard.append(card)
        game.coins -= cost
        game.buys -= 1
        
    return "hi"  # nothing actually needs to be returned, flask crashes without this.

@app.route("/cardplayed/<int:game_id>/<int:card_id>/")
def card_played(game_id, card_id):
    game = games[game_id]
    hand = game.hand
    #i = hand.index(card_name)
    idx = -1
    for i, card in enumerate(hand):
        if card['id'] == card_id:
            idx = i

    if idx == -1:
        raise ValueError
    card = game.hand[idx]
    type = card['type']
    if (type == 'action' and game.phase == 'action') or (type == 'treasure' and game.phase == 'buy'):
        if type == 'action':
            if game.actions >= 1:
                game.actions -= 1
            else:
                return "hi"
        game.in_play.append(card)
        cardPlayer.playCard(game_id, card['name'])
        game.hand.pop(idx)
    return "hi"  # nothing actually needs to be returned, flask crashes without this.


@app.route("/gethand/<int:game_id>/")
def get_hand(game_id):
    return str(games[game_id].hand)

@app.route("/getgamestate/<int:game_id>/")
def getgamestate(game_id):
    state = {}
    state["hand"] = games[game_id].hand
    state["discard"] = games[game_id].discard
    state["in_play"] = games[game_id].in_play
    state["deck"] = games[game_id].deck
    state["phase"] = games[game_id].phase
    state["actions"] = games[game_id].actions
    state["buys"] = games[game_id].buys
    state["coins"] = games[game_id].coins
    return state


@app.route("/getfrontstate/<int:game_id>/")
def getfrontstate(game_id):
    state = {}
    state["hand"] = games[game_id].hand
    state["discard"] = games[game_id].discard
    state["in_play"] = games[game_id].in_play
    state["phase"] = games[game_id].phase
    state["actions"] = games[game_id].actions
    state["buys"] = games[game_id].buys
    state["coins"] = games[game_id].coins
    return state

@app.route('/changeVar/', methods=['POST'])
def change_var():
    req = request.get_json()
    gameID = req['gameID']
    var = req['var']
    delta = int(req['delta'])
    if var == "actions":
        games[gameID].actions += delta
    elif var == "buys":
        games[gameID].buys += delta
    elif var == "coins":
        games[gameID].coins += delta
    else:
        raise ValueError("Invalid variable name")
    return 'Changing variable...' # nothing actually needs to be returned, flask crashes without this.

@app.route('/endphase/<int:game_id>/')
def end_phase(game_id):
    game = games[game_id]
    if game.phase == "action":
        game.phase = "buy"
    elif game.phase == "buy":
        game.end_turn()
    return "ended phase"

@app.route("/getsupply/<int:game_id>/")
def get_supply(game_id):
    raise NotImplementedError

@app.route("/draw/<int:game_id>/<int:num_cards>/")
def draw(game_id, num_cards):
    games[game_id].draw_cards(num_cards)
    return 'hellow world' # nothing actually needs to be returned, flask crashes without this.

@app.route("/newgame/")
def new_game():
    games.append(Game())
    return str(num_games - 1)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    Game()
