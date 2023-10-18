from flask import Flask
from flask import render_template
from flask import url_for
import json
import requests

app = Flask(__name__)




@app.route("/")
def home_page():
    """prompts user to make a new game"""
    return render_template("home-page.html")


@app.route("/newgame")
def new_game():
    """makes a new game and allows user to navigate to it"""
    game_id = requests.request("get", "http://api:5000/newgame").text
    return render_template("new-game.html", game_id=int(game_id))


@app.route("/<int:game_id>/")
def game_page(game_id):
    gamestate = requests.request("get", f"http://api:5000/getfrontstate/{game_id}").json()
    turn_info = {'Money': gamestate['coins'], 'Actions': gamestate['actions'], 'Buys': gamestate['buys']}
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
    
    # hand = requests.request("get", f"http://api:5000/gethand/{game_id}").text
    cards = gamestate["hand"]
    '''cards = hand[1:-1].split(",")
    for i in range(len(cards)):
        cards[i] = cards[i].strip()[1:-1]'''

    return render_template("front-end.html", hand=cards, images=card_pics, turn_info=turn_info)


@app.route("/<int:game_id>/supply")
def supply(game_id):
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
    # TODO: call to backend for cards ordered by amount they cost. Should be unique for each game instance
    cards = ["chapel", "cellar", "village", "merchant", "militia", "moneylender", "mine", "witch", "sentry", "artisan"]
    gamestate = requests.request("get", f"http://api:5000/getfrontstate/{game_id}").json()
    turn_info = {'Money': gamestate['coins'], 'Actions': gamestate['actions'], 'Buys': gamestate['buys']}
    return render_template("supply.html", cards=cards, card_pics=card_pics, turn_info=turn_info)


@app.route("/<int:game_id>/cardbought/<card_id>/")
def card_bought(game_id, card_id):
    """process for buying cards"""
    requests.request("get", f"http://api:5000/cardbought/{game_id}/{card_id}")
    return render_template("card-bought.html")


@app.route("/<int:game_id>/cardplayed/<card_id>/")
def card_played(game_id, card_id):
    """process for playing cards"""
    requests.request("get", f"http://api:5000/cardplayed/{game_id}/{card_id}")
    return render_template("card-played.html")


if __name__ == "__main__":
    app.static_folder = "./static"
    app.template_folder = "./templates"
    app.run(host="0.0.0.0", port=5000)
