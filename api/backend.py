from flask import Flask
import random

from card_scripting import cardPlayer

app = Flask(__name__)
num_games = 0
games = []


class Game:
    def __init__(self):
        """Initializes game, for now this just assumes 1 player and a starting deck
        TODO: support for more than one player"""
        self.deck = ['village', 'village', 'village', 'village', 'village', 'copper', 'copper', 'copper', 'copper', 'copper']
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
    games[game_id].discard.append(card_name)
    games[game_id].end_turn()
    return "hi"  # nothing actually needs to be returned, flask crashes without this.

@app.route("/cardplayed/<int:game_id>/<card_name>/")
def card_played(game_id, card_name):
    hand = games[game_id].hand
    i = hand.index(card_name)
    if i == -1:
        raise ValueError
    games[game_id].in_play.append(games[game_id].hand.pop(i))
    cardPlayer.playCard(game_id, card_name)
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

@app.route('/changeVar/<int:game_id>/<var_name>/<int:var_delta>/')
def change_var(game_id, var_name, var_delta):
    if var_name == "actions":
        games[game_id].actions += var_delta
    elif var_name == "buys":
        games[game_id].buys += var_delta
    elif var_name == "coins":
        games[game_id].coins += var_delta
    else:
        raise ValueError("Invalid variable name")
    return 'hello world' # nothing actually needs to be returned, flask crashes without this.

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
