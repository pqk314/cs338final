from card_scripting import cards
from player import player
import random

class Game:
    def __init__(self, id, num_players):
        """Initializes game, for now this just assumes 1 player and a starting deck
        TODO: support for more than one player"""

        # Dictionary of everything that should update on front-end valid keys:
        # set_coins - sets coins to the value (integer) associated with key
        # set_actions - sets actions to the value (integer) associated with key
        # set_buys - sets buys to the value (integer) associated with key
        # set_phase - sets end phase button to whatever phase is.
        # add - tells game to add card (use card object). Add using update_cards('add', card: card, player: player, game: game)
        # remove - do the same command as above but use remove for first parameter instead
        # select - boolean value for select screen
        # new_turn - boolean for if there is a new turn

        # These next four I'm assuming will be implemented at some point
        # discard_size - sets discard pile size to the value (integer) associated with key
        # deck_size - sets discard pile size to the value (integer) associated with key
        # hand_size - sets discard pile size to the value (integer) associated with key
        # trash_size - sets discard pile size to the value (integer) associated with key
        self.updates = {}

        #to sort the cards by cost the self.supply needs to be sorted
        self.basesupply = ['copper', 'silver', 'gold', 'estate', 'duchy', 'province', 'curse']
        self.supply = ['market', 'workshop', 'council_room', 'moat', 'militia', 'village', 'smithy', 'laboratory', 'witch', 'gardens']
        self.supply.sort(key=lambda card: cards.getCard(card)['cost'])
        # change to [10 for i in range(10)] to make it take the right number of cards to finish the game=
        # self.supplySizes = [2 for i in range(10)]
        self.supplySizes = {key: 2 for key in self.supply}
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
        deck_cards = ['village', 'village', 'village', 'village', 'village', 'copper', 'copper', 'copper', 'copper', 'copper']
        custom_decks = [['cellar', 'village', 'village', 'village', 'village', 'copper', 'copper', 'copper', 'copper', 'copper'],
                        ['poacher', 'moneylender', 'harbinger', 'remodel', 'library', 'artisan', 'copper', 'sentry', 'vassal', 'estate']]
        self.players = []
        for i in range(num_players):
            deck = [self.make_card(c) for c in custom_decks[i]]
            #deck = [self.make_card(c) for c in deck_cards]
            newPlayer = player(self, deck, i)
            self.players.append(newPlayer)

        self.id = id


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
