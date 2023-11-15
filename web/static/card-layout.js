document.querySelectorAll(".playable").forEach(element => {
    element.addEventListener("click", () => cardPlayed(element));
});

function cardPlayed(card) {
    let card_id = card.id
    let request = new XMLHttpRequest()
    request.open('GET', `cardplayed/${card_id.substring(4)}`, false)
    request.send()
    checkForUpdates(true)
}

function endPhase() {
    let request = new XMLHttpRequest()
    request.open('GET', `endphase/`, false)
    request.send()
    checkForUpdates(true)
}


function toggleSelected(element, max, canSelectLess) {
    element.classList.toggle('selected')
    submitButton(max, canSelectLess)
}

function submitButton(max, canSelectLess) {
    let numSelected = document.querySelectorAll(".selected").length
    document.querySelector('#submit-selection').disabled = (numSelected > max && max !== -1) || (numSelected < max && !canSelectLess);
}

function sendSelection(max, canSelectLess) {
    let selection = document.querySelectorAll(".selected");
    let numSelected = selection.length
    if (!canSelectLess && numSelected < max) {
        return;
    }
    let ids = Object.values(selection).map(card => parseInt(card.id));
    var xhr = new XMLHttpRequest();
    let url = new URL(window.location.href);
    url.pathname = `/selected/${url.pathname.split('/')[1]}/`;
    //url.port = 5000
    xhr.open("POST", url.href, false);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({
        ids: ids
    }));

    checkForUpdates(true)

    document.querySelector('body').removeChild(document.querySelector('.blocker'));
    document.querySelector('body').removeChild(document.querySelector('#select'));
    if (xhr.responseText === 'yield') {
        doSelect()
    }
}