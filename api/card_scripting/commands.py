def fromHand(args):
    # args: number, canPickLess
    # number can be negative
    return "yield"
    n = int(args[0])
    canPickLess = args[1] == 'T'
    return [str(i) for i in range(n)]

def getHand(args):
    # no args
    # returns list of all cards in players hand
    raise NotImplementedError

def getDiscard(args):
    # no args
    # returns list of all cards in discard pile
    raise NotImplementedError

def fromTop(args):
    # args: number
    # returns the top n cards
    raise NotImplementedError

def getStore(args):
    # no args
    # returns a list of the cards in the store (1 for each supply pile if nonempty)
    raise NotImplementedError

def gain(args):
    # args: cards, destination
    # moves the cards in the cards list to the destination zone
    if len(args) < 2:
        dest = 'discard'
    else:
        dest = args[1]
    raise NotImplementedError

def trash(args):
    # args: cards
    # moves the specified cards to trash
    return args[0]
    
def play(args):
    # args: card
    # moves the specified card to play area
    raise NotImplementedError

def toHand(arg):
    # args: cards
    # moves the cards in the list to hand
    raise NotImplementedError

def discard(args):
    # args: cards
    # moves the cards in the list to discard pile
    raise NotImplementedError

def toDeck(args):
    # args: cards
    # moves the cards in the list to top of deck
    raise NotImplementedError

def changeCoins(args):
    # args: delta
    # changes coins by the amount
    raise NotImplementedError

def changeBuys(args):
    # args: delta
    # change buys by the amount
    raise NotImplementedError

def changeActions(args):
    # args: delta
    # change actions by the amount
    raise NotImplementedError

def draw(args):
    # args: num
    # draws num cards
    raise NotImplementedError

def count(args):
    # args: any number of list/set-like objects
    return sum([len(arg) for arg in args])

def getChoice(args):
    # args: message to display, list of fString values
    # asks the player for a y/n choice, showing them the message which is an fstring
    # example inpug: args = ["Discard {arg1} from the top of your deck?", "Copper"]
    return True
    raise NotImplementedError

def getName(args):
    # args: card
    return 'sample names'
    return args[0].name
    raise NotImplementedError

def getCost(args):
    # args: card
    return 3
    return args[0].cost
    raise NotImplementedError

def getType(args):
    # args: card
    return 'action'
    raise NotImplementedError

def getFirst(args):
    # args: set of cards
    return args[0]

def getSubset(args):
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

def chooseSubset(args):
    # args: set, n, canChooseLess
    # Asks the player to choose a subset of the set (list of cards), of size n, with the possible option to choose less than n
    # returns a list of the chosen cards
    return args[0][:-1]
    raise NotImplementedError

def reorder(args):
    # args: set
    # allows the player to reorder the cards, then returns the new order
    return args[0][::-1]
    raise NotADirectoryError

def removeFromSet(args):
    # args: set, toRemove
    s = args[0].copy()
    for x in args[1]:
        if x in s:
            s.remove(x)
    return s

def getTrue(args):
    return True

def getFalse(args):
    return False

def makeArray(args):
    # I know this looks weird but its meant to be this way
    return args

def addInts(args):
    return sum([int(n) for n in args])

def eval(args):
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
    
    
        
def countEmptyPiles(args):
    # no args
    # counts the number of empty supply piles and returns that number
    return 0
    raise NotImplementedError


funcs = [fromHand, getHand, getDiscard, fromTop, getStore, gain, trash, play, toHand, discard, toDeck, changeCoins, changeBuys, changeActions, draw, count, getChoice, getName, getCost, getType, getFirst, getSubset, chooseSubset, reorder, removeFromSet, getTrue, getFalse, eval, countEmptyPiles]

yieldFuncs = ['fromHand', 'getChoice', 'chooseSubset', 'reorder']
commands = {}
for func in funcs:
    commands[func.__name__] = func

def doCommand(func, args):
    return commands[func](args)

