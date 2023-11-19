from flask import Flask, request
from game import Game
import psycopg2
from card_scripting import cards
import aiplayer

app = Flask(__name__)

num_games = 0
starting_num = 0
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
    if game_over(game_id)['game_over']:
        return 'game_ended'
    game = games[game_id - starting_num]
    # game.gamestateID += 1
    player = game.currentPlayer
    if player_id != player.id:
        return "Nice try"
    player_number = game.get_player_number(player_id)
    game.update_all_players(f'{player_number}_discard_size', len(player.discard) + 1)
    cost = cards.getCard(card_name)['cost']
    if player.coins >= cost and player.buys >= 1 and player.phase == 'buy' and game.supplySizes[card_name] > 0:
        card = game.make_card(card_name)
        player.discard.append(card)
        player.coins -= cost
        game.update_all_players('set_coins', player.coins)
        player.buys -= 1
        game.update_all_players('set_buys', player.buys)
        game.supplySizes[card_name] -= 1
        for player in game.players:
            if player != game.currentPlayer:
                player.set_text(f"Player {game.get_player_number(player_id)} bought a {(' '.join(card_name.split('_')).title())}.")
            else:
                player.set_text("Left click a card to play it.")

        
    return "hi"  # nothing actually needs to be returned, flask crashes without this.

@app.route("/cardplayed/<int:game_id>/<int:player_id>/<int:card_id>/")
def card_played(game_id, card_id, player_id):
    if game_over(game_id)['game_over']:
        return 'game_ended'
    game = games[game_id - starting_num]
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

@app.route("/getfrontstate/<int:game_id>/<int:playerid>/")
def getfrontstate(game_id, playerid):
    game = games[game_id - starting_num]
    player = game.players[game.get_player_number(playerid) - 1]
    currentPlayer = game.currentPlayer
    state = {"hand": player.hand, "in_play": currentPlayer.in_play, "phase": currentPlayer.phase,
             "actions": currentPlayer.actions, "buys": currentPlayer.buys, "coins": currentPlayer.coins,
             "supply": game.supply, "supplySizes": game.supplySizes, "deckSize": len(currentPlayer.deck),
             "barrier": player.barrier, "text": player.text}
    return state

@app.route("/getdeckinfo/<int:game_id>/<int:player_id>")
def get_deck_info(game_id, player_id):
    game = games[game_id - starting_num]
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

@app.route('/endphase/<int:game_id>/<int:player_id>/')
def endphase(game_id, player_id):
    if not game_exists(game_id)['exists']:
        return "hi"
    game = games[game_id - starting_num]
    player = game.currentPlayer
    if player_id != player.id:
        return "Nice try"

    if player.phase == "action":
        player.phase = "buy"
        game.update_all_players('set_phase', 'buy')
    elif player.phase == "buy":
        player.end_turn()
        if check_game_over(game):
            return 'game over'
        game.currentPlayer = game.players[game.get_player_number(player.id) % len(game.players)]
        game.update_all_players('set_phase', 'action')
        game.update_all_players('set_actions', 1)
        game.update_all_players('set_buys', 1)
        game.update_all_players('set_coins', 0)
        for player in game.players:
            player.set_barrier(f'It is Player {game.get_player_number(game.currentPlayer.id)}\'s turn.')
        game.currentPlayer.set_barrier('')
        game.update_all_players('new_turn', True)
        game.first_turn_ended = True
        if game.is_computer_game and game.currentPlayer == game.players[1]:
            aiplayer.take_turn(game.currentPlayer)
    return "ended phase"

def check_game_over(game):
    '''only called at end of turn and can end game'''
    if game.is_over:
        return True
    empty_piles = 0
    for val in game.supplySizes.values():
        if val == 0:
            empty_piles += 1
    if empty_piles >= 3 or game.supplySizes['province'] == 0:
        game.is_over = True
        return True
    return False

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
    game = games[game_id - starting_num]
    if game.first_turn_ended or not game.is_computer_game:
        return 'no lol'
    game.is_computer_game = False
    return str(game.players[1].id)

@app.route('/<int:game_id>/turnnumber/')
def turn_number(game_id):
    game = games[game_id - starting_num]
    return str(game.get_player_number(game.currentPlayer.id))

@app.route("/selected/<int:game_id>/", methods=['POST'])
def selected(game_id):
    req = request.get_json()
    ids = req['ids']
    game = games[game_id - starting_num]
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
    
@app.route("/getoptions/<int:game_id>/<int:player_id>/")
def get_options(game_id, player_id):
    game = games[game_id - starting_num]
    player_options = game.players[game.get_player_number(player_id) - 1].options
    return player_options if player_options is not None else {}


