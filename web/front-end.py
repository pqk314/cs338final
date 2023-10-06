from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route("/")
def home_page():
    return render_template("front-end.html")


@app.route("/cardbought/<card_id>")
def card_bought(card_id):
    print(card_id)
    return render_template("card-bought.html")


if __name__ == "__main__":
    app.static_folder = "./static"
    app.template_folder = "./templates"
    app.run(host="0.0.0.0", port=5001)
