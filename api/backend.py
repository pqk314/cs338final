from flask import Flask, request, redirect, url_for, render_template
from game import Game
import random, json
import requests
import psycopg2
from card_scripting import cardPlayer, cards, commands, cardParser
from player import player

app = Flask(__name__)
num_games = 0
games = []



DB_NAME = "docker"
DB_USER = "docker"
DB_PASS = "docker"
DB_HOST = "db"
DB_PORT = "5432"

def find_card_in_list(list, card_id):
    for idx, card in enumerate(list):
        if card['id'] == card_id:
            return idx
    return -1


def update_cards(add_or_remove, card, player, game):
    """Adds cards to game.updates, basically facilitates having a dictionary for simplicity's sake."""
    if add_or_remove in game.updates:
        game.updates[add_or_remove].append(card)
    else:
        game.updates[add_or_remove] = [card]


@app.route("/cardbought/<int:game_id>/<card_name>/")
def card_bought(game_id, card_name):
    game = games[game_id]
    # game.gamestateID += 1
    player = game.players[0]
    game.updates['discard_size'] = len(player.discard) + 1
    cost = cards.getCard(card_name)['cost']
    if player.coins >= cost and player.buys >= 1 and player.phase == 'buy':
        card = game.make_card(card_name)
        player.discard.append(card)
        player.coins -= cost
        game.updates['set_coins'] = player.coins
        player.buys -= 1
        game.updates['set_buys'] = player.buys
        # TODO updates for this
        game.supplySizes[card_name] -= 1

        
    return "hi"  # nothing actually needs to be returned, flask crashes without this.

@app.route("/cardplayed/<int:game_id>/<int:card_id>/")
def card_played(game_id, card_id):
    game = games[game_id]
    # game.gamestateID += 1
    player = game.players[0]
    hand = player.hand

    idx = find_card_in_list(hand, card_id)

    if idx == -1:
        raise ValueError
    
    card = player.hand[idx]
    type = card['type']
    if (type == 'action' and player.phase == 'action') or (type == 'treasure' and player.phase == 'buy'):
        if type == 'action':
            if player.actions >= 1:
                player.actions -= 1
                game.updates['set_actions'] = player.actions
            else:
                return "hi"
        player.in_play.append(card)
        removed_card = player.hand.pop(idx)
        update_cards('remove', removed_card, player, game)
        cmd = cardPlayer.getCardCmd(game_id, card['name'])
        player.cmd = cmd
        res = cmd.execute()
        if res == "yield":
            game.updates['select'] = True
            return {'yield': True}

    return {'yield': False}


@app.route("/gethand/<int:game_id>/")
def get_hand(game_id):
    return str(games[game_id].players[0].hand)

@app.route("/getgamestate/<int:game_id>/")
def getgamestate(game_id):
    game = games[game_id]
    player = game.players[0]
    state = {"hand": player.hand, "discard": player.discard, "in_play": player.in_play, "deck": player.deck,
             "phase": player.phase, "actions": player.actions, "buys": player.buys, "coins": player.coins,
             "supply": game.supply, "supplySizes": game.supplySizes}
    return state


@app.route("/getfrontstate/<int:game_id>/")
def getfrontstate(game_id):
    game = games[game_id]
    player = game.players[0]
    state = {"hand": player.hand, "discard": player.discard, "in_play": player.in_play, "phase": player.phase,
             "actions": player.actions, "buys": player.buys, "coins": player.coins, "supply": game.supply,
             "supplySizes": game.supplySizes}
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
        game.updates['set_actions'] = player.actions
    elif var == "buys":
        player.buys += delta
        game.updates['set_buys'] = player.buys
    elif var == "coins":
        player.coins += delta
        game.updates['set_coins'] = player.coins
    else:
        raise ValueError("Invalid variable name")
    return 'Changed variable' # nothing actually needs to be returned, flask crashes without this.

@app.route('/changeZone/', methods=['POST'])
def change_zone():
    req = request.get_json()
    gameID = req['gameID']
    game = games[gameID]
    # game.gamestateID += 1
    player = game.players[0]
    cards = req['cards']
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
    for card in cards:
        card_id = card['id']
        card_loc = player.find_card(card_id)
        if card_loc[1] != -1:
            removed = card_loc[0].pop(card_loc[1])
            if card_loc[0] == player.hand:
                update_cards('remove', removed, player, game)
            # TODO subtract one figure out how this works
            game.updates[f'{zone}_size'] = len(dest) + 1
        if dest == player.hand:
            update_cards('add', card, player, game)
        dest.append(card)

    return 'Changed zone'



@app.route('/endphase/<int:game_id>/')
def end_phase(game_id):
    game = games[game_id]
    # game.gamestateID += 1
    player = game.players[0]
    if player.phase == "action":
        player.phase = "buy"
        game.updates['set_phase'] = 'buy'
    elif player.phase == "buy":
        player.end_turn()
        game.players.append(game.players.pop(0))
        game.updates['set_phase'] = 'action'
    return "ended phase"

