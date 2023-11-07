var xhr = new XMLHttpRequest();
let url = new URL(window.location.href);
game_id = url.pathname.split('/')[1]
checkForUpdates(false)

function checkForUpdates(makeChanges) {
    xhr = new XMLHttpRequest();
    url = new URL(window.location.href);
    url.pathname = `/updates/${game_id}/`;
    xhr.open("GET", url.href, false);
    xhr.send();
    let updates = JSON.parse(xhr.responseText)
    if(Object.keys(updates).length > 0 && makeChanges) change(updates)
}

function change(updates) {
    if(updates.hasOwnProperty('set_coins')) document.querySelector('#money').innerHTML = `Money: ${updates['set_coins']}`
    if(updates.hasOwnProperty('set_actions')) document.querySelector('#actions').innerHTML = `Actions: ${updates['set_actions']}`
    if(updates.hasOwnProperty('set_buys')) document.querySelector('#actions').innerHTML = `Buys: ${updates['set_buys']}`
    if(updates.hasOwnProperty('set_phase')) document.querySelector('#phase').innerHTML = updates['set_phase'] === 'buy' ? 'End Buys' : 'End Action'
    if(updates.hasOwnProperty('select') && updates['select']) window.location.reload()
    if(updates.hasOwnProperty('remove')) {
        for(let i = 0; i < updates['remove'].length; i++) {
            document.querySelectorAll('#hand img').forEach(element => {
                if(parseInt(element.id) === updates['remove'][i]['id']) {
                    document.querySelector('#hand').removeChild(element)
                }
            })
        }
    }
    if(updates.hasOwnProperty('add')) {
        for(let i = 0; i < updates['add'].length; i++) {
            let new_card = document.createElement('img')
            new_card.classList.add('card')
            new_card.id = updates['add'][i]['id']
            new_card.alt = updates['add'][i]['name']
            new_card.src = card_pics[new_card.alt]
            new_card.addEventListener("click", () => cardPlayed(new_card));
            document.querySelector('#hand').appendChild(new_card)
        }
    }
    if(updates.hasOwnProperty('new_turn') && updates['new_turn']) window.location.reload()
}


setInterval(() => checkForUpdates(true), 500);