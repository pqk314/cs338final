from flask import Flask, request, redirect, url_for, render_template
from game import Game
import random, json
import requests

from card_scripting import cardPlayer, cards
from player import player

app = Flask(__name__)
num_games = 0
games = []


        


@app.route("/cardbought/<int:game_id>/<card_name>/")
def card_bought(game_id, card_name):
    game = games[game_id]
    game.gamestateID += 1
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
    game.gamestateID += 1
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
    game = games[gameID]
    player = game.players[0]
    game.gamestateID += 1
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
    game.gamestateID += 1
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
    game.gamestateID += 1
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
    
    global num_games
    global games
    games.append(Game(num_games, 2))
    num_games += 1
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
    game.gamestateID += 1
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
    game = games[game_id]
    return game.players[0].options

@app.route("/findcards/<int:game_id>/")
#TODO
def find_cards(game_id):

    return {'res': games[game_id].find_card_objs([1, 2, 3, 4])}


@app.route("/gamestateID/<int:game_id>/")
def gamestate_id(game_id):
    return str(games[game_id].gamestateID)

# Does not always work for some reason, I will look at it
@app.route("/calculatescore/<int:game_id>/")
def calculate_score(game_id):
    game = games[game_id]
    scores = {}
    for i in range(len(game.players)):
        player = game.players[i]
        scores[i] = player.calculate_score()
    return scores

@app.route("/deckcomposition/<int:game_id>/")
def deck_composition(game_id, player=0):
    game = games[game_id]
    player = game.players[player]
    return player.get_deck_composition()

@app.route("/deckcompositions/<int:game_id>/")
def deck_compositions(game_id):
    game = games[game_id]
    decks = {}
    for i in range(len(game.players)):
        player = game.players[i]
        decks[i] = player.get_deck_composition()
    return decks

@app.route("/gameexists/<int:game_id>/")
def game_exists(game_id):
    return {'exists': game_id < num_games}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    Game()
