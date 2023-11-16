import requests
from player import player

def take_turn(player: player):
    requests.get(f"localhost:5000/endphase/{player.game.id}/{player.id}/")
    for card in player.hand:
        if card['type'] == 'treasure':
            requests.get(f"localhost:5000/cardplayed/{player.game.id}/{player.id}/{card['id']}/")
    if player.coins >= 8:
        requests.get(f"localhost:5000/cardbought/{player.game.id}/{player.id}/province/")
    elif player.coins >= 6 and player.game.supplySizes['province'] > 4:
        requests.get(f"localhost:5000/cardbought/{player.game.id}/{player.id}/gold/")
    elif player.coins >= 5 and player.game.supplySizes['province'] <= 4:
        requests.get(f"localhost:5000/cardbought/{player.game.id}/{player.id}/duchy/")
    elif player.coins >= 3 and player.game.supplySizes['province'] > 4:
        requests.get(f"localhost:5000/cardbought/{player.game.id}/{player.id}/supply/")
    elif player.coins >= 2 and player.game.supplySizes['province'] <= 4:
        requests.get(f"localhost:5000/cardbought/{player.game.id}/{player.id}/estate/")
    requests.get(f"localhost:5000/endphase/{player.game.id}/{player.id}/")
