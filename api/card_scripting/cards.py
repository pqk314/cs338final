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
    'harbinger': '#draw(1); #changeActions(1); #toDeck(#chooseSubset(#getDiscard(), 1, #true()))',
    'merchant': '#draw(1); #changeActions(1); #merchant()', #not implemented
    'vassal': '#changeCoins(2); x=#getFirst(#fromTop(1)); #discard($x); actions=#getSubset($x, #makeArray(type, =, action)); toPlay=#chooseSubset($actions, 1, #true()); #cond(#eval(#count($toPlay), >, 0), #play($toPlay)); #cond(#eval(#count($toPlay), >, 0), #execute(#getFirst($toPlay)))',
    'village': '#draw(1); #changeActions(2)',
    'workshop': 'card=#chooseSubset(#getSubset(#getStore(), #makeArray(cost, <, 5)), 1, #false()); #gain($card); #decreaseSupply($card)',
    'bureaucrat': '#gain(#fromStore(silver), deck); #attack(`#toDeck(#chooseSubset(#getSubset(#getHand(), #makeArray(type, =, victory)), 1, #false()))`)',
    'militia': '#changeCoins(2); #attack(`x=#eval(#count(#getHand()), -, 3); #cond(#eval($x, >, 0), #set(toDiscard, #chooseSubset(#getHand(), $x, #false()))); #cond(#eval($x, >, 0), #discard($toDiscard))`)',
    'moneylender': 'x=#getSubset(#getHand(), #makeArray(name, =, copper)); toTrash=#chooseSubset($x, 1, #true()); willTrash=#false(); #cond(#eval(#count($toTrash), >, 0), willTrash=#true()); #cond($willTrash, #trash($toTrash)); #cond($willTrash, #changeCoins(3))',
    'poacher': '#draw(1); #changeActions(1); #changeCoins(1); #discard(#chooseSubset(#getHand(), #eval(17, -, #count(#getStore())), #false()))',
    'remodel': 'x=#chooseSubset(#getHand(), 1, #false()); cost=#getCost(#getFirst($x)); #trash($x); options=#getSubset(#getStore(), #makeArray(cost, <=, #eval($cost, +, 2))); card=#chooseSubset($options, 1, #false()); #gain($card); #decreaseSupply($card)',
    'smithy': '#draw(3)',
    'throne_room': 'c=#chooseSubset(#getSubset(#getHand(), #makeArray(type, =, action)), 1, #false()); #play($c); #execute($c); #execute($c)',
    'bandit': '#gain(#fromStore(gold)); #attack(`top=#fromTop(2); toTrash=#chooseSubset(#getSubset(#getSubset($top, #makeArray(type, =, treasure)), #makeArray(name, !=, copper)), 1, #false()); #discard($top); #trash($toTrash)`)',
    'council_room': '#draw(4); #changeBuys(1); #attack(`#draw(1)`)',
    'festival': '#changeActions(2); #changeBuys(1); #changeCoins(2)',
    'laboratory': '#draw(2); #changeActions(1)',
    'library': 'cards=#fromTop(1); break=#eval(#eval(#count(#getHand()), >=, 7), or, #eval(#count($cards), =, 0)); #cond($break, #discard(#getSetAside())); #cond($break, #endEarly()); actions=#getSubset($cards, #makeArray(type, =, action)); skip=#chooseSubset($actions, -1, #true()); #toHand($cards); #setAside($skip); #execute(#makeCard(library));', #not implemented
    'market': '#draw(1); #changeActions(1); #changeBuys(1); #changeCoins(1)',
    
    'mine':'x=#chooseSubset(#getSubset(#getHand(), #makeArray(type, =, treasure)), 1, #false()); cost=#getCost(#getFirst($x)); #trash($x); options=#getSubset(#getStore(), #makeArray(cost, <=, #eval($cost, +, 3)), #makeArray(type, =, treasure)); card=#chooseSubset($options, 1, #false()); #gain($card, hand); #decreaseSupply($card);',
    'sentry': '#draw(1); #changeActions(1); x=#fromTop(2); toTrash=#chooseSubset($x, 2, #true()); #trash($toTrash); x=#removeFromSet($x, $toTrash); toDiscard=#chooseSubset($x, 2, #true()); #discard($toDiscard); x=#removeFromSet($x, $toDiscard); x=#reorder($x); #toDeck($x)',
    'witch': '#draw(2); #attack(`curse=#fromStore(curse); #gain($curse)`)',
    'artisan': 'card=#chooseSubset(#getSubset(#getStore(), #makeArray(cost, <, 6)), 1, #false()); #gain($card, hand); #decreaseSupply($card); #toDeck(#chooseSubset(#getHand(), 1, #false()))',


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