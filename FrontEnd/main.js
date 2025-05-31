let inputCount = 1;

function displayInput() {
    inputCount++;

    const container = document.getElementById("input-container");
    const template = document.querySelector(".input-template");

    const newInput = template.cloneNode(true);
    newInput.classList.remove("input-template");

    const inputs = newInput.querySelectorAll('input');
    inputs.forEach(input => input.value = "");

    const radios = newInput.querySelectorAll('input[type="radio"]');
    radios.forEach(radio => {
        radio.name = `time-${inputCount}`;
        radio.checked = false;
    });

    const removeBtn = document.createElement("button");
    removeBtn.innerHTML = `<i class="fa-solid fa-trash"></i> Remove`;
    removeBtn.className = "btn remove-btn";
    removeBtn.type = "button";
    removeBtn.onclick = function () {
        newInput.remove();
    };

    newInput.style.marginTop = "40px";
    newInput.appendChild(removeBtn);

    container.appendChild(newInput);
}

async function generateSchedule() {
    const inputCards = document.querySelectorAll("#input-container .input-card:not(.input-template)");
    const course_sections = [];

    inputCards.forEach(card => {
        const cname = card.querySelector('input[name="cname"]')?.value.trim();
        const prof_id = card.querySelector('input[name="prof_id"]')?.value.trim();
        const start = parseFloat(card.querySelector('input[name="start"]')?.value.trim());
        const end = parseFloat(card.querySelector('input[name="end"]')?.value.trim());

        if (!cname || !prof_id || isNaN(start) || isNaN(end)) return;

        // Wrap each course's sections in a list (only 1 section per course in current setup)
        course_sections.push([{ start, end, prof_id }]);
    });

    const preferredStart = parseFloat(document.getElementById("preferred-start")?.value);
    const preferredEnd = parseFloat(document.getElementById("preferred-end")?.value);

    if (isNaN(preferredStart) || isNaN(preferredEnd)) {
        alert("Please enter a valid preferred time range.");
        return;
    }

    const prof_ratings = {};
    course_sections.flat().forEach(section => {
        if (!(section.prof_id in prof_ratings)) {
            prof_ratings[section.prof_id] = 4.0; // default rating, can be improved later
        }
    });

    const payload = {
        course_sections,
        preferred_range: [preferredStart, preferredEnd],
        prof_ratings
    };

    try {
        const res = await fetch("http://127.0.0.1:8000/generate_schedule/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const data = await res.json();
        document.getElementById("output").textContent = JSON.stringify(data, null, 2);
    } catch (err) {
        console.error("Failed to generate schedule", err);
        alert("An error occurred while generating the schedule.");
    }
}
