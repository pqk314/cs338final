from flask import render_template

supply = ['cellar', 'moat', 'merchant', 'village', 'workshop', 'smithy', 'remodel', 'militia', 'mine', 'market']

steps = [
    {'page': 'tutorial-front-end.html', 'hand': ['copper', 'copper', 'copper', 'estate', 'estate'], 'message': 'Welcome to Dominion! We\'ll get you playing as soon as we can. If you haven\'t read the rules yet, you should start with that! We have no actions to play right now, so let\'s start by ending our action phase.', 'turn_info': {'Actions': 1, 'Money': 0, 'Buys': 1}, 'end_what': 'End Action', 'click': 'end'},
    {'page': 'tutorial-front-end.html', 'hand': ['copper', 'copper', 'copper', 'estate', 'estate'], 'message': 'Awesome! Now we can play our coppers. I\'ll make you a deal, you play one and I\'ll play the rest.', 'turn_info': {'Actions': 1, 'Money': 0, 'Buys': 1}, 'end_what': 'End Buy', 'click': 'copper'},
    {'page': 'tutorial-front-end.html', 'hand': ['estate', 'estate'], 'message': 'Since each copper is worth one money, we now have 3. Let\'s look at the shop to see what to buy.', 'turn_info': {'Actions': 1, 'Money': 3, 'Buys': 1}, 'end_what': 'End Buy', 'click': 'supply'},
    {'page': 'tutorial-supply.html', 'message': 'Welcome to the shop! Here we can buy anything worth 3 or less because that is how much money we have. We should buy a silver, so we can buy more expensive cards later on.', 'turn_info': {'Money': 3, 'Buys': 1}, 'end_what': 'End Buy', 'click': 'silver'},
    {'page': 'tutorial-supply.html', 'message': 'We\'re out of buys so let\'s end our turn.', 'turn_info': {'Money': 0, 'Buys': 0}, 'end_what': 'End Buy', 'click': 'end'},
    {'page': 'tutorial-front-end.html', 'hand': ['estate'], 'message': 'For your second hand, you always have 4 copper if you started with 3. I played them for you, let\'s go to the market.', 'turn_info': {'Actions': 1, 'Money': 4, 'Buys': 1}, 'end_what': 'End Buy', 'click': 'supply'},
    {'page': 'tutorial-supply.html', 'message': 'We have enough money for an action! Buy a militia so we can get more money.', 'turn_info': {'Money': 0, 'Buys': 1}, 'end_what': 'End Buy', 'click': 'militia'},
    {'page': 'tutorial-front-end.html', 'hand': ['militia', 'copper', 'copper', 'copper', 'estate'], 'message': 'There were no more cards in our deck, so we shuffled our discard pile and it became our new deck. We got super lucky too! Let\'s play a militia since we have an action card now', 'turn_info': {'Actions': 1, 'Money': 0, 'Buys': 1}, 'end_what': 'End Action', 'click': 'militia'},
    {'page': 'tutorial-front-end.html', 'hand': ['copper', 'copper', 'copper', 'estate'], 'message': 'We\'re out of actions, but we got two money from playing militia. Let\'s go to our buy phase.', 'turn_info': {'Actions': 0, 'Money': 2, 'Buys': 1}, 'end_what': 'End Action', 'click': 'end'},
    {'page': 'tutorial-supply.html', 'message': 'I played your treasures for you again. Now you have 5 money. Let\'s buy a mine so we can upgrade our coppers.', 'turn_info': {'Money': 5, 'Buys': 1}, 'end_what': 'End Buy', 'click': 'mine'},
    {'page': 'tutorial-front-end.html', 'hand': ['estate', 'estate', 'copper', 'copper', 'mine'], 'message': 'I took a turn for you. We were able to buy a gold, which is a basic treasure worth 3 that costs 6. Now let\'s play mine to upgrade a copper.', 'turn_info': {'Actions': 1, 'Money': 0, 'Buys': 1}, 'end_what': 'End Action', 'click': 'mine'},
    {'page': 'tutorial-front-end.html', 'hand': ['estate', 'estate', 'copper', 'copper'], 'message': 'Click a copper to trash it, permanently removing it from the game.', 'turn_info': {'Actions': 0, 'Money': 0, 'Buys': 1}, 'end_what': 'End Action', 'click': 'copper'},
    {'page': 'tutorial-supply.html', 'message': 'We now get to pick a treasure costing up to three more than it. That means we either get a copper or a silver. Let\'s take a silver', 'turn_info': {'Money': 0, 'Buys': 1}, 'end_what': 'End Buy', 'click': 'silver'},
    {'page': 'tutorial-front-end.html', 'hand': ['estate', 'estate', 'copper', 'silver'], 'message': 'Because mine says "gain to your hand," we get to keep the silver for this turn. Let\'s go to the buy phase.', 'turn_info': {'Actions': 1, 'Money': 0, 'Buys': 1}, 'end_what': 'End Action', 'click': 'end'},
    {'page': 'tutorial-supply.html', 'message': 'I played your treasures for you again. We have three money this turn. We can buy a village to play more actions later on.', 'turn_info': {'Money': 3, 'Buys': 1}, 'end_what': 'End Buy', 'click': 'village'},
    {'page': 'tutorial-front-end.html', 'hand': ['gold', 'silver', 'copper', 'militia', 'estate'], 'message': 'Woah! What a great hand. Let\'s start by playing militia.', 'turn_info': {'Actions': 1, 'Money': 0, 'Buys': 1}, 'end_what': 'End Action', 'click': 'militia'},
    {'page': 'tutorial-front-end.html', 'hand': ['gold', 'silver', 'copper', 'estate'], 'message': 'I ended your action phase. Let\'s play gold.', 'turn_info': {'Actions': 0, 'Money': 2, 'Buys': 1}, 'end_what': 'End Buy', 'click': 'gold'},
    {'page': 'tutorial-supply.html', 'message': 'I played your treasures for you again. We have 8 money! Let\'s buy a province.', 'turn_info': {'Money': 8, 'Buys': 1}, 'end_what': 'End Buy', 'click': 'province'},
    {'page': 'tutorial-completion.html'}
]

def do_step(step_num, card_pics):
    return render_template(steps[step_num]['page'], step=step_num, card_pics=card_pics, tutorial_step=steps[step_num], cards=supply)
