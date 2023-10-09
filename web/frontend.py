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
    #hand = requests.request("get", f"http://api:5000/gethand/{game_id}").text
    cards = gamestate["hand"]
    '''cards = hand[1:-1].split(",")
    for i in range(len(cards)):
        cards[i] = cards[i].strip()[1:-1]'''
    card_pics = {
        "copper": url_for('static', filename='images/372px-Copper.jpg'),
        "silver": url_for('static', filename='images/375px-Silver.jpg'),
        "gold": url_for('static', filename='images/375px-Gold.jpg'),
        "estate": url_for('static', filename='images/373px-Estate.jpg'),
        "duchy": url_for('static', filename='images/372px-Duchy.jpg'),
        "province": url_for('static', filename='images/375px-Province.jpg'),
        "curse": url_for('static', filename='images/372px-Curse.jpg')
    }
    return render_template("front-end.html", hand=cards, images=card_pics)


@app.route("/<int:game_id>/cardbought/<card_id>/")
def card_bought(game_id, card_id):
    """process for buying cards"""
    requests.request("get", f"http://api:5000/cardbought/{game_id}/{card_id}")
    return render_template("card-bought.html")


if __name__ == "__main__":
    app.static_folder = "./static"
    app.template_folder = "./templates"
    app.run(host="0.0.0.0", port=5000)
