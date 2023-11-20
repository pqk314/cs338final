from card_scripting import cards
import aiplayer

def getGameState(player):
    game = player.game
    state = {"hand": player.hand, "discard": player.discard, "in_play": player.in_play, "deck": player.deck,
             "phase": player.phase, "actions": player.actions, "buys": player.buys, "coins": player.coins,
             "supply": game.supply, "supplySizes": game.supplySizes}
    return state
def changeVar(player, var, delta):
    game = player.game
    delta = int(delta)
    if var == "actions":
        player.actions += delta
        game.update_all_players('set_actions', player.actions)
    elif var == "buys":
        player.buys += delta
        game.update_all_players('set_buys', player.buys)
    elif var == "coins":
        player.coins += delta
        game.update_all_players('set_coins', player.coins)
    else:
        raise ValueError("Invalid variable name")
    return True

def changeZone(player, cards, zone):
    if not type(cards) == list:
        cards = [cards]
    if len(cards) == 0:
        return False
    game = player.game
    dest = None
    if zone == 'discard':
        dest = player.discard
    elif zone == 'hand':
        dest = player.hand
    elif zone == 'deck':
        dest = player.deck
    elif zone == 'trash':
        dest = game.trash
    elif zone == 'in_play':
        dest = player.in_play
    elif zone == 'set_aside':
        dest = player.set_aside
    for card in cards:
        card_id = card['id']
        card_loc = player.find_card(card_id)
        if card_loc[1] != -1:
            removed = card_loc[0].pop(card_loc[1])
            if card_loc[0] == player.hand:
                player.update_list('remove', removed)
        if dest == player.hand:
            player.update_list('add', card)
        if dest == player.in_play:
            player.update_list('play', card)
        dest.append(card)
        for p in game.players:
            p.updates['size_update'] = p.deck_info()
    return True

def getHand(args, player):
    # no args
    # returns list of all cards in players hand
    return getGameState(player)['hand']

def getDiscard(args, player):
    # no args
    # returns list of all cards in discard pile
    return getGameState(player)['discard']

def getSetAside(args, player):
    # no args
    # returns list of all cards in discard pile
    return player.set_aside

def fromTop(args, player):
    # args: number
    # returns the top n cards
    return player.from_top(int(args[0]))

def getStore(args, player):
    # no args
    # returns a list of the cards in the store (1 for each supply pile if nonempty)
    game = player.game
    cards = [game.make_card(name) for name, val in game.supplySizes.items() if val > 0]
    game.floatingCards += cards
    return cards

def fromStore(args, player):
    # args: cardname
    # returns a new card object of the card name
    game = player.game
    card_name = args[0]
    if game.supplySizes[card_name] == 0:
        return []
    game.supplySizes[card_name] -= 1
    card = game.make_card(card_name)
    game.floatingCards.append(card)
    
    return card

def decreaseSupply(args, player):
    # args: card obj
    # decrements the number of the card in the supply
    player.game.supplySizes[args[0].name] -= 1

def gain(args, player):
    # args: cards, destination
    # moves the cards in the cards list to the destination zone
    cards = args[0]
    if len(args) < 2:
        dest = 'discard'
    else:
        dest = args[1]
    return changeZone(player, cards, dest)

def trash(args, player):
    # args: cards
    # moves the specified cards to trash
    cards = args[0]
    return changeZone(player, cards, 'trash')
    
def play(args, player):
    # args: card
    # moves the specified card to play area
    cards = args[0]
    return changeZone(player, cards, 'in_play')

def toHand(args, player):
    # args: cards
    # moves the cards in the list to hand
    cards = args[0]
    return changeZone(player, cards, 'hand')

def discard(args, player):
    # args: cards
    # moves the cards in the list to discard pile
    cards = args[0]
    return changeZone(player, cards, 'discard')

def toDeck(args, player):
    # args: cards
    # moves the cards in the list to top of deck
    cards = args[0]
    return changeZone(player, cards, 'deck')

def setAside(args, player):
    # args: cards
    # moves the cards in the list to set aside zone
    cards = args[0]
    return changeZone(player, cards, 'set_aside')

def changeCoins(args, player):
    # args: delta
    # changes coins by the amount
    return changeVar(player, 'coins', args[0])

def changeBuys(args, player):
    # args: delta
    # change buys by the amount
    return changeVar(player, 'buys', args[0])

def changeActions(args, player):
    # args: delta
    # change actions by the amount
    return changeVar(player, 'actions', args[0])

def draw(args, player):
    # args: num
    # draws num cards
    player.draw_cards(int(args[0]))
    return True

def count(args, player):
    # args: any number of list/set-like objects
    return sum([len(arg) for arg in args])

