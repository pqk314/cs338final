macros = {
    'cantrip': '#draw(1); #changeActions(1)',
    'resetText': '#setText(Left click a card to play it.)'
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
    'cellar': '#changeActions(1); #setText(Choose any number of cards to discard); x=#chooseSubset(#getHand(), -1, #true()); #discard($x); #draw(#count($x)); &resetText',
    'chapel': '#setText(Choose up to 4 cards to trash); #trash(#chooseSubset(#getHand(), 4, #true())); &resetText',
    'moat': '#draw(2)',
    'harbinger': '&cantrip; #setText(Choose up to 1 card to put on top of your deck); #toDeck(#chooseSubset(#getDiscard(), 1, #true())); &resetText',
    'merchant': '&cantrip; #merchant()',
    'vassal': '#changeCoins(2); #setText(Choose up to 1 action to play); x=#getFirst(#fromTop(1)); #discard($x); actions=#getSubset($x, #makeArray(type, =, action)); toPlay=#chooseSubset($actions, 1, #true()); #cond(#eval(#count($toPlay), >, 0), #play($toPlay)); #cond(#eval(#count($toPlay), >, 0), #execute(#getFirst($toPlay))); &resetText',
    'village': '#draw(1); #changeActions(2)',
    'workshop': '#setText(Choose a card to gain); card=#chooseSubset(#getSubset(#getStore(), #makeArray(cost, <, 5)), 1, #false()); #gain($card); #decreaseSupply($card); &resetText',
    'bureaucrat': '#gain(#fromStore(silver), deck); #attack(`#setText(Choose a victory card to put on top of your deck); options=#getSubset(#getHand(), #makeArray(type, =, victory)); #toDeck(#chooseSubset($options, 1, #false())); #cond(#eval(#count($options), = , 0), #reveal(#getHand(), Player reveals their hand with no victory cards:)); &resetText; `)',
    'militia': '#changeCoins(2); #attack(`x=#eval(#count(#getHand()), -, 3); #setText(Choose {} cards to discard, $x); #cond(#eval($x, >, 0), #set(toDiscard, #chooseSubset(#getHand(), $x, #false()))); #cond(#eval($x, >, 0), #discard($toDiscard)); #cond(#eval($x, >, 0), #reveal($toDiscard, Player discarded:)); &resetText; `)',
    'moneylender': 'x=#getSubset(#getHand(), #makeArray(name, =, copper)); #setText(Choose up to one Copper to trash); toTrash=#chooseSubset($x, 1, #true()); willTrash=#false(); #cond(#eval(#count($toTrash), >, 0), #set(willTrash, #true())); #cond($willTrash, #trash($toTrash)); #cond($willTrash, #changeCoins(3)); &resetText',
    'poacher': '&cantrip; #changeCoins(1); x=#eval(17, -, #count(#getStore())); #setText(Choose {} cards to discard, $x); #discard(#chooseSubset(#getHand(), $x, #false())); &resetText',
    'remodel': '#setText(Choose a card to trash); x=#chooseSubset(#getHand(), 1, #false()); cost=#getCost(#getFirst($x)); #trash($x); options=#getSubset(#getStore(), #makeArray(cost, <=, #eval($cost, +, 2))); #setText(Choose a card to gain); card=#chooseSubset($options, 1, #false()); #gain($card); #decreaseSupply($card); &resetText',
    'smithy': '#draw(3)',
    'throne_room': '#setText(Choose up to one action to play); c=#chooseSubset(#getSubset(#getHand(), #makeArray(type, =, action)), 1, #true()); #play($c); &resetText; #execute($c); #execute($c)',
    'bandit': '#gain(#fromStore(gold)); #attack(`top=#fromTop(2); #reveal($top, Player discarded:); #setText(Choose a treasure card besides a Copper to trash); toTrash=#chooseSubset(#getSubset(#getSubset($top, #makeArray(type, =, treasure)), #makeArray(name, !=, copper)), 1, #false()); #discard($top); #trash($toTrash); &resetText; `)',
    'council_room': '#draw(4); #changeBuys(1); #attack(`#draw(1)`)',
    'festival': '#changeActions(2); #changeBuys(1); #changeCoins(2)',
    'laboratory': '#draw(2); #changeActions(1)',
    'library': 'cards=#fromTop(1); break=#eval(#eval(#count(#getHand()), >=, 7), or, #eval(#count($cards), =, 0)); #cond($break, #discard(#getSetAside())); #cond($break, #endEarly()); actions=#getSubset($cards, #makeArray(type, =, action)); #setText(Choose up to one action to set aside); skip=#chooseSubset($actions, -1, #true()); &resetText; #toHand($cards); #setAside($skip); #execute(#makeCard(library));',
    'market': '&cantrip; #changeBuys(1); #changeCoins(1)',
    
    'mine':'#setText(Choose up to one treasure to trash); x=#chooseSubset(#getSubset(#getHand(), #makeArray(type, =, treasure)), 1, #true()); cost=#getCost(#getFirst($x)); #trash($x); options=#getSubset(#getStore(), #makeArray(cost, <=, #eval($cost, +, 3)), #makeArray(type, =, treasure)); #setText(Choose a treasure to gain to your hand); card=#chooseSubset($options, 1, #false()); #gain($card, hand); #decreaseSupply($card); &resetText',
    'sentry': '&cantrip; x=#fromTop(2); #setText(Choose any number of cards to trash); toTrash=#chooseSubset($x, 2, #true()); #trash($toTrash); x=#removeFromSet($x, $toTrash); #setText(Choose any number of cards to discard); toDiscard=#chooseSubset($x, 2, #true()); #discard($toDiscard); x=#removeFromSet($x, $toDiscard); #toDeck($x); #setText(Choose a card to have on top of your deck); x=#chooseSubset($x, 1, #false()); #toDeck($x); &resetText',
    'witch': '#draw(2); #attack(`curse=#fromStore(curse); #gain($curse)`)',
    'artisan': '#setText(Choose a card to gain to your hand); card=#chooseSubset(#getSubset(#getStore(), #makeArray(cost, <, 6)), 1, #false()); #gain($card, hand); #decreaseSupply($card); #setText(Choose a card to put on top of your deck); #toDeck(#chooseSubset(#getHand(), 1, #false())); &resetText',


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