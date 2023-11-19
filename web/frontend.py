from flask import Flask
from flask import render_template, url_for, redirect, request
import requests
import tutorial_executer

app = Flask(__name__)
card_pics = None


def get_card_pics():
    """Returns card_pics so that it can be used in multiple functions. Flask doesn't let this be statically declared, so
    this is the way we chose to do it."""
    global card_pics
    if card_pics is None:
        card_pics = {
            "copper": url_for('static', filename='images/372px-Copper.jpg'),
            "silver": url_for('static', filename='images/375px-Silver.jpg'),
            "gold": url_for('static', filename='images/375px-Gold.jpg'),
            "estate": url_for('static', filename='images/373px-Estate.jpg'),
            "duchy": url_for('static', filename='images/372px-Duchy.jpg'),
            "province": url_for('static', filename='images/375px-Province.jpg'),
            "curse": url_for('static', filename='images/372px-Curse.jpg'),
            "moat": url_for('static', filename='images/372px-Moat.jpg'),
            "vassal": url_for('static', filename='images/372px-Vassal.jpg'),
            "cellar": url_for('static', filename='images/373px-Cellar.jpg'),
            "laboratory": url_for('static', filename='images/373px-Laboratory.jpg'),
            "library": url_for('static', filename='images/373px-Library.jpg'),
            "merchant": url_for('static', filename='images/373px-Merchant.jpg'),
            "remodel": url_for('static', filename='images/373px-Remodel.jpg'),
            "sentry": url_for('static', filename='images/373px-Sentry.jpg'),
            "smithy": url_for('static', filename='images/373px-Smithy.jpg'),
            "village": url_for('static', filename='images/373px-Village.jpg'),
            "witch": url_for('static', filename='images/373px-Witch.jpg'),
            "workshop": url_for('static', filename='images/373px-Workshop.jpg'),
            "bandit": url_for('static', filename='images/374px-Bandit.jpg'),
            "bureaucrat": url_for('static', filename='images/374px-Bureaucrat.jpg'),
            "harbinger": url_for('static', filename='images/374px-Harbinger.jpg'),
            "market": url_for('static', filename='images/374px-Market.jpg'),
            "militia": url_for('static', filename='images/374px-Militia.jpg'),
            "mine": url_for('static', filename='images/374px-Mine.jpg'),
            "moneylender": url_for('static', filename='images/374px-Moneylender.jpg'),
            "poacher": url_for('static', filename='images/374px-Poacher.jpg'),
            "throne_room": url_for('static', filename='images/374px-Throne_Room.jpg'),
            "artisan": url_for('static', filename='images/375px-Artisan.jpg'),
            "chapel": url_for('static', filename='images/375px-Chapel.jpg'),
            "council_room": url_for('static', filename='images/375px-Council_Room.jpg'),
            "festival": url_for('static', filename='images/375px-Festival.jpg'),
            "gardens": url_for('static', filename='images/375px-Gardens.jpg')
        }
    return card_pics


@app.route("/")
def home_page():
    """Displays home page to users."""
    pics = get_card_pics()
    return render_template("home-page.html", card_pics=pics)


@app.route("/newgame/")
def new_game():
    """makes a new game and redirects user to their new game"""
    game_info = requests.request("get", "http://api:5000/newgame").json()
    # requests.get(f"http://api:5000/createtable/")
    return redirect(f'/{game_info["game_id"]}/{game_info["player_id"]}/')

@app.route('/joingame/<int:game_id>')
def join_game(game_id):
    """Allows player to join game with the requested ID. Autofills the user ID to allow for a harder to guess user ID"""
    try:
        player_id = int(requests.request("get", f"http://api:5000/joingame/{game_id}").text)
    except ValueError:
        return redirect('/')
    return redirect(f'/{game_id}/{player_id}/')


