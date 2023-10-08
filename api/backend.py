from flask import Flask
from random import randint

app = Flask(__name__)
num_games = 0
games = []


class Game:
    def __init__(self):
        """Initializes game, for now this just assumes 1 player and a starting deck
        TODO: support for more than one player"""
        self.deck = ["copper", "copper", "copper", "copper", "copper", "copper", "copper", "estate", "estate", "estate"]
        self.hand = []
        self.discard = []
        self.in_play = []
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
        """shuffles deck, this should be final, really there is no need to change this"""
        for i in range(len(self.deck)):
            idx = randint(i, len(self.deck) - 1)
            temp = self.deck[]
            self.deck[i] = self.deck[idx]
            self.deck[idx] = temp

    def end_turn(self):
        """Discards all cards in hand and in front of player"""
        while len(self.hand) > 0:
            self.discard.append(self.hand.pop())
        while len(self.in_play) > 0:
            self.discard.append(self.in_play.pop())
        self.draw_cards(5)


@app.route("/cardbought/<int:game_id>/<card_name>/")
def card_bought(game_id, card_name):
    games[game_id].discard.append(card_name)
    games[game_id].end_turn()
    return "hi"  # nothing actually needs to be returned, flask crashes without this.


@app.route("/gethand/<int:game_id>/")
def get_hand(game_id):
    return str(games[game_id].hand)


@app.route("/newgame/")
def new_game():
    games.append(Game())
    return str(num_games - 1)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    Game()
