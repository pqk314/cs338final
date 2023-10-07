const images = {
    "copper": "http://localhost:7555/static/images/372px-Copper.jpg",
    "silver": "http://localhost:7555/static/images/375px-Silver.jpg",
    "gold": "http://localhost:7555/static/images/375px-Gold.jpg",
    "estate": "http://localhost:7555/static/images/373px-Estate.jpg",
    "duchy": "http://localhost:7555/static/images/372px-Duchy.jpg",
    "province": "http://localhost:7555/static/images/375px-Province.jpg",
    "curse": "http://localhost:7555/static/images/372px-Curse.jpg"
}
document.querySelectorAll(".buyable").forEach(element => {
    element.addEventListener("click", () => cardBought(element));
    element.src = images[element.classList[2]];
});

function cardBought(card) {
    window.location.href =`${window.location}/cardbought/${card.id}`;
}