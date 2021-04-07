const inputField = document.getElementById("input-field")
const characterCountOutput = document.getElementById("character-count")

inputField.addEventListener("input", (e) => {
    const characterCount = e.target.value.length;
    characterCountOutput.innerText = characterCount;
})
