document.querySelectorAll(".card").forEach(element => {
    element.addEventListener("click", () => cardPlayed(element));
});

function cardPlayed(card) {
    window.location.href =`/${window.location.toString().split('/')[3]}/cardplayed/${card.id}`;
}