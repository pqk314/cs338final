from flask import Flask, request, redirect, url_for, render_template
import random
import requests

from card_scripting import cardPlayer, cards, cardParser


class player:
    def __init__(self, game
                 , deck, id):
        """Initializes a player, for now this just assumes 1 player and a starting deck"""
        # Dictionary of everything that should update on front-end valid keys:
        # set_coins - sets coins to the value (integer) associated with key
        # set_actions - sets actions to the value (integer) associated with key
        # set_buys - sets buys to the value (integer) associated with key
        # set_phase - sets end phase button to whatever phase is.
        # add - tells game to add card (use card object). Add using update_cards('add', card: card, player: player, game: game)
        # remove - do the same command as above but use remove for first parameter instead
        # select - boolean value for select screen
        # new_turn - boolean for if there is a new turn

        self.updates = {}

        self.game = game
        self.deck = deck
        self.id = id
        # self.supply = random.sample(sorted(cards.supply_options), 10)
        
        self.hand = []
        self.discard = []
        self.in_play = []
        self.set_aside = []
        self.phase = "action"
        self.actions = 1
        self.buys = 1
        self.coins = 0
        self.cmd = None
        self.options = None
        self.cmd_stack = []
        self.shuffle()
        self.hand = self.deck[-5:]
        self.deck = self.deck[0:-5]

        self.text = 'Left click a card to play it.'
        self.barrier = ''

    def update_list(self, key, val):
        """Makes having list in dictionaries simpler, basically facilitates having a dictionary for simplicity's
        sake."""
        if key in self.updates:
            self.updates[key].append(val)
        else:
            self.updates[key] = [val]

    def set_text(self, text: str):
        """Sets heading text at top of page"""
        self.text = text
        self.updates['text'] = text

    def set_barrier(self, text: str):
        """Sets barrier with the message indicated in the text variable. if text = '', it will remove the barrier"""
        self.barrier = text
        self.updates['barrier'] = text

    def draw_cards(self, num_to_draw):
        """draws cards while attempting to catch edge cases. I may have forgotten one, but this may be final."""
        for i in range(num_to_draw):
            if len(self.deck) == 0 and len(self.discard) == 0:
                break
            if len(self.deck) == 0:
                self.deck = [card for card in self.discard]
                self.discard = []
                self.shuffle()

            self.hand.append(self.deck.pop())
            self.update_list('add', self.hand[-1])

        for p in self.game.players:
            p.updates['size_update'] = p.deck_info()

    def deck_info(self):
        deck_info = [
            f'Your Deck: {str(len(self.deck))} cards',
            f'Your Discard: {str(len(self.discard))} cards'
        ]
        for i in range(len(self.game.players)):
            if self.game.players[i] == self:
                continue
            deck_info.append(f"Player {i + 1}'s deck: {str(len(self.game.players[i].deck))} cards")
            deck_info.append(f"Player {i + 1}'s hand: {str(len(self.game.players[i].hand))} cards")
            deck_info.append(f"Player {i + 1}'s discard: {str(len(self.game.players[i].discard))} cards")
        return deck_info

    def from_top(self, num):
        fromTop = []
        for i in range(num):
            if len(self.deck) == 0 and len(self.discard) == 0:
                break
            if len(self.deck) == 0:
                self.deck = [card for card in self.discard]
                self.discard = []
                self.shuffle()
            fromTop.append(self.deck.pop())
        self.game.floatingCards += fromTop
        return fromTop

    def find_card_in_list(self, list, card_id):
        for idx, card in enumerate(list):
            if card['id'] == card_id:
                return idx
        return -1

    def find_card(self, card_id):
        for l in [self.hand, self.deck, self.discard, self.in_play]:
            idx = self.find_card_in_list(l, card_id)
            if idx != -1:
                return l, idx
        return [], -1

    def shuffle(self):
        """shuffles deck"""
        random.shuffle(self.deck)

    def end_turn(self):
        """Discards all cards in hand and in front of player"""
        while len(self.hand) > 0:
            self.discard.append(self.hand.pop())
            self.update_list('remove', self.discard[-1])
        while len(self.in_play) > 0:
            self.discard.append(self.in_play.pop())
        self.draw_cards(5)
        # TODO make these changeVar calls
        self.actions = 1
        self.buys = 1
        self.coins = 0
        self.phase = 'action'
    
    def calculate_score(self):
        score = 0
        cards = self.deck + self.hand + self.in_play + self.discard
        for c in cards:
            if(c['name'] == 'estate'):
                score += 1
            if(c['name'] == 'duchy'):
                score += 3
            if(c['name'] == 'province'):
                score += 6
            if(c['name'] == "gardens"):
                score += (len(cards)//10)
            if(c['name'] == 'curse'):
                score -= 1
        return score
    
    def set_command(self, cmd):
        self.cmd = cardParser.multicommand(cmd, self)

    def execute_command(self):
        res = self.cmd.execute()
        if res == "yield":
            self.updates['select'] = True
            return {'yield': True}
        #return {'yield': False}
        if self.cmd == None or self.cmd.commands == []:
            self.cmd = None
            while self.cmd_stack:
                if self.cmd_stack[-1] == []:
                    self.cmd_stack.pop()
                    continue
                self.cmd = self.cmd_stack.pop()
                res = self.cmd.execute()
                if res == 'yield':
                    self.updates['select'] = True
                    return {'yield': True}
        return {'yield': False}
    