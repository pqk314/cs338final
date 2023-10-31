from flask import Flask, request, redirect, url_for, render_template
import random, json
import requests

from card_scripting import cardPlayer, cards
from player import player

app = Flask(__name__)
num_games = 0
games = []


class Game:
    def __init__(self, num_players):
        """Initializes game, for now this just assumes 1 player and a starting deck
        TODO: support for more than one player"""
        
        #to sort the cards by cost the self.supply needs to be sorted
        self.supply = ['market', 'festival', 'council_room', 'moat', 'militia', 'village', 'smithy', 'laboratory', 'witch', 'gardens']
        self.supply.sort(key=lambda card: cards.getCard(card)['cost'])
        # change to [10 for i in range(10)] to make it take the right number of cards to finish the game=
        self.supplySizes = [2 for i in range(10)]
        self.nextCardID = 0
        deck_cards = ['village', 'village', 'village', 'village', 'village', 'copper', 'copper', 'copper', 'copper', 'copper']
        custom_decks = [['cellar', 'village', 'village', 'village', 'village', 'copper', 'copper', 'copper', 'copper', 'copper'],
                        ['cellar', 'copper', 'copper', 'copper', 'copper', 'copper', 'copper', 'estate', 'estate', 'estate']]
        self.players = []
        for i in range(num_players):
            deck = [self.make_card(c) for c in custom_decks[i]]
            #deck = [self.make_card(c) for c in deck_cards]
            newPlayer = player(self, deck, i)
            #newPlayer.shuffle()
            #newPlayer.draw_cards(5)
            self.players.append(newPlayer)
            

        self.cmd = None
        self.options = None
        global num_games
        self.id = num_games
        num_games += 1

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

    def find_card_in_list(self, list, card_id):
        for idx, card in enumerate(list):
            if card['id'] == card_id:
                return idx
        return -1

    def find_card(self, card_id):
        for player in self.players:
            l, idx = player.find_card(card_id)
            if idx != -1:
                return l, idx
        return [], -1
    
    def find_card_in_trash(self, card_id):
        idx = self.find_card_in_list(self.trash, card_id)
        if idx != -1:
            return self.trash, idx
        return [], -1
    
    def find_card_objs(self, card_ids):
        objs = []
        for card_id in card_ids:
            l, idx = self.find_card(card_id)
            if idx!= -1:
                objs.append(l[idx])
        return objs

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
    player = game.players[0]
    cost = cards.getCard(card_name)['cost']
    if player.coins >= cost and player.buys >= 1:
        card = game.make_card(card_name)
        player.discard.append(card)
        player.coins -= cost
        player.buys -= 1
        game.supplySizes[game.supply.index(card_name)] -= 1

        
    return "hi"  # nothing actually needs to be returned, flask crashes without this.

@app.route("/cardplayed/<int:game_id>/<int:card_id>/")
def card_played(game_id, card_id):
    game = games[game_id]
    player = game.players[0]
    hand = player.hand

    idx = player.find_card_in_list(hand, card_id)

    if idx == -1:
        raise ValueError
    
    card = player.hand[idx]
    type = card['type']
    if (type == 'action' and player.phase == 'action') or (type == 'treasure' and player.phase == 'buy'):
        if type == 'action':
            if player.actions >= 1:
                player.actions -= 1
            else:
                return "hi"
        player.in_play.append(card)
        player.hand.pop(idx)
        cmd = cardPlayer.getCardCmd(game_id, card['name'])
        player.cmd = cmd
        res = cmd.execute()
        if res == "yield":
            return {'yield': True}

    return {'yield': False}


@app.route("/gethand/<int:game_id>/")
def get_hand(game_id):
    return str(games[game_id].players[0].hand)

@app.route("/getgamestate/<int:game_id>/")
def getgamestate(game_id):
    game = games[game_id]
    player = game.players[0]
    state = {}
    state["hand"] = player.hand
    state["discard"] = player.discard
    state["in_play"] = player.in_play
    state["deck"] = player.deck
    state["phase"] = player.phase
    state["actions"] = player.actions
    state["buys"] = player.buys
    state["coins"] = player.coins
    state["supply"] = game.supply
    state["supplySizes"] = game.supplySizes
    return state


@app.route("/getfrontstate/<int:game_id>/")
def getfrontstate(game_id):
    game = games[game_id]
    player = game.players[0]
    state = {}
    state["hand"] = player.hand
    state["discard"] = player.discard
    state["in_play"] = player.in_play
    state["phase"] = player.phase
    state["actions"] = player.actions
    state["buys"] = player.buys
    state["coins"] = player.coins
    state["supply"] = game.supply
    state["supplySizes"] = game.supplySizes
    return state

