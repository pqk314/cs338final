import cardParser as parser
import cards

def playCard(gameID, card):
    text = cards.cards(card)
    cmd = parser.multicommand(text)
    cmd.execute()
