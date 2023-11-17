from flask import Flask, request, redirect, url_for, render_template
from game import Game
import random, json
import requests
import psycopg2
from card_scripting import cardPlayer, cards, commands, cardParser
from player import player
import aiplayer

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

@app.route("/cardbought/<int:game_id>/<int:player_id>/<card_name>/")
def card_bought(game_id, player_id, card_name):
    game = games[game_id]
    # game.gamestateID += 1
    player = game.currentPlayer
    if player_id != player.id:
        return "Nice try"
    player_number = game.get_player_number(player_id)
    game.update_all_players(f'{player_number}_discard_size', len(player.discard) + 1)
    cost = cards.getCard(card_name)['cost']
    if player.coins >= cost and player.buys >= 1 and player.phase == 'buy':
        card = game.make_card(card_name)
        player.discard.append(card)
        player.coins -= cost
        game.update_all_players('set_coins', player.coins)
        player.buys -= 1
        game.update_all_players('set_buys', player.buys)
        game.supplySizes[card_name] -= 1
        game.update_all_players('cardbought', ' '.join(card_name.split('_')).title())

        
    return "hi"  # nothing actually needs to be returned, flask crashes without this.

@app.route("/cardplayed/<int:game_id>/<int:player_id>/<int:card_id>/")
def card_played(game_id, card_id, player_id):
    game = games[game_id]
    # game.gamestateID += 1
    player = game.currentPlayer
    if player_id != player.id:
        return "not current player"
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
                game.update_all_players('set_actions', player.actions)
            else:
                return "hi"
        player.in_play.append(card)
        removed_card = player.hand.pop(idx)
        player.update_list('remove', removed_card)
        game.update_all_players(f'{game.get_player_number(player.id)}_hand_size', len(player.hand))
        game.update_list_all_players('play', card['name'])
        player.set_command(cards.getCardText(card['name']))
        res = player.execute_command()
        if res == "yield":
            player.updates['select'] = True
            return {'yield': True}

    return {'yield': False}

# TODO is this used?
@app.route("/gethand/<int:game_id>/")
def get_hand(game_id):
    return str(games[game_id].currentPlayer.hand)

@app.route("/getgamestate/<int:game_id>/")
def getgamestate(game_id):
    game = games[game_id]
    player = game.currentPlayer
    state = {"hand": player.hand, "discard": player.discard, "in_play": player.in_play, "deck": player.deck,
             "phase": player.phase, "actions": player.actions, "buys": player.buys, "coins": player.coins,
             "supply": game.supply, "supplySizes": game.supplySizes}
    return state


@app.route("/getfrontstate/<int:game_id>/<int:playerid>/")
def getfrontstate(game_id, playerid):
    game = games[game_id]
    player = game.players[game.get_player_number(playerid) - 1]
    currentPlayer = game.currentPlayer
    state = {"hand": player.hand, "discard": player.discard, "in_play": currentPlayer.in_play, "phase": currentPlayer.phase,
             "actions": currentPlayer.actions, "buys": currentPlayer.buys, "coins": currentPlayer.coins, "supply": game.supply,
             "supplySizes": game.supplySizes, "deckSize": len(currentPlayer.deck)}
    return state

@app.route("/getdeckinfo/<int:game_id>/<int:player_id>")
def get_deck_info(game_id, player_id):
    game = games[game_id]
    player_num = game.get_player_number(player_id) - 1
    deck_info = [
        f'Your Deck: {str(len(game.players[player_num].deck))} cards',
        f'Your Discard: {str(len(game.players[player_num].discard))} cards'
    ]
    for i in range(len(game.players)):
        if i != player_num:
            deck_info.append(f"Player {i + 1}'s deck: {str(len(game.players[i].deck))} cards")
            deck_info.append(f"Player {i + 1}'s hand: {str(len(game.players[i].hand))} cards")
            deck_info.append(f"Player {i + 1}'s discard: {str(len(game.players[i].discard))} cards")
    deck_info.append(player_num + 1)
    return deck_info

@app.route('/changeVar/', methods=['POST'])
def change_var():
    req = request.get_json()
    gameID = req['gameID']
    var = req['var']
    delta = int(req['delta'])
    game = games[gameID]
    player = game.currentPlayer
    game.gamestateID += 1
    if var == "actions":
        player.actions += delta
        game.update_all_players('set_actions', player.actions)
    elif var == "buys":
        player.buys += delta
        game.update_all_players('set_buys', player.buys)
    elif var == "coins":
        player.coins += delta
        game.update_all_players('set_coins', player.coins)
    else:
        raise ValueError("Invalid variable name")
    return 'Changed variable' # nothing actually needs to be returned, flask crashes without this.

