const ALLOWED_DAYS = {
    // With 0 we emulate the lowest # of days possible
    0: [...Array(28).keys()].map(x => x + 1),
    1: [...Array(31).keys()].map(x => x + 1),
    2: [...Array(28).keys()].map(x => x + 1),
    3: [...Array(31).keys()].map(x => x + 1),
    4: [...Array(30).keys()].map(x => x + 1),
    5: [...Array(31).keys()].map(x => x + 1),
    6: [...Array(30).keys()].map(x => x + 1),
    7: [...Array(31).keys()].map(x => x + 1),
    8: [...Array(31).keys()].map(x => x + 1),
    9: [...Array(30).keys()].map(x => x + 1),
    10: [...Array(31).keys()].map(x => x + 1),
    11: [...Array(30).keys()].map(x => x + 1),
    12: [...Array(31).keys()].map(x => x + 1)
};

// Locate our selectors, one for listening, one for appending options under
const monthSelector = document.querySelector("[name = 'month']")
const daySelector = document.querySelector("[name = 'day']")

// Listen to any change in the selector
monthSelector.addEventListener('input', e => {
    // Reset value
    // daySelector.selectedIndex = 0;
    // Remove children from the previous events if there are any
    while (daySelector.childNodes.length > 1) {
        daySelector.removeChild(daySelector.lastChild);
    }
    const selectedVal = monthSelector.value;
    // Handle when no month is chosen
    if (selectedVal) {
        // Look up our allowed days array
        const days = ALLOWED_DAYS[parseInt(selectedVal)];
        // Add options to the selector
        days.forEach(day => {
            // Create our option element
            const newOption = document.createElement('option');
            // Add data to the element
            newOption.value = day;
            newOption.innerHTML = day;
            // Append option under days selector
            daySelector.appendChild(newOption);
        })
    };
})


