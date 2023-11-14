from card_scripting import cardParser
from card_scripting import cards

def getCardCmd(player, card): 
    text = cards.getCardText(card)
    cmd = cardParser.multicommand(text, player)
    return cmd
