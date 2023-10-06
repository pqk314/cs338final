document.querySelectorAll(".buyable-card").forEach(element => {
    element.addEventListener("click", () => cardBought(element))
})

function cardBought(card) {
    window.location.href =`/cardbought/${card.id}`
}