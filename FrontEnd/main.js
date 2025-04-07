let inputCount = 1;

function displayInput() {
    inputCount++;

    const container = document.getElementById("input-container");
    const template = document.querySelector(".input-template");

    // Clone the input card deeply
    const newInput = template.cloneNode(true);

    // Remove 'input-template' class from clone to avoid re-selecting
    newInput.classList.remove("input-template");

    // Reset text input
    const textInput = newInput.querySelector('input[type="text"]');
    if (textInput) textInput.value = "";

    // Update radio button names so each group is unique
    const radios = newInput.querySelectorAll('input[type="radio"]');
    radios.forEach(radio => {
        radio.name = `time-${inputCount}`;
        radio.checked = false;
    });

    // Add remove button to cloned input card
    const removeBtn = document.createElement("button");
    removeBtn.innerHTML = `<i class="fa-solid fa-trash"></i> Remove`;
    removeBtn.className = "btn remove-btn";
    removeBtn.type = "button";
    removeBtn.onclick = function () {
        newInput.remove();
    };

    // Add margin between blocks and append remove button
    newInput.style.marginTop = "40px";
    newInput.appendChild(removeBtn);

    // Append the new input card
    container.appendChild(newInput);
}