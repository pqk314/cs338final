def fromHand(args):
    # args: number, canPickLess
    # number can be negative
    n = int(args[0])
    canPickLess = args[1] == 'T'
    return [str(i) for i in range(n)]

def getHand(args):
    # no args
    raise NotImplementedError

def fromDiscard(args):
    # args: number, canPickLess
    raise NotImplementedError

def fromTop(args):
    # args: number, canPickLess
    raise NotImplementedError

def getStore(args):
    # no args
    raise NotImplementedError

def gain(args):
    # args: cards, destination
    if len(args) < 2:
        dest = 'discard'
    else:
        dest = args[1]
    raise NotImplementedError

def trash(args):
    # args: cards
    return args[0]
    
def play(args):
    # args: card
    raise NotImplementedError

def toHand(arg):
    # args: cards
    raise NotImplementedError

def discard(args):
    # args: cards
    raise NotImplementedError

def toDeck(args):
    # args: cards
    raise NotImplementedError

def changeCoins(args):
    # args: delta
    raise NotImplementedError

def changeBuys(args):
    # args: delta
    raise NotImplementedError

def changeActions(args):
    # args: delta
    raise NotImplementedError

def draw(args):
    # args: num
    raise NotImplementedError

def count(args):
    # args: any list/set-like object
    return len(args[0])

def getChoice(args):
    # args: message to display, list of fString values
    return True

def getName(args):
    # args: card
    return 'sample names'
    #return args[0].name

def getCost(args):
    # args: card
    return 3
    #return args[0].cost

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
    # operators are <, >, and =
    # multiconditions are seperated by &
    newSet = []
    #conditions = [c.strip().split() for c in args[1].split('&')]
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
    return args[0][:-1]
    raise NotImplementedError

def reorder(args):
    # args: set
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
    
    
        
def countEmptyPiles(args):
    return 0
    raise NotImplementedError


funcs = [fromHand, getHand, fromDiscard, fromTop, getStore, gain, trash, play, toHand, discard, toDeck, changeCoins, changeBuys, changeActions, draw, count, getChoice, getName, getCost, getType, getFirst, getSubset, chooseSubset, reorder, removeFromSet, getTrue, getFalse, eval, countEmptyPiles]

commands = {}
for func in funcs:
    commands[func.__name__] = func

def doCommand(func, args):
    return commands[func](args)

