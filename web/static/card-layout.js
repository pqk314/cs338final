document.querySelectorAll(".card").forEach(element => {
    if (element.classList.contains('selectable')) { return; }
    element.addEventListener("click", () => cardPlayed(element));
});

function cardPlayed(card) {
    window.location.href =`/${window.location.toString().split('/')[3]}/cardplayed/${card.id}`;
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
    if (!canSelectLess & numSelected < max) {
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

/*
    var xhr2 = new XMLHttpRequest();
    let url2 = new URL(window.location.href);
    url2.pathname = `/ischoice/${url2.pathname.split('/')[1]}/`;
    //url.port = 5000
    xhr2.open("GET", url2.href, false);
    xhr2.setRequestHeader('Content-Type', 'application/json');
    xhr2.send */
    
}