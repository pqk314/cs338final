from card_scripting import cardPlayer

class turn():
    def __init__(self, gameID, playerID, hand, deck, discard):
        self.player = playerID
        self.hand = hand
        self.deck = deck
        self.discard = discard
        self.played = []
        self.actions = 1
        self.buys = 1
        self.coins = 0
        self.phase = "action"
        self.game = gameID
    
    def playAction(self, card):
        if self.phase != "action" or self.actions == 0 or card not in self.hand:
            return False
        self.hand.remove(card)
        self.played.append(card)
        cardPlayer.playCard(self.game, self.player, card)
        self.actions -= 1

    def playTreasure(self, card):
        if self.phase != "buy" or card not in self.hand:
            return False
        self.hand.remove(card)
        self.played.append(card)
        cardPlayer.playCard(self.game, self.player, card)
    

    def playCard(self, card):
        if card.type == "action":
            return self.playAction(card)
        elif card.type == "treasure":
            return self.playTreasure(card)
            
    