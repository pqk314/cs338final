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
    'throne_room': {'type': 'action', 'cost': 4},
    'bandit': {'type': 'action', 'cost': 5},
    'council_room': {'type': 'action', 'cost': 5},
    'festival': {'type': 'action', 'cost': 5},
    'laboratory': {'type': 'action', 'cost': 5},
    'library': {'type': 'action', 'cost': 5},
    'market': {'type': 'action', 'cost': 5},
    'mine': {'type': 'action', 'cost': 5},
    'sentry': {'type': 'action', 'cost': 5},
    'witch': {'type': 'action', 'cost': 5},
    'artisan': {'type': 'action', 'cost': 6},


    'copper': {'type': 'treasure', 'cost': 0},
    'silver': {'type': 'treasure', 'cost': 3},
    'gold': {'type': 'treasure', 'cost': 6},

    'estate': {'type': 'victory', 'cost': 2},
    'duchy': {'type': 'victory', 'cost': 5},
    'province': {'type': 'victory', 'cost': 8},
    'gardens': {'type': 'victory', 'cost': 4},

    'curse': {'type': 'curse', 'cost': 0}
}


cardTexts = {
    'cellar': '#changeActions(1); x=#chooseSubset(#getHand(), -1, #true()); #discard($x); #draw(#count($x))',
    'chapel': '#trash(#chooseSubset(#getHand(), 4, #true()))',
    'moat': '#draw(2)',
    'harbinger': '#draw(1); #changeActions(1); #toDeck(#chooseSubset(#getDiscard(), 1, T))',
    'merchant': '#draw(1); #changeActions(1); somethingelse#', #not implemented
    #'vassal': '#changeCoins(2); x=#getFirst(#fromTop(1)); #discard($x); willPlay=#false(); #cond(#eval(#getType($x), =, action), #cond(#chooseSubset($x, 1, #true()), willPlay=#true())); #cond($willPlay, #play($x))',
    'vassal': '#changeCoins(2); x=#getFirst(#fromTop(1)); #discard($x); actions=#getSubset($x, #makeArray(type, =, action)); toPlay=#chooseSubset($actions, 1, #true()); #cond(#eval(#count($toPlay), >, 0), #play($toPlay)); #cond(#eval(#count($toPlay), >, 0), #execute(#getFirst($toPlay)))',
    'village': '#draw(1); #changeActions(2)',
    'workshop': '#gain(#chooseSubset(#getSubset(#getStore(), #makeArray(cost, <, 5)), 1, F))',
    'bureaucrat': '', #not implemented
    'militia': '#changeCoins(2)', #not implemented
    'moneylender': 'x=#getSubset(#getHand(), #makeArray(name, =, copper)); toTrash=#chooseSubset($x, 1, #true()); willTrash=#false(); #cond(#eval(#count($toTrash), >, 0), willTrash=#true()); #cond($willTrash, #trash($toTrash)); #cond($willTrash, #changeCoins(3))',
    'poacher': '#draw(1); #changeActions(1); #changeCoins(1); #discard(#chooseSubset(#getHand(), #eval(17, -, #count(#getStore())), #false()))',
    'remodel': 'x=#chooseSubset(#getHand(), 1, #false()); cost=#getCost(#getFirst($x)); #trash($x); options=#getSubset(#getStore(), #makeArray(cost, <=, #eval($cost, +, 2))); #gain(#chooseSubset($options, 1, #false()))',
    'smithy': '#draw(3)',
    'throne_room': '', #not implemented
    'bandit': '', # not implemented
    'council_room': '#draw(4); #changeBuys(1); #attack(#draw(1))',
    'festival': '#changeActions(2); #changeBuys(1); #changeCoins(2)',
    'laboratory': '#draw(2); #changeActions(1)',
    'library': 'n=#eval(7, -, #count(#getHand())); cards=#fromTop($n); actions=#getSubset($cards, #makeArray(type, =, action)); skip=#chooseSubset($actions, -1, #true()); #toHand(#removeFromSet($cards, $skip)); #trash($skip); #execute(#makeCard(library)); #discard($skip)', #not implemented
    'market': '#draw(1); #changeActions(1); #changeBuys(1); #changeCoins(1)',
    
    'mine':'x=#chooseSubset(#getSubset(#getHand(), #makeArray(type, =, treasure)), 1, #false()); cost=#getCost(#getFirst($x)); #trash($x); options=#getSubset(#getStore(), #makeArray(cost, <=, #eval($cost, +, 3)), #makeArray(type, =, treasure)); #gain(#chooseSubset($options, 1, #false()), hand)',
    'sentry': '#draw(1); #changeActions(1); x=#fromTop(2); toTrash=#chooseSubset($x, 2, #true()); #trash($toTrash); x=#removeFromSet($x, $toTrash); toDiscard=#chooseSubset($x, 2, #true()); #discard($toDiscard); x=#removeFromSet($x, $toDiscard); x=#reorder($x); #toDeck($x)',
    'witch': '#draw(2); #attack(#gain(#fromStore(curse)))',
    'artisan': '#gain(#chooseSubset(#getSubset(#getStore(), #makeArray(cost, <, 6)), 1, #false()), hand); #toDeck(#chooseSubset(#getHand(), 1, #false()))',


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