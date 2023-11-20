let xhr = new XMLHttpRequest();
let url = new URL(window.location.href);
game_id = url.pathname.split('/')[1]
checkForUpdates(false)

/**
 * This gets the latest updates from the backend for the player whose window is calling this.
 * @param makeChanges tells page whether there should be refreshes (always true except at in line 4)
 */
function checkForUpdates(makeChanges) {
    xhr = new XMLHttpRequest();
    let url = window.location.href + '/updates/'
    xhr.open("GET", url, false);
    xhr.send();
    let updates = JSON.parse(xhr.responseText)
    if((Object.keys(updates).length > 0 && makeChanges) || updates.hasOwnProperty('new_game_prompt')) change(updates)
}

/**
 * Makes changes to front end page based on the updates JSON
 * @param updates JSON containing info for updating front end page
 */
function change(updates) {
    // prompts player to invite friend
    console.log(updates);
    if(updates.hasOwnProperty('new_game_prompt')) {
        document.querySelector('#info-text').innerHTML = `To invite friend, send them this link: http://${window.location.host}/joingame/${game_id}\nIf you finish your first turn before they join. They will no longer be able to join and you will play against an AI player.`
        return;
    }

    // This is only for if the game_id doesn't exist like if a docker container restarted
    if(updates.hasOwnProperty('home_page')) window.location.href = "/"

    // Redirects to game over page if the game has ended
    if(updates.hasOwnProperty('game_over')) window.location.href = 'gameover'

    // these simply set the game variables to the values associated with their respective keys
    if(updates.hasOwnProperty('set_coins')) document.querySelector('#money').innerHTML = `Money: ${updates['set_coins']}`
    if(updates.hasOwnProperty('set_actions')) document.querySelector('#actions').innerHTML = `Actions: ${updates['set_actions']}`
    if(updates.hasOwnProperty('set_buys')) document.querySelector('#buys').innerHTML = `Buys: ${updates['set_buys']}`
    if(updates.hasOwnProperty('set_phase')) document.querySelector('#phase').innerHTML = updates['set_phase'] === 'buy' ? 'End Buys' : 'End Action'

    // calls select function to handle things if select is needed
    if(updates.hasOwnProperty('select') && updates['select']) doSelect();

    // adds cards for list under add key.
    if(updates.hasOwnProperty('add')) addCards(updates['add'])

    // removes specified cards
    if(updates.hasOwnProperty('remove')) removeCards(updates['remove'])

    // adds card to in-play zone
    if(updates.hasOwnProperty('play')) playCards(updates['play'])

    // these are responsible for regulating the deck/discard/hand size texts.
    if (updates.hasOwnProperty('size_update')) updateSizes(updates['size_update'])

    // this only removes in play cards and then checks whether the barrier should be removed, put up, or neither
    if(updates.hasOwnProperty('new_turn')) document.querySelectorAll('#in-play img').forEach(element => document.querySelector('#in-play').removeChild(element));

    // puts up or removes barrier with instructions given by backend.
    if(updates.hasOwnProperty('barrier')) setBarrier(updates['barrier'])

    // updates info-text with appropriate text from backend.
    if(updates.hasOwnProperty('text')) document.querySelector('#info-text').innerHTML = updates['text']
}

/**
 * Puts up or removes barrier and sets it to say what was specified in updates.
 */
function setBarrier(barrier) {
    if(barrier.length !== 0) {
        document.querySelector('#turn-blocker').style.display = 'block';
        document.querySelector('#turn-text').style.display = 'inline';
        document.querySelector('#turn-text').innerHTML = barrier;
    } else {
        document.querySelector('#turn-blocker').style.display = 'none';
        document.querySelector('#turn-text').style.display = 'none';
    }
}

/**
 * Adds cards to hand by creating elements and their properties.
 * @param cards cards to add
 */
function addCards(cards) {
    for(let i = 0; i < cards.length; i++) {
        let element = document.querySelector('#hand').appendChild(
            Object.assign(
                document.createElement('img'), {
                    src: card_pics[cards[i]['name']],
                    className: 'card playable',
                    alt: cards[i]['name'],
                    id: 'card' + cards[i]['id'],
                    draggable: false
            }))
            element.addEventListener("click", () => cardPlayed(element));
    }
}

/**
 * Removes cards from hand by deleting elements.
 * @param cards cards to remove
 */
function removeCards(cards) {
    for(let i = 0; i < cards.length; i++) {
        document.querySelector('#hand').removeChild(document.querySelector(`#card${cards[i]['id']}`))
    }
}

/**
 * Adds cards to play zone.
 * @param cards cards to remove
 */
function playCards(cards) {
    for(let i = 0; i < cards.length; i++) {
        document.querySelector('#in-play').appendChild(Object.assign(document.createElement('img'), {
                src: card_pics[cards[i]],
                alt: cards[i],
                className: 'card',
                draggable: false
            }
        ));
    }
}

/**
 * Sets up select screen when told to do so if a selection is occurring.
 */
function doSelect() {
    xhr = new XMLHttpRequest();
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

    console.log(document.querySelector('#info-text').getBoundingClientRect().bottom);
    selectContainer.style.top = `${document.querySelector('#info-text').getBoundingClientRect().bottom + window.scrollY}px`

    for(let i = 0; i < selection['options'].length; i++) {
        let newCard = selectContainer.appendChild(Object.assign(document.createElement('img'), {
            src: card_pics[selection['options'][i]['name']],
            className: 'card selectable',
            alt: selection['options'][i]['name'],
            id: selection['options'][i]['id'],
            draggable: false
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
    document.querySelector('#info-text').style.color = 'white'
}

/**
 * Sets all the deck-info menu to have the right sized decks
 * @param updates contains new deck info
 */
function updateSizes(updates) {
    console.log(updates)
    const deckInfo = document.querySelector('#deck-info');
    deckInfo.querySelectorAll('p').forEach(element => deckInfo.removeChild(element));
    for(let i = 0; i < updates.length; i++) {
        deckInfo.appendChild(Object.assign(document.createElement('p'), {
            innerHTML: updates[i]
        }))
    }
}

// makes the document start checking backend for updates
setInterval(() => checkForUpdates(true), 500);