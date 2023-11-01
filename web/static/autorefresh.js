var xhr = new XMLHttpRequest();
let url = new URL(window.location.href);
game_id = url.pathname.split('/')[1]
url.pathname = `/gamestateID/${gameID}/`;
//url.port = 5000
xhr.open("GET", url.href, False);
xhr.setRequestHeader('Content-Type', 'application/json');
xhr.send();

last_id = xhr.responseText;

function checkForUpdates() {
    xhr = new XMLHttpRequest();
    url = new URL(window.location.href);
    url.pathname = `/gamestateID/${gameID}/`;
    xhr.open("GET", url.href, False);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send();
    if (xhr.responseText!= last_id) {
        location.reload()
    }
}

document.setInterval(checkForUpdates, 500);