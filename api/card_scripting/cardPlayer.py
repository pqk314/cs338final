from card_scripting import cardParser
from card_scripting import cards

def getCardCmd(gameID, card): 
    text = cards.getCardText(card)
    cmd = cardParser.multicommand(text, gameID)
    return cmd
