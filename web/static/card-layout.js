const cardContainers = document.querySelectorAll(".card-container");
cardContainers.forEach(element => {
    let gridTemplate = ""
    element.querySelectorAll(".card").forEach(() => gridTemplate += "1fr ");
    gridTemplate = gridTemplate.substring(0, gridTemplate.length - 1);
    element.style.gridTemplateColumns = gridTemplate;
})