def attack(args, player):
    # args: multicommand string
    # executes the multicommand for each player besides the current player
    cmd = args[0]
    shouldYield = False
    for p in player.game.players:
        if p is player:
            continue
        p.set_command(cmd)
        res = p.execute_command()
        if ('yield' in res and res['yield'] == True) or res == 'yield':
            shouldYield = True
    if shouldYield:
        player.set_barrier("Waiting for other players.")
        player.cmd.commands = player.cmd.commands[1:]
        return 'yield'
    return True

def execute(args, player):
    # args: card
    # executes the command of the card for the current player
    if type(args[0]) == list:
        card = args[0][0]
    else:
        card = args[0]
    current_command = player.cmd
    current_command.commands = current_command.commands[1:]
    player.cmd_stack.append(current_command)
    cmdStr = cards.getCardText(card['name'])
    player.set_command(cmdStr)
    res = player.execute_command()
    if ('yield' in res and res['yield'] == True) or res == 'yield':
        return 'yield'
    return res

def makeCard(args, player):
    # args: card name
    # creates and returns an object of the card with the specified name
    return player.game.make_card(args[0])

def endEarly(args, player):
    # args: none
    # ends the execution early
    player.cmd.commands = player.cmd.commands[:1]
    return True

def getChoice(args, player):
    # args: message to display, list of fString values
    # asks the player for a y/n choice, showing them the message which is an fstring
    # example inpug: args = ["Discard {arg1} from the top of your deck?", "Copper"]
    return True

def getName(args, player):
    # args: card
    return args[0]['name']

def getCost(args, player):
    # args: card
    return args[0]['cost']

def getType(args, player):
    # args: card
    return args[0]['type']

def getFirst(args, player):
    # args: set of cards
    if len(args[0]) == 0:
        return []
    return args[0][0]

def getSubset(args, player):
    # args: set of cards, condition1, condition2...
    # conditions are formatted "[<propertyName> <operator> <target>]"
    # operators are <, >, <=, >=, and =
    if type(args[0]) != list:
        args[0] = [args[0]]
    newSet = []
    conditions = args[1:]
    if type(args[0]) != list:
        args[0] = [args[0]]
    for card in args[0]:
        isLegal = True
        for cond in conditions:
            val = card[cond[0]]
            target = cond[2]
            if isinstance(val, int):
                target = int(target)
            
            operator = cond[1]
            if operator == '=':
                if val != target:
                    isLegal = False
                    break
            elif operator == '!=':
                if val == target:
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

def chooseSubset(args, player):
    # args: set, n, canChooseLess
    # Asks the player to choose a subset of the set (list of cards), of size n, with the possible option to choose less than n
    # returns a list of the chosen cards
    o = {'options': args[0], 'n': int(args[1]), 'canChooseLess': args[2]}
    if o['n'] >= len(o['options']) and not o['canChooseLess']:
        return o['options']
    if o['n'] == 0 or len(o['options']) == 0:
        return []
    if player.game.is_computer_game and player.game.currentPlayer != player:
        return aiplayer.make_selection(o['options'], o['n'], o['canChooseLess'])
    player.options = o
    return 'yield'

def reorder(args, player):
    # args: set
    # allows the player to reorder the cards, then returns the new order
    return args[0][::-1]
    raise NotADirectoryError

def removeFromSet(args, player):
    # args: set, toRemove
    s = args[0].copy()
    for x in args[1]:
        if x in s:
            s.remove(x)
    return s

def true(args, player):
    return True

def false(args, player):
    return False

def makeArray(args, player):
    # I know this looks weird but its meant to be this way
    return args

def addInts(args, player):
    # args: list of ints
    # sums the ints
    return sum([int(n) for n in args])

def eval(args, player):
    # args: val, operator, target
    # evaluates an expression. Can be boolean or numerical
    val1 = args[0]
    operator = args[1]
    val2 = args[2]
    if isinstance(val1, int):
        val2 = int(val2)
    elif val1.isdigit():
        val1 = int(val1)
        val2 = int(val2)

    if operator == '=':
        return val1 == val2
    elif operator == '>':
        return val1 > val2
    elif operator == '<':
        return val1 < val2
    elif operator == '>=':
        return val1 >= val2
    elif operator == '<=':
        return val1 <= val2
    elif operator == '+':
        return val1 + val2
    elif operator == '-':
        return val1 - val2
    elif operator == 'and':
        return val1 and val2
    elif operator == 'or':
        return val1 or val2
    else:
        raise ValueError(f"Invalid operator {operator}")
    


funcs = [getHand, getDiscard, getSetAside, fromTop, getStore, fromStore, gain, trash, play, toHand, discard, toDeck, setAside, changeCoins, changeBuys, changeActions, draw, count, getChoice, getName, getCost, getType, getFirst, getSubset, chooseSubset, reorder, removeFromSet, true, false, eval, makeArray, attack, execute, makeCard, endEarly]

yieldFuncs = ['fromHand', 'getChoice', 'chooseSubset', 'reorder']
commands = {}
for func in funcs:
    commands[func.__name__] = func

def doCommand(func, args, player):
    return commands[func](args, player)