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
    if(updates.hasOwnProperty('set_buys')) document.querySelector('#actions').innerHTML = `Buys: ${updates['set_buys']}`
    if(updates.hasOwnProperty('set_phase')) document.querySelector('#phase').innerHTML = updates['set_phase'] === 'buy' ? 'End Buys' : 'End Action'
    if(updates.hasOwnProperty('select') && updates['select']) doSelect();
    if(updates.hasOwnProperty('remove')) {
        for(let i = 0; i < updates['remove'].length; i++) {
            document.querySelector('#hand').removeChild(document.querySelector(`#card${updates['remove'][i]['id']}`))
        }
    }
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
    if(updates.hasOwnProperty('new_turn') && updates['new_turn']) window.location.reload()
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
    submitButton();
}


setInterval(() => checkForUpdates(true), 500);