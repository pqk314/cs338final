from card_scripting import cards
from player import player
import random

class Game:
    def __init__(self, id, num_players):
        """Initializes game, for now this just assumes 1 player and a starting deck
        TODO: support for more than one player"""
        #to sort the cards by cost the self.supply needs to be sorted
        self.basesupply = ['copper', 'silver', 'gold', 'estate', 'duchy', 'province', 'curse']
        self.supply = ['market', 'workshop', 'council_room', 'moat', 'militia', 'village', 'smithy', 'laboratory', 'witch', 'gardens']
        self.supply.sort(key=lambda card: cards.getCard(card)['cost'])
        # change to [10 for i in range(10)] to make it take the right number of cards to finish the game=
        # self.supplySizes = [2 for i in range(10)]
        self.supplySizes = {key: 10 for key in self.supply}
        self.supplySizes['copper'] = 60 - 7*num_players
        self.supplySizes['silver'] = 40
        self.supplySizes['gold'] = 30
        victorySizes = 12 if num_players > 2 else 8
        self.supplySizes['estate'] = victorySizes
        self.supplySizes['duchy'] = victorySizes
        self.supplySizes['province'] = victorySizes
        self.floatingCards = []
        self.trash = []
        if 'gardens' in self.supply:
            self.supplySizes['gardens'] = victorySizes
        self.supplySizes['curse'] = 10*num_players - 10
        self.nextCardID = 0
        self.gamestateID = 0
        deck_cards = ['copper', 'copper', 'copper', 'copper', 'copper', 'copper', 'copper', 'estate', 'estate', 'estate']
        custom_decks = [['cellar', 'village', 'village', 'village', 'village', 'copper', 'copper', 'copper', 'copper', 'copper'],
                        ['poacher', 'moneylender', 'harbinger', 'remodel', 'library', 'throne_room', 'copper', 'sentry', 'vassal', 'estate']]
        self.players = []
        for i in range(num_players):
            # deck = [self.make_card(c) for c in custom_decks[i]]
            deck = [self.make_card(c) for c in deck_cards]
            newPlayer = player(self, deck, self.make_player_id())
            self.players.append(newPlayer)
        self.currentPlayer = self.players[0]

        self.is_computer_game = True
        self.first_turn_ended = False
        self.is_over = False
        self.added_to_db = False

        self.id = id

    def make_player_id(self):
        id = random.randint(0, 1000000000)
        new_id = id
        while True:
            for player in self.players:
                if player.id == id:
                    id = random.randint(0, 1000000000)
            if id == new_id:
                break
            else:
                new_id = id
        return id


    def get_player_number(self, player_id):
        """Takes in player ID and outputs number that is that players location in the players array"""
        for i in range(len(self.players)):
            if self.players[i].id == player_id:
                return i + 1
        raise ValueError('Player ID not found')

    def update_all_players(self, key, val):
        for p in self.players:
            p.updates[key] = val

    def update_list_all_players(self, key, val):
        for p in self.players:
            p.update_list(key, val)

    def make_card(self, name):
        """returns a card object with the given name"""
        card = cards.getCard(name).copy()
        card['id'] = self.nextCardID
        card['name'] = name
        self.nextCardID += 1
        return card

    def find_card_in_list(self, list, card_id):
        for idx, card in enumerate(list):
            if card['id'] == card_id:
                return idx
        return -1

    def find_card(self, card_id):
        idx = self.find_card_in_list(self.floatingCards, card_id)
        if idx != -1:
            return self.floatingCards, idx
        for player in self.players:
            l, idx = player.find_card(card_id)
            if idx != -1:
                return l, idx
        return [], -1
    
    def find_card_in_trash(self, card_id):
        idx = self.find_card_in_list(self.trash, card_id)
        if idx != -1:
            return self.trash, idx
        return [], -1
    
    def find_card_objs(self, card_ids):
        objs = []
        for card_id in card_ids:
            l, idx = self.find_card(card_id)
            if idx!= -1:
                objs.append(l[idx])
        return objs

    def shuffle(self):
        """shuffles deck"""
        random.shuffle(self.deck)


    def update_cards(self, add_or_remove, card):
        """Adds cards to game.updates, basically facilitates having a dictionary for simplicity's sake."""
        if add_or_remove in self.updates:
            self.updates[add_or_remove].append(card)
        else:
            self.updates[add_or_remove] = [card]
