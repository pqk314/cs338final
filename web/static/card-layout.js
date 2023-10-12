const cardContainers = document.querySelectorAll(".card-container");
cardContainers.forEach(element => {
    let gridTemplate = ""
    element.querySelectorAll(".card").forEach(() => gridTemplate += "1fr ");
    gridTemplate = gridTemplate.substring(0, gridTemplate.length - 1);
    element.style.gridTemplateColumns = gridTemplate;
})

document.querySelectorAll(".card").forEach(element => {
    element.addEventListener("click", () => cardPlayed(element));
});

function cardPlayed(card) {
    window.location.href =`/${window.location.toString().split('/')[3]}/cardplayed/${card.classList[card.classList.length - 1]}`;
}