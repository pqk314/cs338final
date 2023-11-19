// sets up playable cards on game page
document.querySelectorAll(".playable").forEach(element => {
    element.addEventListener("click", () => cardPlayed(element));
});

// sets up buyable cards on home page
document.querySelectorAll(".buyable").forEach(element => {
    element.addEventListener("click", () => window.location.href = `cardbought/${element.id}`);
})

// makes images not draggable.
document.querySelectorAll('img').forEach(element => element.draggable = false)

/**
 * Tells backend that a card was played, then updates page
 * @param card the card that was clicked
 */
function cardPlayed(card) {
    let card_id = card.id
    let request = new XMLHttpRequest()
    request.open('GET', `cardplayed/${card_id.substring(4)}`, false)
    request.send()
    checkForUpdates(true)
}

/**
 * Tells backend that the end phase button was clicked. Then updates page.
 */
function endPhase() {
    let request = new XMLHttpRequest()
    request.open('GET', `endphase/`, false)
    request.send()
    checkForUpdates(true)
}

/**
 * Toggles a card that was clicked to add selected to it. Grays out button if an illegal number is selected.
 * @param element which card was clicked
 * @param max maximum number of cards that can be selected (-1 for unlimited)
 * @param canSelectLess whether selecting fewer than max is legal
 */
function toggleSelected(element, max, canSelectLess) {
    element.classList.toggle('selected')
    submitButton(max, canSelectLess)
}

/**
 * Enables/disables submit button on select screen depending on whether the move is legal.
 * @param max maximum number of cards that can be selected (-1 for unlimited)
 * @param canSelectLess whether selecting fewer than max is legal
 */
function submitButton(max, canSelectLess) {
    let numSelected = document.querySelectorAll(".selected").length
    document.querySelector('#submit-selection').disabled = (numSelected > max && max !== -1) || (numSelected < max && !canSelectLess);
}

/**
 * Informs backend of selection choice then checks for updates. If another select is occuring it will immediately
 * reconstruct screen.
 * @param max maximum number of cards that can be selected (-1 for unlimited)
 * @param canSelectLess whether selecting fewer than max is legal
 */
function sendSelection(max, canSelectLess) {
    let selection = document.querySelectorAll(".selected");
    let numSelected = selection.length;
    if ((!canSelectLess && numSelected < max) || (numSelected > max && max !== -1)) {
        return;
    }
    let ids = Object.values(selection).map(card => parseInt(card.id));
    var xhr = new XMLHttpRequest();
    let url = new URL(window.location.href);
    url.pathname = `/selected/${url.pathname.split('/')[1]}/`;
    //url.port = 5000
    xhr.open("POST", url.href, false);
    xhr.setRequestHeader('Content-Type', 'application/json');
    message = { ids: ids, playerNum: playerNum}
    if (playerNum!== null) {
        message.playerNum = playerNum;
    }
    xhr.send(JSON.stringify(message));

    checkForUpdates(true)

    document.querySelector('body').removeChild(document.querySelector('.blocker'));
    document.querySelector('body').removeChild(document.querySelector('#select'));
    if (xhr.responseText === 'yield') {
        doSelect()
    }
}