// Read data from our const.json, reads const.json to response variable
// let JSON_DATA;
// let ACCOUNT_SUMMARY;

async function main() {

    let JSON_DATA;
    let ACCOUNT_SUMMARY;
    while (!JSON_DATA) {
        JSON_DATA = await fetchConst();
        await new Promise(resolve => setTimeout(resolve, 1000)); // wait for 1000 milisec before trying again
    }
    ACCOUNT_SUMMARY = JSON_DATA["ACCOUNT_SUMMARY"];

    getClientTimezone(JSON_DATA["CLIENT_TZ_ELEMENT_NAME"]); // Fetch our client's timezone

    // Code for controlling rounding of user's input when buying / selling shares
    // Locate shares element
    try {
        const sharesField = document.querySelector("[name = 'shares']");
        // Listen to user's input
        sharesField.addEventListener('change', e => {
            // Get current value
            const sharesVal = sharesField.value;
            // Truncate to two decimals
            let newSharesValue = Math.trunc(parseFloat(sharesVal));
            // Convert to string
            newSharesValue = newSharesValue.toString();
            // Write to field
            sharesField.value = newSharesValue;
        });
    } catch (error) {
        console.warn("Failed to locate shares element");
    }

    // Code that adds popovers when users hovers over elements
    // Locate elements that need popovers
    const elsForPopovers = document.querySelectorAll('.data-account-text');
    elsForPopovers.forEach(element => {

        element.addEventListener('mouseover', () => {
            showPopover(element, ACCOUNT_SUMMARY);
        })

        element.addEventListener('mouseout', () => {
            hidePopover(element);
        })
    });
}

async function fetchConst() {
    try {
        const response = await fetch('static/const.json');
        const data = await response.json();
        console.log(data);
        return data
    } catch (error) {
        console.error(error);
    }
}


// Code for showing extra info on account data metrics
// Funcs for showing and hiding popovers
function showPopover(element, acc_summary) {
    const elementIdValue = element.id;
    let popoverText;
    if (element.id === 'cash') {
        popoverText = acc_summary['cash']['popover'];
    } else if (element.id === 'net_worth') {
        popoverText = acc_summary['net_worth']['popover'];
    } else {
        // If we get here, smth is off so writing to console + returning
        console.error(`Got an unexpected element id: ${elementIdValue}`);
        return; // probably not the best practice
    };

    // If we don't return from the block above, can proceed to the below lines
    const popover = document.createElement('div');
    popover.classList.add('data-extra-popover');
    popover.classList.add('data-account-metrics-popover');
    popover.textContent = popoverText;

    // Decide on where to place the element, chatGPT helped ehre
    const { left, top, width, height } = element.getBoundingClientRect(); // This gives an object and we take the needed keys
    popover.style.left = `${left + width}px`;
    popover.style.top = `${top + height}px`;

    // Show our popover
    popover.style.display = 'block';
    element.appendChild(popover);
}

function hidePopover(element) {
    // Here we just need to remove the popover we added earlier
    const toRemove = element.querySelectorAll('.data-extra-popover');
    toRemove.forEach(item => {
        item.remove();
    });
}

function getClientTimezone(elementName) {
    // Get client timezone
    const tzOffset = new Date().getTimezoneOffset();
    // Add this info to the page as input element
    // This shares the info with the backend
    const formElement = document.querySelector('form');
    if (!formElement) {
        console.warn("No form on page");
        return;
    }
    // Create a new form input element
    const tzElement = document.createElement('input');
    // Set the needed attributes
    tzElement.setAttribute('type', 'hidden'); // Makes sure it is now show in the page
    // Name to for backend to parse data
    tzElement.setAttribute('name', elementName);
    tzElement.setAttribute('value', tzOffset);
    // Append element to the form
    formElement.appendChild(tzElement);
}

////////////////////////////CALLING MAIN HERE//////////////////////////////////

main();