@app.route("/<int:game_id>/<int:player_id>/")
def game_page(game_id, player_id):
    """Checks that game exists and is still going. If a selection is occuring, it tells the front end to prepare for it.
    It gets the info needed for the front end"""
    exists = requests.get(f"http://api:5000/gameexists/{game_id}").json()['exists']
    is_over = requests.request("get", f"http://api:5000/gameisover/{game_id}/").json()['game_over']
    if not exists or is_over:
        return redirect(url_for("home_page"))
    select_info = select_cards(game_id, player_id)
    select_info = None if len(select_info.keys()) == 0 else select_info

    # Gets info like cards in hand or cards in play.
    gamestate = requests.request("get", f"http://api:5000/getfrontstate/{game_id}/{player_id}").json()

    # Gets player's deck/hand/discard size to display along with the number associated with a player's id
    deck_info = requests.request("get", f"http://api:5000/getdeckinfo/{game_id}/{player_id}").json()
    player_num = deck_info.pop()

    # This takes gamestate info and puts it in a more convenient package
    turn_info = {'Money': gamestate['coins'], 'Actions': gamestate['actions'], 'Buys': gamestate['buys']}
    cards = gamestate["hand"]
    in_play = gamestate['in_play']
    end_what = f"End {gamestate['phase'].title()}"
    text = gamestate['text']
    barrier = gamestate['barrier']

    pics = get_card_pics()
    return render_template("game.html", hand=cards, in_play=in_play, images=pics,
                           turn_info=turn_info, end_what=end_what, game_id=game_id, deck_info=deck_info,
                           select_info=select_info, player_num=player_num, barrier=barrier, text=text)

@app.route('/<int:game_id>/turnnumber/')
def turn_number(game_id):
    """Returns the number associated with the player who is currently taking a turn"""
    return requests.request("get", f"http://api:5000/{game_id}/turnnumber/").text

@app.route("/<int:game_id>/<int:player_id>/supply")
def supply(game_id, player_id):
    """Loads the supply page with the appropriate cards for whatever game_id is passed"""
    exists = requests.get(f"http://api:5000/gameexists/{game_id}").json()['exists']
    is_over = requests.request("get", f"http://api:5000/gameisover/{game_id}/").json()['game_over']
    if not exists or is_over:
        return redirect(url_for("home_page"))
    pics = get_card_pics()

    # gamestate is used for what cards are in supply and how many of them there are.
    gamestate = requests.request("get", f"http://api:5000/getfrontstate/{game_id}/{player_id}").json()
    cards = gamestate['supply']
    turn_info = {'Money': gamestate['coins'], 'Actions': gamestate['actions'], 'Buys': gamestate['buys']}
    end_what = f"End {gamestate['phase'].title()}"
    remaining_cards = gamestate['supplySizes']
    return render_template("supply.html", cards=cards, card_pics=pics, turn_info=turn_info, end_what=end_what, remaining_cards = remaining_cards)


@app.route("/<int:game_id>/<int:player_id>/cardbought/<card_id>/")
def card_bought(game_id, player_id, card_id):
    """process for buying cards"""
    requests.request("get", f"http://api:5000/cardbought/{game_id}/{player_id}/{card_id}")
    return redirect(f'/{game_id}/{player_id}/supply')


@app.route("/<int:game_id>/<int:player_id>/cardplayed/<card_id>/")
def card_played(game_id, player_id, card_id):
    """process for playing cards"""
    requests.request("get", f"http://api:5000/cardplayed/{game_id}/{player_id}/{card_id}")
    return redirect(f'/{game_id}/{player_id}')

@app.route("/<int:game_id>/<int:player_id>/endphase/")
def end_phase(game_id, player_id):
    """ends current phase"""
    if requests.request("get", f"http://api:5000/gameisover/{game_id}/").json()['game_over']:
        return redirect(url_for('game_over', game_id=game_id, player_id=player_id))

    requests.request("get", f"http://api:5000/endphase/{game_id}/{player_id}/")
    return redirect(f'/{game_id}/{player_id}')

@app.route("/<int:game_id>/<int:player_id>/supply/endphase/")
def end_phase_supply(game_id, player_id):
    """ends current phase and redirects to supply if the turn hasn't changed"""
    if requests.request("get", f"http://api:5000/gameisover/{game_id}/").json()['game_over']:
        return redirect(url_for('game_over', game_id=game_id, player_id=player_id))

    requests.request("get", f"http://api:5000/endphase/{game_id}/{player_id}/")
    phase = requests.request("get", f"http://api:5000/getgamestate/{game_id}").json()['phase']
    if phase == 'buy':
        return redirect(f'/{game_id}/{player_id}/supply')
    return redirect(f'/{game_id}/{player_id}')


