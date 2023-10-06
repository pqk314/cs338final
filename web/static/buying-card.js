const images = {
    "copper": "static/images/372px-Copper.jpg",
    "silver": "static/images/375px-Silver.jpg",
    "gold": "static/images/375px-Gold.jpg",
    "estate": "static/images/373px-Estate.jpg",
    "duchy": "static/images/372px-Duchy.jpg",
    "province": "static/images/375px-Province.jpg",
    "curse": "static/images/372px-Curse.jpg"
}
document.querySelectorAll(".buyable").forEach(element => {
    element.addEventListener("click", () => cardBought(element));
    element.src = images[element.classList[2]];
});

function cardBought(card) {
    window.location.href =`/cardbought/${card.id}`;
}