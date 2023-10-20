import requests
import json

def getGameState(gameID):
    return requests.request("get", f"http://api:5000/getgamestate/{gameID}").json()
def changeVar(gameID, var, delta):
    #return requests.request("get", f"http://api:5000/changeVar/{gameID}/{var}/{delta}")
    return requests.post('http://api:5000/changeVar/', json={'gameID': gameID, 'var': var, 'delta': delta})
def changeZone(gameID, cards, zone):
    return requests.post('http://api:5000/changeZone/', json={'gameID': gameID, 'cards': cards, 'zone': zone})

def fromHand(args, gameID):
    # args: number, canPickLess
    # if number is negative allows picking any number
    n, canPickLess = args[0], args[1]
    return "yield"
    n = int(args[0])
    canPickLess = args[1] == 'T'
    return [str(i) for i in range(n)]

def getHand(args, gameID):
    # no args
    # returns list of all cards in players hand
    return getGameState(gameID)['hand']

def getDiscard(args, gameID):
    # no args
    # returns list of all cards in discard pile
    return getGameState(gameID)['discard']

def fromTop(args, gameID):
    # args: number
    # returns the top n cards
    n=int(args[0])
    deck = getGameState(gameID)['deck']
    if len(deck) < n:
        return deck [::-1]
    return deck[-1:-n-1:-1]

def getStore(args, gameID):
    # no args
    # returns a list of the cards in the store (1 for each supply pile if nonempty)
    return requests.get("http://api:5000/getStore/{gameID}").json()['store']

def gain(args, gameID):
    # args: cards, destination
    # moves the cards in the cards list to the destination zone
    cards = args[0]
    if len(args) < 2:
        dest = 'discard'
    else:
        dest = args[1]
    return changeZone(gameID, cards, dest)

def trash(args, gameID):
    # args: cards
    # moves the specified cards to trash
    cards = args[0]
    return changeZone(gameID, cards, 'trash')
    
def play(args, gameID):
    # args: card
    # moves the specified card to play area
    raise NotImplementedError

def toHand(args, gameID):
    # args: cards
    # moves the cards in the list to hand
    cards = args[0]
    return changeZone(gameID, cards, 'hand')

def discard(args, gameID):
    # args: cards
    # moves the cards in the list to discard pile
    cards = args[0]
    return changeZone(gameID, cards, 'discard')

def toDeck(args, gameID):
    # args: cards
    # moves the cards in the list to top of deck
    cards = args[0]
    return changeZone(gameID, cards, 'deck')

def changeCoins(args, gameID):
    # args: delta
    # changes coins by the amount
    return changeVar(gameID, 'coins', args[0])

def changeBuys(args, gameID):
    # args: delta
    # change buys by the amount
    return changeVar(gameID, 'buys', args[0])

def changeActions(args, gameID):
    # args: delta
    # change actions by the amount
    return changeVar(gameID, 'actions', args[0])

def draw(args, gameID):
    # args: num
    # draws num cards
    return requests.request("get", f"http://api:5000/draw/{gameID}/{args[0]}")

def count(args, gameID):
    # args: any number of list/set-like objects
    return sum([len(arg) for arg in args])

def getChoice(args, gameID):
    # args: message to display, list of fString values
    # asks the player for a y/n choice, showing them the message which is an fstring
    # example inpug: args = ["Discard {arg1} from the top of your deck?", "Copper"]
    return True
    raise NotImplementedError

def getName(args, gameID):
    # args: card
    return args[0]['name']

def getCost(args, gameID):
    # args: card
    return args[0]['cost']

def getType(args, gameID):
    # args: card
    return args[0]['type']

def getFirst(args, gameID):
    # args: set of cards
    return args[0]

def getSubset(args, gameID):
    # args: set of cards, condition1, condition2...
    # conditions are formatted "[<propertyName> <operator> <target>]"
    # operators are <, >, <=, >=, and =
    newSet = []
    conditions = args[1:]
    for card in args[0]:
        isLegal = True
        for cond in conditions:
            val = getattr(card, cond[0])
            target = cond[2]
            if isinstance(val, int):
                target = int(target)
            
            operator = cond[1]
            if operator == '=':
                if val != target:
                    isLegal = False
                    break
            elif operator == '>':
                if val <= target:
                    isLegal = False
                    break
            elif operator == '<':
                if val >= target:
                    isLegal = False
                    break
            elif operator == '>=':
                if val < target:
                    isLegal = False
                    break
            elif operator == '<=':
                if val > target:
                    isLegal = False
                    break
        if isLegal:
            newSet.append(card)
    return newSet

def chooseSubset(args, gameID):
    # args: set, n, canChooseLess
    # Asks the player to choose a subset of the set (list of cards), of size n, with the possible option to choose less than n
    # returns a list of the chosen cards
    return "yield"
    return args[0][:-1]
    raise NotImplementedError

def reorder(args, gameID):
    # args: set
    # allows the player to reorder the cards, then returns the new order
    return args[0][::-1]
    raise NotADirectoryError

def removeFromSet(args, gameID):
    # args: set, toRemove
    s = args[0].copy()
    for x in args[1]:
        if x in s:
            s.remove(x)
    return s

def getTrue(args, gameID):
    return True

def getFalse(args, gameID):
    return False

def makeArray(args, gameID):
    # I know this looks weird but its meant to be this way
    return args

def addInts(args, gameID):
    return sum([int(n) for n in args])

def eval(args, gameID):
    # args: val, operator, target
    val = args[0]
    operator = args[1]
    target = args[2]
    if isinstance(val, int):
        target = int(target)

    if operator == '=':
        return val == target
    elif operator == '>':
        return val > target
    elif operator == '<':
        return val < target
    elif operator == '>=':
        return val >= target
    elif operator == '<=':
        return val <= target
    raise ValueError
    
    
        
def countEmptyPiles(args, gameID):
    # no args
    # counts the number of empty supply piles and returns that number
    return 0
    raise NotImplementedError


funcs = [fromHand, getHand, getDiscard, fromTop, getStore, gain, trash, play, toHand, discard, toDeck, changeCoins, changeBuys, changeActions, draw, count, getChoice, getName, getCost, getType, getFirst, getSubset, chooseSubset, reorder, removeFromSet, getTrue, getFalse, eval, countEmptyPiles]

yieldFuncs = ['fromHand', 'getChoice', 'chooseSubset', 'reorder']
commands = {}
for func in funcs:
    commands[func.__name__] = func

def doCommand(func, args, gameID):
    return commands[func](args, gameID)