@app.route("/<int:game_id>/<int:player_id>/gameover/")
def game_over(game_id, player_id):
    """This checks to make sure the game is actually over. If it is, it displays the pertinent information for that
    game. This means it calculates deck compositions and victory points"""
    # TODO get rid of player_id?
    exists = requests.get(f"http://api:5000/gameexists/{game_id}").json()['exists']
    if not exists:
        return redirect(url_for("home_page"))
    if not requests.request("get", f"http://api:5000/gameisover/{game_id}/").json()['game_over']:
        return redirect(url_for('game_page', game_id=game_id, player_id=player_id))
    pics = get_card_pics()
    deck_comps = requests.get(f"http://api:5000/deckcompositions/{game_id}/").json()
    vp = requests.get(f'http://api:5000/calculatescore/{game_id}/').json()
    requests.get(f"http://api:5000/save/{game_id}")
    return render_template("game-over.html", victory_points=vp, deck_compositions=deck_comps, card_pics=pics)

@app.route("/<int:game_id>/getoldgame")
def getoldgame(game_id):
    pics = get_card_pics()
    data = requests.get(f"http://api:5000/getoldgame/{game_id}").json()
    return render_template("game-over.html", victory_points = data['score'], deck_compositions = data['deck_comps'], card_pics = pics)

@app.route('/<int:game_id>/<int:player_id>/selectinfo/')
def select_cards(game_id, player_id):
    """Gets the info the frontend needs to let a player select cards. This means it gets options, the maximum
    number of cards to select, and whether a player can choose less."""
    select_info = {}
    req = requests.get(f"http://api:5000/getoptions/{game_id}/{player_id}").json()
    if len(req.keys()) > 0:
        select_info['options'] = req['options']
        select_info['max_num'] = req['n']
        select_info['can_choose_less'] = 'true' if req['canChooseLess'] else 'false'
    return select_info

@app.route("/<int:game_id>/selected/", methods=["POST"])
def selected(game_id):
    """Tells backend which cards were chosen by a player"""
    req = request.get_json()
    requests.post(f"http://api:5000/selected/{game_id}", json=req)
    return redirect(f'/{game_id}')

@app.route("/<int:game_id>/<int:player_id>/updates/")
def updates(game_id, player_id):
    """Gets the updates that a player needs for the front end to be properly up-to-date."""
    return requests.get(f"http://api:5000/updates/{game_id}/{player_id}").json()

@app.route("/tutorial/<int:step>")
def tutorial(step):
    """This code renders the tutorial which is stored in a separate file because the code is very 'bulky.'"""
    pics = get_card_pics()
    return tutorial_executer.do_step(step, pics)

@app.route("/data/")
def data():
    """Programmed by the backgammon group, this code returns the most common card found in games stored in the SQL
    database."""
    res = requests.get(f"http://api:5000/getstats/").json()
    most_common_card = get_most_common_card(res["deck"])
    pics = get_card_pics()
    return render_template("data.html", card = most_common_card, images=pics)
    # return render_template("data.html", card = "copper")

# move to backend?
def get_most_common_card(games):
    """gets the most common card in the final hands of all players given a list of games. Helper function to data()"""
    card_occurrence_dict = create_card_occurrence_dict(games)
    most_common_card = max(card_occurrence_dict, key=card_occurrence_dict.get)
    return most_common_card

def create_card_occurrence_dict(games):
    """creates a dictionary that counts the occurrence of each card in the final hands of all players given a list of
    games"""
    card_occurrence_dict = {}
    for game in games:
        for hand in game:
            for card in hand:
                if card != "fake":
                    if card not in card_occurrence_dict:
                        card_occurrence_dict[card] = 1
                    else:
                        card_occurrence_dict[card] += 1
    return card_occurrence_dict

@app.route("/savegame/<int:game_id>")
def save_game(game_id):
    """This is somewhat of a 'developer view' of what is stored in the SQL Database"""
    # TODO delete this?
    info = requests.get(f"http://api:5000/dbget/{game_id}/").json()
    result = info['deck']
    return render_template("db-connection.html", result = result)


@app.route("/<int:game_id>/save/")
def save(game_id):
    # TODO does nothing?
    # requests.get(f"http://api:5000/createtable/")
    # requests.get(f"http://api:5000/save/{game_id}")
    info = requests.get(f"http://api:5000/getstats/").json()
    cardlist = info['deck'][1][0]
    return render_template("db-connection.html", cardlist = cardlist)

@app.route("/<int:game_id>/debug/")
def debug(game_id):
    return requests.get(f"http://api:5000/debug/{game_id}").json()

if __name__ == "__main__":
    app.static_folder = "./static"
    app.template_folder = "./templates"
    app.run(host="0.0.0.0", port=5000)