@app.route('/changeVar/', methods=['POST'])
def change_var():
    req = request.get_json()
    gameID = req['gameID']
    var = req['var']
    delta = int(req['delta'])
    player = games[gameID].players[0]
    if var == "actions":
        player.actions += delta
    elif var == "buys":
        player.buys += delta
    elif var == "coins":
        player.coins += delta
    else:
        raise ValueError("Invalid variable name")
    return 'Changed variable' # nothing actually needs to be returned, flask crashes without this.

@app.route('/changeZone/', methods=['POST'])
def change_zone():
    req = request.get_json()
    gameID = req['gameID']
    game = games[gameID]
    player = game.players[0]
    cards = req['cards']
    card_ids = [card['id'] for card in cards]
    zone = req['zone']

    dest = None
    if zone == 'discard':
        dest = player.discard
    elif zone == 'hand':
        dest = player.hand
    elif zone == 'deck':
        dest = player.deck
    elif zone == 'trash':
        dest = game.trash
    # TODO: only one trash zone per game
    for card_id in card_ids:
        card_loc = player.find_card(card_id)
        if card_loc[1] == -1:
            continue
        dest.append(card_loc[0].pop(card_loc[1]))

    return 'Changed zone'



@app.route('/endphase/<int:game_id>/')
def end_phase(game_id):
    game = games[game_id]
    player = game.players[0]
    if player.phase == "action":
        player.phase = "buy"
    elif player.phase == "buy":
        player.end_turn()
        game.players.append(game.players.pop(0))
    return "ended phase"

@app.route("/getsupply/<int:game_id>/")
def get_supply(game_id):
    game = games[game_id]
    return {"store": [game.make_card(game.supply[i]) for i in range(10) if game.supplySizes[i] > 0]}

@app.route("/draw/<int:game_id>/<int:num_cards>/")
def draw(game_id, num_cards):
    games[game_id].players[0].draw_cards(num_cards)
    return 'hello world' # nothing actually needs to be returned, flask crashes without this.

@app.route("/newgame/")
def new_game():
    games.append(Game(2))
    return str(num_games - 1)

@app.route("/selected/<int:game_id>/", methods=['POST'])
def selected(game_id):
    req = request.get_json()
    ids = req['ids']
    game = games[game_id]
    if 'player' in req:
        player = game.players[req['player']]
    else:
        player = game.players[0]
    player.options = None
    cards = game.find_card_objs(ids)
    player.cmd.setPlayerInput(cards)
    res = player.cmd.execute()

    if res == "yield":
        return "yield"

    return "Hello World!"

@app.route("/setoptions/<int:game_id>/", methods=['POST'])
def set_options(game_id):
    game = games[game_id]
    req = request.get_json()
    if 'player' in req:
        player = game.players[req['player']]
        del req['player']
    else:
        player = game.players[0]
    player.options = req
    return "hello world" # nothing actually needs to be returned, flask crashes without this.

@app.route("/ischoice/<int:game_id>/")
def ischoice(game_id):
    return {'is_choice': games[game_id].players[0].options != None}
    
@app.route("/getoptions/<int:game_id>/")
def get_options(game_id):
    return games[game_id].players[0].options

@app.route("/findcards/<int:game_id>/")
#TODO
def find_cards(game_id):

    return {'res': games[game_id].find_card_objs([1, 2, 3, 4])}

# Does not always work for some reason, I will look at it
@app.route("/calculatescore/<int:game_id>/")
def calculate_score(game_id):
    game = games[game_id]
    res = {}
    for i in range(len(game.players)):
        score = 0
        player = game.players[i]
        cards = player.deck + player.hand + player.in_play + player.discard
        for c in cards:
            if(c['name'] == 'estate'):
                score += 1
            if(c['name'] == 'duchy'):
                score += 3
            if(c['name'] == 'province'):
                score += 6
            if(c['name'] == "gardens"):
                score += (len(cards)//10)
        res[i] = score
    return res

@app.route("/deckcomposition/<int:game_id>/")
def deck_composition(game_id, player=0):
    game = games[game_id]
    player = game.players[player]
    cards = player.deck + player.hand + player.in_play + player.discard
    deck_comp = {}
    for card in cards:
        if card['name'] in deck_comp:
            deck_comp[card['name']] += 1
        else:
            deck_comp[card['name']] = 1
    return deck_comp

@app.route("/deckcompositions/<int:game_id>/")
def deck_compositions(game_id):
    game = games[game_id]
    res = {}
    for i in range(len(game.players)):
        player = game.players[i]
        cards = player.deck + player.hand + player.in_play + player.discard
        deck_comp = {}
        for card in cards:
            if card['name'] in deck_comp:
                deck_comp[card['name']] += 1
            else:
                deck_comp[card['name']] = 1
        res[i] = deck_comp
    return res

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    Game()
