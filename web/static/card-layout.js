document.querySelectorAll(".card").forEach(element => {
    if (element.classList.contains('selectable')) { return; }
    element.addEventListener("click", () => cardPlayed(element));
});

function cardPlayed(card) {
    let card_id = card.id
    let request = new XMLHttpRequest()
    request.open('GET', `cardplayed/${card_id}`, false)
    request.send()
    checkForUpdates(true)
}

function endPhase() {
    let request = new XMLHttpRequest()
    request.open('GET', `endphase/`, false)
    request.send()
    checkForUpdates(true)
}


function toggleSelected(element, max) {
    if (element.classList.contains("selected")) {
        element.classList.remove("selected");
        return
    }
    numSelected = document.querySelectorAll(".selected").length
    if (numSelected < max || max == -1) {
        element.classList.add("selected");
    }
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

    if (xhr.responseText == 'yield') {
        location.reload()
    } else {
        window.location.href =`../`;
    }
    
}