@app.route("/getsupply/<int:game_id>/")
def get_supply(game_id):
    game = games[game_id]
    #return {'store': [game.make_card('curse')]}
    cards = [game.make_card(name) for name, val in game.supplySizes.items() if val > 0]
    game.floatingCards += cards
    return {"store": cards}

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
    #raise ValueError(str(game.floatingCards))
    player.cmd.setPlayerInput(cards)
    res = player.cmd.execute()

    if res == "yield":
        return "yield"

    return "Hello World!"

@app.route("/setoptions/<int:game_id>/", methods=['POST'])
def set_options(game_id):
    # TODO what does this do?
    game = games[game_id]
    # game.gamestateID += 1
    req = request.get_json()
    if 'player' in req:
        player = game.players[req['player']]
        del req['player']
    else:
        player = game.players[0]

    if req['n'] > 0 and len(req['options']) > 0:
        player.options = req
    else:
        player.cmd.setPlayerInput([])
    return "hello world" # nothing actually needs to be returned, flask crashes without this.

@app.route("/ischoice/<int:game_id>/")
def ischoice(game_id):
    return {'is_choice': games[game_id].players[0].options != None}
    
@app.route("/getoptions/<int:game_id>/")
def get_options(game_id):
    game = games[game_id]
    return game.players[0].options if game.players[0].options is not None else {}

@app.route("/findcards/<int:game_id>/")
#TODO
def find_cards(game_id):

    return {'res': games[game_id].find_card_objs([1, 2, 3, 4])}


@app.route("/updates/<int:game_id>/")
def updates(game_id):
    updates = games[game_id].updates
    games[game_id].updates = {}
    return updates

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

# used
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

@app.route("/attack/", methods=['POST'])
def attack():
    req = request.get_json()
    game_id = req['gameID']
    game = games[game_id]
    multicommand = req['multicommand']
    for player in game.players[1:]:
        player.cmd = cardParser.multicommand(multicommand, game_id)
        #res = player.cmd.execute()
        player.cmd.execute()
    return "yield"
        

@app.route("/makecard/<int:game_id>/<card_name>/")
def make_card(game_id, card_name):
    game = games[game_id]
    if game.supplySizes[card_name] == 0:
        return {'empty': True}
    game.supplySizes[card_name] -= 1
    card = game.make_card(card_name)
    game.floatingCards.append(card)
    
    return card




@app.route("/createtable/")
def createtable():
    try:
        conn = psycopg2.connect(database=DB_NAME,
                            user=DB_USER,
                            password=DB_PASS,
                            host=DB_HOST,
                            port=DB_PORT)

        cur = conn.cursor()  # creating a cursor
 
        # executing queries to create table
        cur.execute("""
        CREATE TABLE Games
        (
            ID INT   PRIMARY KEY NOT NULL,
            NAME TEXT[][]
        )
        """)
        
        # commit the changes
        conn.commit()
        print("Table Created successfully")

    except:
        print("Database not connected successfully")
    return "hi"


@app.route("/save/<int:game_id>/")
def save(game_id):
    game = games[game_id]
    decks = deck_compositions(game_id)

    hand = []
    # change for multiple players
    for h in range(len(decks)):
        hand.append(decks[h])
    
    handlists = "{"
    for x in range(len(hand)):
        savehand = "{"
        for s in hand[x].keys():
            for y in range(hand[x][s]):
                savehand += s + ","
        savehand = savehand[:len(savehand)-1]
        savehand += "}"
        handlists += savehand + ","
    handlists = handlists[:len(handlists)-1]
    handlists += "}"


    conn = psycopg2.connect(database=DB_NAME,
                            user=DB_USER,
                            password=DB_PASS,
                            host=DB_HOST,
                            port=DB_PORT)
    cur = conn.cursor()
    cur.execute("INSERT INTO Games (ID,NAME) VALUES ('% s','% s')" % (game_id, handlists))
    conn.commit()
    return "hi"

# returns a list that conatins all of the cards in the first player's hand
@app.route("/dbget/<int:game_id>")
def dbget(game_id):
    returnjson = {'deck':""}
    # getting the people back
    conn = psycopg2.connect(database=DB_NAME,
                        user=DB_USER,
                        password=DB_PASS,
                        host=DB_HOST,
                        port=DB_PORT)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Games")
    rows = cur.fetchall()
    game = rows[game_id]
    # game should be of the form (0, ['copper', 'cellar', 'copper', 'copper', 'copper']) 
    handlist = game[1]
    # handlist is a list
    
    
    conn.close()
    # due to multihands
    returnjson['deck'] = handlist[0]
    return returnjson


# This is the endpoint we need completed
# This returns a [game1, game2, game3] where gamex = [play1hand, player2hand, player3hand] where playerxhand = ['copper', 'cellar']
@app.route("/getstats/")
def getstats():
    ans = []

    conn = psycopg2.connect(database=DB_NAME,
                        user=DB_USER,
                        password=DB_PASS,
                        host=DB_HOST,
                        port=DB_PORT)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Games")
    rows = cur.fetchall()

    # like a list of game = rows[game_id]
    for r in rows:
        ans.append(r[1]) 

    # game = rows[game_id]
    # game should be of the form (0, ['copper', 'cellar', 'copper', 'copper', 'copper']) 
    # handlist = game[1]
    # handlist is a list

    conn.close()
    rtn = {'deck': ans}
    return rtn


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    Game()
