from flask import Flask
from flask import render_template, url_for, redirect, request
import json
import requests
import tutorial_executer

app = Flask(__name__)
card_pics = None


def get_card_pics():
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
    """prompts user to make a new game"""
    pics = get_card_pics()
    return render_template("home-page.html", card_pics=pics)


@app.route("/newgame/")
def new_game():
    """makes a new game and allows user to navigate to it"""
    game_id = requests.request("get", "http://api:5000/newgame").text
    requests.get(f"http://api:5000/createtable/")
    return redirect(f'/{game_id}/')


@app.route("/<int:game_id>/")
def game_page(game_id):
    # TODO for some reason this causes problems but it'd be really nice if this worked.
    # updates(game_id)

    exists = requests.get(f"http://api:5000/gameexists/{game_id}").json()['exists']
    if not exists:
        return redirect(url_for("home_page"))
    select_info = select_cards(game_id)
    select_info = None if len(select_info.keys()) == 0 else select_info
    gamestate = requests.request("get", f"http://api:5000/getfrontstate/{game_id}").json()
    turn_info = {'Money': gamestate['coins'], 'Actions': gamestate['actions'], 'Buys': gamestate['buys']}
    pics = get_card_pics()
    cards = gamestate["hand"]
    end_what = f"End {gamestate['phase'].title()}"
    return render_template("front-end.html", hand=cards, images=pics, turn_info=turn_info, end_what=end_what, game_id=game_id, select_info=select_info)

@app.route("/<int:game_id>/supply")
def supply(game_id):
    exists = requests.get(f"http://api:5000/gameexists/{game_id}").json()['exists']
    if not exists:
        return redirect(url_for("home_page"))
    pics = get_card_pics()
    gamestate = requests.request("get", f"http://api:5000/getfrontstate/{game_id}").json()
    cards = gamestate['supply']
    turn_info = {'Money': gamestate['coins'], 'Actions': gamestate['actions'], 'Buys': gamestate['buys']}
    end_what = f"End {gamestate['phase'].title()}"
    # TODO: call to backend, should be formatted as {card_name (str): num_left (int)}
    # make sure to pass into render template when done.
    remaining_cards = {}
    remaining_cards = gamestate['supplySizes']
    cards_left = gamestate['supplySizes']
    #for c in cards:
    #    remaining_cards[c] = cards_left[cards.index(c)]print(remaining_cards)
    return render_template("supply.html", cards=cards, card_pics=pics, turn_info=turn_info, end_what=end_what, remaining_cards = remaining_cards)


@app.route("/<int:game_id>/cardbought/<card_id>/")
def card_bought(game_id, card_id):
    """process for buying cards"""
    requests.request("get", f"http://api:5000/cardbought/{game_id}/{card_id}")
    return redirect(f'/{game_id}/supply')


@app.route("/<int:game_id>/cardplayed/<card_id>/")
def card_played(game_id, card_id):
    """process for playing cards"""
    res = requests.request("get", f"http://api:5000/cardplayed/{game_id}/{card_id}").json()
    return redirect(f'/{game_id}')

@app.route("/<int:game_id>/endphase/")
def end_phase(game_id):
    """ends current phase"""

    # I don't know exactly how we are trying to orginize the endgame stuff but this works
    
    gamestate = requests.request("get", f"http://api:5000/getfrontstate/{game_id}").json()
    supplySizes = gamestate['supplySizes']
    count = 0
    for x in supplySizes.keys():
        if supplySizes[x] < 1:
            count += 1
    if count >= 2:
        return redirect(url_for('game_over', game_id=game_id))

    requests.request("get", f"http://api:5000/endphase/{game_id}")
    return redirect(f'/{game_id}')

@app.route("/<int:game_id>/supply/endphase/")
def end_phase_supply(game_id):
    """ends current phase and redirects to supply if the turn hasn't changed"""

    # I don't know exactly how we are trying to orginize the endgame stuff but this works
    gamestate = requests.request("get", f"http://api:5000/getfrontstate/{game_id}").json()
    supplySizes = gamestate['supplySizes']
    count = 0
    for x in supplySizes.keys():
        if supplySizes[x] < 1:
            count += 1
    if count >= 2:
        return redirect(url_for('game_over', game_id=game_id))

    requests.request("get", f"http://api:5000/endphase/{game_id}")
    phase = requests.request("get", f"http://api:5000/getgamestate/{game_id}").json()['phase']
    if phase == 'buy':
        return redirect(f'/{game_id}/supply')
    return redirect(f'/{game_id}')


