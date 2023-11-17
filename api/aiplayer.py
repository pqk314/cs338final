import requests
from player import player


def take_turn(player: player):
    requests.get(f"http://localhost:5000/endphase/{player.game.id}/{player.id}/")
    to_play = []
    for card in player.hand:
        if card['type'] == 'treasure':
            to_play.append(card['id'])
    while to_play:
        requests.get(f"http://localhost:5000/cardplayed/{player.game.id}/{player.id}/{to_play.pop()}/")
    if player.coins >= 8 and player.game.supplySizes['province'] > 0:
        requests.get(f"http://localhost:5000/cardbought/{player.game.id}/{player.id}/province/")
    elif player.coins >= 6 and player.game.supplySizes['province'] > 4 and player.game.supplySizes['gold'] > 0:
        requests.get(f"http://localhost:5000/cardbought/{player.game.id}/{player.id}/gold/")
    elif player.coins >= 5 and player.game.supplySizes['province'] <= 4 and player.game.supplySizes['duchy'] > 0:
        requests.get(f"http://localhost:5000/cardbought/{player.game.id}/{player.id}/duchy/")
    elif player.coins >= 3 and player.game.supplySizes['province'] > 4 and player.game.supplySizes['silver'] > 0:
        requests.get(f"http://localhost:5000/cardbought/{player.game.id}/{player.id}/silver/")
    elif player.coins >= 2 and player.game.supplySizes['province'] <= 4 and player.game.supplySizes['estate'] > 0:
        requests.get(f"http://localhost:5000/cardbought/{player.game.id}/{player.id}/estate/")
    if player.coins >= 6 and player.buys == 1:
        requests.get(f"http://localhost:5000/cardbought/{player.game.id}/{player.id}/gold/")
    elif player.coins >= 3 and player.buys == 1:
        requests.get(f"http://localhost:5000/cardbought/{player.game.id}/{player.id}/silver/")
    requests.get(f"http://localhost:5000/endphase/{player.game.id}/{player.id}/")
