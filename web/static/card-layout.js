document.querySelectorAll(".card").forEach(element => {
    if (element.classList.contains('selectable')) { return; }
    element.addEventListener("click", () => cardPlayed(element));
});

function cardPlayed(card) {
    window.location.href =`/${window.location.toString().split('/')[3]}/cardplayed/${card.id}`;
}

function sendSelection() {
    let selection = document.querySelectorAll(".selected");
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
    window.location.href =`../`;
}