@app.route('/changeZone/', methods=['POST'])
def change_zone():
    req = request.get_json()
    gameID = req['gameID']
    game = games[gameID]
    # game.gamestateID += 1
    player = game.currentPlayer
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
                player.update_list('remove', removed)
                game.update_all_players(f'{game.get_player_number(player.id)}_hand_size', len(player.hand))
            if card_loc[0] == player.deck:
                game.update_all_players(f'{game.get_player_number(player.id)}_deck_size', len(player.hand))
            if card_loc[0] == player.discard:
                game.update_all_players(f'{game.get_player_number(player.id)}_discard_size', len(player.hand))
            player.updates[f'{zone}_size'] = len(dest) + 1
        if dest == player.hand:
            player.update_list('add', card)
            game.update_list_all_players(f'{game.get_player_number(player.id)}_hand_size', len(player.hand) + 1)
        dest.append(card)

    return 'Changed zone'



@app.route('/endphase/<int:game_id>/<int:player_id>/')
def endphase(game_id, player_id):
    if game_id >= len(games):
        return "hi"
    game = games[game_id]
    player = game.currentPlayer
    if player_id != player.id:
        return "Nice try"

    if player.phase == "action":
        player.phase = "buy"
        game.update_all_players('set_phase', 'buy')
    elif player.phase == "buy":
        player.end_turn()
        game.currentPlayer = game.players[game.get_player_number(player.id) % len(game.players)]
        game.update_all_players('set_phase', 'action')
        game.update_all_players('set_actions', 1)
        game.update_all_players('set_buys', 1)
        game.update_all_players('set_coins', 0)
        game.update_all_players('new_turn', True)
        game.first_turn_ended = True
        if game.is_computer_game and game.currentPlayer == game.players[1]:
            aiplayer.take_turn(game.currentPlayer)
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
    games[game_id].currentPlayer.draw_cards(num_cards)
    return 'hello world' # nothing actually needs to be returned, flask crashes without this.

@app.route("/newgame/")
def new_game():
    
    global num_games
    global games
    games.append(Game(num_games, 2))
    num_games += 1
    game = games[-1]
    game.players[0].updates['new_game_prompt'] = True
    return {
        'game_id': str(game.id),
        'player_id': game.players[0].id
            }

@app.route('/joingame/<int:game_id>/')
def join_game(game_id):
    game = games[game_id]
    if game.first_turn_ended or not game.is_computer_game:
        return 'no lol'
    game.is_computer_game = False
    return str(game.players[1].id)

@app.route('/<int:game_id>/turnnumber/')
def turn_number(game_id):
    game = games[game_id]
    return str(game.get_player_number(game.currentPlayer.id))

@app.route("/selected/<int:game_id>/", methods=['POST'])
def selected(game_id):
    req = request.get_json()
    ids = req['ids']
    game = games[game_id]
    if 'player' in req:
        player = game.players[req['player']]
    else:
        player = game.currentPlayer
    player.options = None
    cards = game.find_card_objs(ids)
    #raise ValueError(str(game.floatingCards))
    player.cmd.setPlayerInput(cards)
    #res = player.cmd.execute()
    res = player.execute_command()
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
        player = game.currentPlayer

    if req['n'] != 0 and len(req['options']) > 0:
        player.options = req
    else:
        player.cmd.setPlayerInput([])
    return "hello world" # nothing actually needs to be returned, flask crashes without this.

# TODO fix
# @app.route("/ischoice/<int:game_id>/<int:player_id>")
# def ischoice(game_id, player_id):
#     return {'is_choice': games[game_id].players[games[game_id].get_player_number(player_id) - 1].options is not None}
    
@app.route("/getoptions/<int:game_id>/<int:player_id>/")
def get_options(game_id, player_id):
    game = games[game_id]
    player_options = game.players[game.get_player_number(player_id) - 1].options
    return player_options if player_options is not None else {}

@app.route("/findcards/<int:game_id>/")
def find_cards(game_id):

    return {'res': games[game_id].find_card_objs([1, 2, 3, 4])}


@app.route("/updates/<int:game_id>/<int:player_id>")
def updates(game_id, player_id):
    game = games[game_id]
    update_list = game.players[game.get_player_number(player_id) - 1].updates
    game.players[game.get_player_number(player_id) - 1].updates = {}
    return update_list

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
        player.set_command(multicommand)
        #player.cmd = cardParser.multicommand(multicommand, game_id)
        #res = player.cmd.execute()
        player.execute_command()
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
        CREATE TABLE IF NOT EXISTS Games
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
        count = 0
        savehand = "{"
        for s in hand[x].keys():
            for y in range(hand[x][s]):
                savehand += s + ","
                count += 1
        for x in range(20-count):
            savehand+= "fake,"
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
    cur.execute("INSERT INTO Games (ID,NAME) VALUES (% s,'% s')" % (game_id, handlists))
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


@app.route("/debug/<int:game_id>/")
def debug(game_id):
    player = games[game_id].players[0]
    cmd = player.cmd
    return {'cmds': [com.command for com in cmd.commands], 'cmdStack': [[com.command for com in cmd.commands] for cmd in player.cmd_stack]}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    Game()
