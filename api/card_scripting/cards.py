macros = {
    'cantrip': '#draw(1); #changeActions(1);',
    'chapel': 'x=#fromHand(4, T); #trash($x);'
}
# use '&macroname' in a card to call the macro
supply_options = [
    'cellar',
    'chapel',
    'moat',
    'harbinger',
    'merchant',
    'vassal',
    'village',
    'workshop',
    'bureaucrat',
    'militia',
    'moneylender',
    'poacher',
    'remodel',
    'smithy',
    'throne_room',
    'bandit',
    'council_room',
    'festival',
    'laboratory',
    'library',
    'market',
    'mine',
    'sentry',
    'witch',
    'artisan',
    'gardens',
]
cards = {
    'cellar': {'type': 'action', 'cost': 2},
    'chapel': {'type': 'action', 'cost': 2},
    'moat': {'type': 'action', 'cost': 2},
    'harbinger': {'type': 'action', 'cost': 3},
    'merchant': {'type': 'action', 'cost': 3},
    'vassal': {'type': 'action', 'cost': 3},
    'village': {'type': 'action', 'cost': 3},
    'workshop': {'type': 'action', 'cost': 3},
    'bureaucrat': {'type': 'action', 'cost': 4},
    'militia': {'type': 'action', 'cost': 4},
    'moneylender': {'type': 'action', 'cost': 4},
    'poacher': {'type': 'action', 'cost': 4},
    'remodel': {'type': 'action', 'cost': 4},
    'smithy': {'type': 'action', 'cost': 4},
    'throne room': {'type': 'action', 'cost': 4},
    'bandit': {'type': 'action', 'cost': 5},
    'council room': {'type': 'action', 'cost': 5},
    'festival': {'type': 'action', 'cost': 5},
    'laboratory': {'type': 'action', 'cost': 5},
    'library': {'type': 'action', 'cost': 5},
    'market': {'type': 'action', 'cost': 5},
    'mine': {'type': 'action', 'cost': 5},
    'sentry': {'type': 'action', 'cost': 5},
    'witch': {'type': 'action', 'cost': 5},
    'artisan': {'type': 'action', 'cost': 5},


    'copper': {'type': 'treasure', 'cost': 0},
    'silver': {'type': 'treasure', 'cost': 3},
    'gold': {'type': 'treasure', 'cost': 6},

    'estate': {'type': 'victory', 'cost': 2},
    'duchy': {'type': 'victory', 'cost': 5},
    'province': {'type': 'victory', 'cost': 8},
    'gardens': {'type': 'victory', 'cost': 4}
}


cardTexts = {
    'cellar': '#changeActions(1); x=#chooseSubset(#getHand(), -1, T); #discard($x); #draw(#count($x))',
    'chapel': '#trash(#fromHand(4, T))',
    'moat': '#draw(2)',
    'harbinger': '#draw(1); #changeActions(1); #toDeck(#chooseSubset(#getDiscard(), 1, T))',
    'merchant': '#draw(1); #changeActions(1); somethingelse#', #not implemented
    'vassal': '#changeCoins(2); x=#getFirst(#fromTop(1)); #discard($x); #cond(#eval(#getType($x), =, action), #cond(#getChoice("Play {}?", #getName($x)), #play($x)))',
    'village': '#draw(1); #changeActions(2)',
    'workshop': '#gain(#chooseSubset(#getSubset(#getStore(), #makeArray(cost, <, 5)), 1, F))',
    'bureaucrat': '', #not implemented
    'militia': '#changeCoins(2)', #not implemented
    'moneylender': '#set(x, #getSubset(#getHand(), #makeArray(name, =, copper))); #set(hasCopper, #eval(#count(#get(x)), >, 0)); #set(willTrash, #getFalse()) #cond(#get(hasCopper), #set(willTrash, #getChoice("Trash a copper?"))); #cond(#get(hasCopper), #trash(#getFirst(#get(x)))); #cond(#get(hasCopper), #changeCoins(3))',
    'poacher': '#draw(1); #changeActions(1); #changeCoins(1); #discard(#fromHand(#countEmptyPiles(), F))',
    'remodel': '#x=#fromHand(1, F); #trash($x); #gain(#chooseSubset(#getSubset(#getStore(), cost, <=, #addInts(#getCost($x), 2)), 1, F))',
    'smithy': '#draw(3)',
    'throne room': '', #not implemented
    'bandit': '', # not implemented
    'council room': '#draw(4); #changeBuys(1); ', #not implemented
    'festival': '#changeActions(2); #changeBuys(1); #changeCoins(2)',
    'laboratory': '#draw(2); #changeActions(1)',
    'library': '', #not implemented
    'market': '#draw(1); #changeActions(1); #changeBuys(1); #changeCoins(1)',
    'mine': '#set(x, #fromHand(1, F)); ', #not implemented
    'sentry': '#draw(1); #changeActions(1); x=#fromTop(2); toTrash=#chooseSubset($x, 2, T); #trash($toTrash); x=#removeFromSet($x, $toTrash); toDiscard=#chooseSubset($x, 2, T); #discard($toDiscard); x=#removeFromSet($x, $toDiscard); x=#reorder($x); #toDeck($x)',
    'witch': '#draw(2); ', # not implemented
    'artisan': 'notImplemented; #toDeck(#fromHand(1, F))',


    'copper': '#changeCoins(1)',
    'silver': '#changeCoins(2)',
    'gold': '#changeCoins(3)',
}

def getCardNames():
    return cardTexts.keys()

def getCardText(cardName):
    return cardTexts[cardName]

def getCard(cardName):
    return cards[cardName]