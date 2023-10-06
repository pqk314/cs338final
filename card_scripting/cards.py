cards = {
    'cellar': 'x=#chooseSubset(#getHand(), -1, T); #discard($x); #draw(#count($x))',
    'chapel': '#trash(#fromHand(4, T))',
    'moat': '#draw(2)',
    'harbinger': '#draw(1); #changeActions(1); #toDeck(#fromDiscard(1, T))',
    'merchant': '#draw(1); #changeActions(1); somethingelse#', #not implemented
    'vassal': '#changeCoins(2); x=#getFirst(#fromTop(1)); #discard($x); #cond(#eval(#getType($x), =, action), #cond(#getChoice("Play {}?", #getName($x)), #play($x)))',
    'village': '#draw(1); #changeActions(2)',
    'workshop': '#gain(#chooseSubset(#getSubset(#getStore(), #makeArray(cost, <, 5)), 1, F))',
    'bureaucrat': '', #not implemented
    'militia': '', #not implemented
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

