var xhr = new XMLHttpRequest();
let url = new URL(window.location.href);
game_id = url.pathname.split('/')[1]
checkForUpdates(false)

function checkForUpdates(makeChanges) {
    xhr = new XMLHttpRequest();
    let url = window.location.href + '/updates/'
    xhr.open("GET", url, false);
    xhr.send();
    let updates = JSON.parse(xhr.responseText)
    if(Object.keys(updates).length > 0 && makeChanges) change(updates)
}

function change(updates) {
    console.log(updates);
    if(updates.hasOwnProperty('home_page')) window.location.href = "/"
    if(updates.hasOwnProperty('set_coins')) document.querySelector('#money').innerHTML = `Money: ${updates['set_coins']}`
    if(updates.hasOwnProperty('set_actions')) document.querySelector('#actions').innerHTML = `Actions: ${updates['set_actions']}`
    if(updates.hasOwnProperty('set_buys')) document.querySelector('#buys').innerHTML = `Buys: ${updates['set_buys']}`
    if(updates.hasOwnProperty('set_phase')) document.querySelector('#phase').innerHTML = updates['set_phase'] === 'buy' ? 'End Buys' : 'End Action'
    if(updates.hasOwnProperty('select') && updates['select']) doSelect();
    if(updates.hasOwnProperty('add')) {
        for(let i = 0; i < updates['add'].length; i++) {
            let new_card = document.createElement('img')
            new_card.src = card_pics[updates['add'][i]['name']]
            new_card.classList.add('card')
            new_card.classList.add('playable')
            new_card.alt = updates['add'][i]['name']
            new_card.id = 'card' + updates['add'][i]['id']
            new_card.addEventListener("click", () => cardPlayed(new_card));
            document.querySelector('#hand').appendChild(new_card)
        }
    }
    if(updates.hasOwnProperty('remove')) {
        for(let i = 0; i < updates['remove'].length; i++) {
            document.querySelector('#hand').removeChild(document.querySelector(`#card${updates['remove'][i]['id']}`))
        }
    }
    if(updates.hasOwnProperty('play')) {
        for(let i = 0; i < updates['play'].length; i++) {
            document.querySelector('#in-play').appendChild(Object.assign(document.createElement('img'), {
                src: card_pics[updates['play'][i]],
                alt: updates['play'][i],
                className: 'card'
                }
            ));
        }
    }

    if (updates.hasOwnProperty(`${playerNum}_deck_size`)) document.querySelector('#deck-info p:nth-child(2)').innerHTML = `Your Deck: ${updates[`${playerNum}_deck_size`]} cards`
    if (updates.hasOwnProperty(`${playerNum}_discard_size`)) document.querySelector('#deck-info p:nth-child(3)').innerHTML = `Your Discard: ${updates[`${playerNum}_discard_size`]} cards`

    if(playerNum !== 1) {
        if (updates.hasOwnProperty('1_deck_size')) document.querySelector('#deck-info p:nth-child(4)').innerHTML = `Player 1's deck: ${updates['1_deck_size']} cards`
        if (updates.hasOwnProperty('1_hand_size')) document.querySelector('#deck-info p:nth-child(5)').innerHTML = `Player 1's hand: ${updates['1_hand_size']} cards`
        if (updates.hasOwnProperty('1_discard_size')) document.querySelector('#deck-info p:nth-child(6)').innerHTML = `Player 1's deck: ${updates['1_discard_size']} cards`
    } else {
        if (updates.hasOwnProperty('2_deck_size')) document.querySelector('#deck-info p:nth-child(4)').innerHTML = `Player 2's deck: ${updates['2_deck_size']} cards`
        if (updates.hasOwnProperty('2_hand_size')) document.querySelector('#deck-info p:nth-child(5)').innerHTML = `Player 2's hand: ${updates['2_hand_size']} cards`
        if (updates.hasOwnProperty('2_discard_size')) document.querySelector('#deck-info p:nth-child(6)').innerHTML = `Player 2's deck: ${updates['2_discard_size']} cards`
    }

    if(updates.hasOwnProperty('new_turn')) {
        document.querySelectorAll('#in-play img').forEach(element => document.querySelector('#in-play').removeChild(element));
        isTurn()
    }
}

function isTurn() {
    xhr = new XMLHttpRequest();
    let url = window.location.href + '/turnnumber/'
    xhr.open('GET', url, false);
    xhr.send();
    let current = parseInt(xhr.responseText)
    if(current !== playerNum) {
        document.querySelector('#turn-blocker').style.display = 'block';
        document.querySelector('#turn-text').style.display = 'inline';
        document.querySelector('#turn-text').innerHTML = `It is Player ${current}'s turn.`;
    } else {
        document.querySelector('#turn-blocker').style.display = 'none';
        document.querySelector('#turn-text').style.display = 'none';
    }
}

function doSelect() {
    xhr = new XMLHttpRequest();
    // url = new URL(window.location.href);
    // url.pathname = `/${game_id}/selectinfo/`;
    let url = window.location.href + '/selectinfo/'
    xhr.open("GET", url, false);
    xhr.send();
    let selection = JSON.parse(xhr.responseText)
    if(Object.keys(selection).length === 0) return;
    selection['can_choose_less'] = (selection['can_choose_less'] === 'true')
    document.body.appendChild(Object.assign(document.createElement('div'), {
        className: 'blocker'
    }));

    let selectContainer = document.body.appendChild(Object.assign(document.createElement('div'), {
        id: 'select',
        className: 'select card-container'
    }));

    for(let i = 0; i < selection['options'].length; i++) {
        let newCard = selectContainer.appendChild(Object.assign(document.createElement('img'), {
            src: card_pics[selection['options'][i]['name']],
            className: 'card selectable',
            alt: selection['options'][i]['name'],
            id: selection['options'][i]['id'],
        }))
        newCard.addEventListener('click', () => toggleSelected(newCard, selection['max_num'], selection['can_choose_less']))
    }
    selectContainer.appendChild(document.createElement('br'));
    selectContainer.appendChild(Object.assign(document.createElement('button'), {
        id: 'submit-selection',
        onclick: () => sendSelection(selection['max_num'], selection['can_choose_less']),
        innerHTML: 'Submit'
    }));
    submitButton(selection['max_num'], selection['can_choose_less']);
}


setInterval(() => checkForUpdates(true), 500);