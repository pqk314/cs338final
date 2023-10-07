from flask import Flask
from flask import render_template
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
    hand = requests.request("get", f"http://api:5000/gethand/{game_id}").text
    cards = hand[1:-1].split(",")
    for i in range(len(cards)):
        cards[i] = cards[i].strip()[1:-1]
    return render_template("front-end.html", hand=cards)


@app.route("/<int:game_id>/cardbought/<card_id>/")
def card_bought(game_id, card_id):
    """process for buying cards"""
    requests.request("get", f"http://api:5000/cardbought/{game_id}/{card_id}")
    return render_template("card-bought.html")


if __name__ == "__main__":
    app.static_folder = "./static"
    app.template_folder = "./templates"
    app.run(host="0.0.0.0", port=5000)
