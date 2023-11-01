var xhr = new XMLHttpRequest();
let url = new URL(window.location.href);
game_id = url.pathname.split('/')[1]
url.pathname = `/gamestateID/${game_id}/`;
//url.port = 5000
xhr.open("GET", url.href, false);
xhr.setRequestHeader('Content-Type', 'application/json');
xhr.send();

last_id = xhr.responseText;

function checkForUpdates() {
    xhr = new XMLHttpRequest();
    url = new URL(window.location.href);
    url.pathname = `/gamestateID/${game_id}/`;
    xhr.open("GET", url.href, false);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send();
    if (xhr.responseText!= last_id) {
        location.reload()
    }
}


setInterval(checkForUpdates, 500);