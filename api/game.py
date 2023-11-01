from card_scripting import cards
from player import player
import random

class Game:
    def __init__(self, id, num_players):
        """Initializes game, for now this just assumes 1 player and a starting deck
        TODO: support for more than one player"""
        
        #to sort the cards by cost the self.supply needs to be sorted
        self.supply = ['market', 'festival', 'council_room', 'moat', 'militia', 'village', 'smithy', 'laboratory', 'witch', 'gardens']
        self.supply.sort(key=lambda card: cards.getCard(card)['cost'])
        # change to [10 for i in range(10)] to make it take the right number of cards to finish the game=
        self.supplySizes = [2 for i in range(10)]
        self.nextCardID = 0
        self.gamestateID = 0
        deck_cards = ['village', 'village', 'village', 'village', 'village', 'copper', 'copper', 'copper', 'copper', 'copper']
        custom_decks = [['cellar', 'village', 'village', 'village', 'village', 'copper', 'copper', 'copper', 'copper', 'copper'],
                        ['cellar', 'copper', 'copper', 'copper', 'copper', 'copper', 'copper', 'estate', 'estate', 'estate']]
        self.players = []
        for i in range(num_players):
            deck = [self.make_card(c) for c in custom_decks[i]]
            #deck = [self.make_card(c) for c in deck_cards]
            newPlayer = player(self, deck, i)
            #newPlayer.shuffle()
            #newPlayer.draw_cards(5)
            self.players.append(newPlayer)
            
        self.id = id


    def make_card(self, name):
        """returns a card object with the given name"""
        card = cards.getCard(name).copy()
        card['id'] = self.nextCardID
        card['name'] = name
        self.nextCardID += 1
        return card

    def draw_cards(self, num_to_draw):
        """draws cards while attempting to catch edge cases. I may have forgotten one, but this may be final."""
        self.gamestateID += 1
        for i in range(num_to_draw):
            if len(self.deck) == 0 and len(self.discard) == 0:
                break
            if len(self.deck) == 0:
                self.deck = self.discard
                self.discard = []
                self.shuffle()
            self.hand.append(self.deck.pop())

    def find_card_in_list(self, list, card_id):
        for idx, card in enumerate(list):
            if card['id'] == card_id:
                return idx
        return -1

    def find_card(self, card_id):
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

    def end_turn(self):
        self.gamestateID += 1
        """Discards all cards in hand and in front of player"""
        while len(self.hand) > 0:
            self.discard.append(self.hand.pop())
        while len(self.in_play) > 0:
            self.discard.append(self.in_play.pop())
        self.draw_cards(5)
        self.actions = 1
        self.buys = 1
        self.coins = 0
        self.phase = 'action'