@app.route("/<int:game_id>/gameover/")
def game_over(game_id):
    requests.get(f"http://api:5000/save/{game_id}")

    # TODO: There needs to be an if statement for if the game is, in fact, not over.
    
    exists = requests.get(f"http://api:5000/gameexists/{game_id}").json()['exists']
    if not exists:
        return redirect(url_for("home_page"))
    gamestate = requests.request("get", f"http://api:5000/getfrontstate/{game_id}").json()
    supplySizes = gamestate['supplySizes']
    count = 0
    for x in supplySizes.keys():
        if supplySizes[x] < 1:
            count += 1
    if count < 2:
        return redirect(f'/{game_id}')
    pics = get_card_pics()
    deck_comps = requests.get(f"http://api:5000/deckcompositions/{game_id}/").json()
    vp = requests.get(f'http://api:5000/calculatescore/{game_id}/').json()
    return render_template("game-over.html", victory_points=vp, deck_compositions=deck_comps, card_pics=pics)

@app.route('/<int:game_id>/selectinfo/')
def select_cards(game_id):
    select_info = {}
    req = requests.get(f"http://api:5000/getoptions/{game_id}").json()
    if len(req.keys()) > 0:
        select_info['options'] = req['options']
        select_info['max_num'] = req['n']
        select_info['can_choose_less'] = 'true' if req['canChooseLess'] else 'false'
    return select_info

@app.route("/<int:game_id>/selected/", methods=["POST"])
def selected(game_id):
    req = request.get_json()
    requests.post(f"http://api:5000/selected/{game_id}", json=req)
    redirect(f'/{game_id}')

@app.route("/updates/<int:game_id>/")
def updates(game_id):
    exists = requests.get(f"http://api:5000/gameexists/{game_id}").json()['exists']
    if not exists:
        return {'home_page': True}
    return requests.get(f"http://api:5000/updates/{game_id}").json()

@app.route("/selected/<int:game_id>/", methods=["POST"])
def selected2(game_id):
    app.logger.info("relaying")
    req = request.get_json()
    res = requests.post(f"http://api:5000/selected/{game_id}", json=req).text
    return res
    redirect(f'/{game_id}')

@app.route("/ischoice/<int:game_id>/")
def ischoice(game_id):
    res = requests.get(f"http://api:5000/ischoice/{game_id}")
    return res

@app.route("/tutorial/<int:step>")
def tutorial(step):
    pics = get_card_pics()
    return tutorial_executer.do_step(step, pics)

@app.route("/data/")
def data():
    res = requests.get(f"http://api:5000/getstats/")
    most_common_card = get_most_common_card(res)
    return render_template("data.html", card = most_common_card)
    # return render_template("data.html", card = "copper")

'''gets the most common card in the final hands of all players given a list of games'''
# move to backend?
def get_most_common_card(games):
    card_occurrence_dict = create_card_occurrence_dict(games)
    print(card_occurrence_dict)
    most_common_card = max(card_occurrence_dict, key=card_occurrence_dict.get)           
    return most_common_card

'''creates a dictionary that counts the occurrence of each card in the final hands of all players given a list of games'''
def create_card_occurrence_dict(games):
    card_occurrence_dict = {}
    print("games: ", games)
    for game in games:
        print("game: ", game)
        for hand in game:
            print("hand: ", hand)
            for card in hand:
                print("card: ", game)
                if card not in card_occurrence_dict:
                    card_occurrence_dict[card] = 1
                else:
                    card_occurrence_dict[card] += 1
    return card_occurrence_dict

@app.route("/savegame/")
def save_game():

    # requests.get(f"http://api:5000/dbadd/")
    info = requests.get(f"http://api:5000/dbget/").json()
    result = info['works']
    return render_template("db-connection.html", result = result)


@app.route("/<int:game_id>/save/")
def save(game_id):
    # requests.get(f"http://api:5000/createtable/")
    # requests.get(f"http://api:5000/save/{game_id}")
    info = requests.get(f"http://api:5000/dbget/{game_id}").json()
    cardlist = info['deck']
    return render_template("db-connection.html", cardlist = cardlist)

if __name__ == "__main__":
    app.static_folder = "./static"
    app.template_folder = "./templates"
    app.run(host="0.0.0.0", port=5000)
