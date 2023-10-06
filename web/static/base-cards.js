const baseCardDiv = document.querySelector("#base-cards");
let gridTemplate = ""
baseCardDiv.querySelectorAll(".buyable").forEach(() => gridTemplate += "1fr ");
gridTemplate = gridTemplate.substring(0, gridTemplate.length - 1);
baseCardDiv.style.gridTemplateColumns = gridTemplate;