@app.route("/updates/<int:game_id>/<int:player_id>")
def updates(game_id, player_id):
    if not game_exists(game_id)['exists']:
        return {'home_page': True}
    game = games[game_id - starting_num]
    if game.is_over:
        return {'game_over': True}
    update_list = game.players[game.get_player_number(player_id) - 1].updates
    game.players[game.get_player_number(player_id) - 1].updates = {}
    return update_list

def calculate_score(game_id):
    game = games[game_id - starting_num]
    scores = []
    for i in range(len(game.players)):
        player = game.players[i]
        scores.append(player.calculate_score())
    return scores

def deck_composition(deck):
    deck_comp = {}
    for card in deck:
        if card == 'fake':
            continue
        if card in deck_comp:
            deck_comp[card] += 1
        else:
            deck_comp[card] = 1
    return deck_comp

@app.route("/gameexists/<int:game_id>/")
def game_exists(game_id):
    return {'exists': num_games > game_id >= starting_num}

@app.route('/gameisover/<int:game_id>/')
def game_over(game_id):
    """different from check_game_over because this can't end the game."""
    return {'game_over': games[game_id - starting_num].is_over}

# TODO possibly delete
@app.route("/attack/", methods=['POST'])
def attack():
    req = request.get_json()
    game_id = req['gameID']
    game = games[game_id - starting_num]
    multicommand = req['multicommand']
    for player in game.players[1:]:
        player.set_command(multicommand)
        #player.cmd = cardParser.multicommand(multicommand, game_id)
        #res = player.cmd.execute()
        player.execute_command()
    return "yield"

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
            ID BIGINT   PRIMARY KEY NOT NULL,
            DECK TEXT[][],
            VP BIGINT[]
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
    game = games[game_id - starting_num]
    if game.db_id != -1:
        return str(game.db_id)
    decks = []
    for player in game.players:
        decks.append(sorted(player.deck + player.discard + player.hand + player.in_play, key=lambda card: card['name']))

    hand_lists = "{"
    for deck in decks:
        savehand = "{"
        for i in range(len(max(decks, key=len))):
            if i < len(deck):
                savehand += f"{deck[i]['name']},"
            else:
                savehand += 'fake,'
        savehand = savehand[:-1]
        savehand += "}"
        hand_lists += savehand + ","
    hand_lists = hand_lists[:-1]
    hand_lists += "}"


    conn = psycopg2.connect(database=DB_NAME,
                            user=DB_USER,
                            password=DB_PASS,
                            host=DB_HOST,
                            port=DB_PORT)
    cur = conn.cursor()
    id = get_num_games()
    vps = f'{{{str(calculate_score(game_id))[1:-1]}}}'
    cur.execute("INSERT INTO Games (ID,DECK,VP) VALUES (% s,'% s', '%s')" % (id, hand_lists, vps))
    conn.commit()
    conn.close()
    game.db_id = id
    return str(id)

# returns a list that conatins all of the cards in the first player's hand
@app.route("/dbget/<int:game_id>/")
def dbget(game_id):
    returnjson = {'deck':""}
    # getting the people back
    conn = psycopg2.connect(database=DB_NAME,
                        user=DB_USER,
                        password=DB_PASS,
                        host=DB_HOST,
                        port=DB_PORT)
    cur = conn.cursor()
    cur.execute("SELECT DECK, VP FROM Games WHERE ID=%s", (game_id,))
    rows = cur.fetchall()
    game = rows[0]
    # game should be of the form (0, ['copper', 'cellar', 'copper', 'copper', 'copper']) 
    # handlist is a list

    conn.close()
    # due to multihands
    returnjson['deck'] = game
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

    conn.close()
    rtn = {'deck': ans}
    return rtn

def get_num_games():
    conn = psycopg2.connect(database=DB_NAME,
                            user=DB_USER,
                            password=DB_PASS,
                            host=DB_HOST,
                            port=DB_PORT)
    cur = conn.cursor()
    cur.execute("SELECT count(ID) FROM Games")
    return cur.fetchone()[0]

# return decks = {i:{estate:1}} where i is player num and {} is their deck comp
@app.route("/getgame/<int:game_id>")
def getgame(game_id):
    ans = {}
    deck_comps = []
    table = dbget(game_id)['deck']
    hands = table[0]
    print(hands)
    vps = table[1]

    for deck in hands:
        deck_comps.append(deck_composition(deck))

        ans['deck_comps'] = deck_comps
        ans['score'] = vps
        
    return ans


@app.route("/debug/<int:game_id>/")
def debug(game_id):
    player = games[game_id - starting_num].players[0]
    cmd = player.cmd
    return {'cmds': [com.command for com in cmd.commands], 'cmdStack': [[com.command for com in cmd.commands] for cmd in player.cmd_stack]}


if __name__ == "__main__":
    createtable()
    starting_num = get_num_games()
    num_games = starting_num
    
    app.run(host="0.0.0.0", port=5000)
