// Some constants
const FOUNDER = 'Yahiko';
const HOKAGE_8 = 'Naruto Uzumaki';
const FORMS_RESET_TIME_MS = 2000;
const CORRECT_TEXT = 'Correct!';
const INCORRECT_TEXT = 'Incorrect.';
const TEXT_ALERT_SIZE = '12px';
const TEXT_ALERT_COLOR = '#5A5A5A';
const CORRECT_COLOR = 'green';
const INCORRECT_COLOR = 'red';

// Validator for multiple choice
document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('ol').querySelectorAll('button').forEach(
        button => button.addEventListener('click', function(event) {
            const oldColor = button.style.backgroundColor;
            const qElement = document.querySelector('#q1');
            // pre-create our text alert
            const textEl = document.createElement('span');
            // Do some styling for the alert
            qElement.style.display = 'block';
            textEl.style.display = 'block';
            textEl.style.fontSize = TEXT_ALERT_SIZE;
            textEl.style.color = TEXT_ALERT_COLOR;
            // Add child element where we will alert on correct / incorrect answers
            if (qElement.childElementCount == 0)
            {
                qElement.appendChild(textEl); // Acutally add text under question
            }
            // Edit color and text alert
            if (button.innerHTML == FOUNDER)
            {
                button.style.backgroundColor = CORRECT_COLOR; // add color
                textEl.textContent = CORRECT_TEXT; // Add text under question
            }
            else
            {
                // similar logic for incorrect answers
                button.style.backgroundColor = INCORRECT_COLOR;
                textEl.textContent = INCORRECT_TEXT;
            }
            // Restore old state of things
            setTimeout(function() {
                button.style.backgroundColor = oldColor;
                // Remove children text element
                while (qElement.firstChild)
                {
                    qElement.removeChild(qElement.firstChild);
                }
            }, FORMS_RESET_TIME_MS)
            //event.preventDefault(); // This is needed, not clear why though
        })
     );
});
// Validator for free response
document.addEventListener('DOMContentLoaded', function() {
    const submitEl = document.querySelector('#submit_q2');
    submitEl.addEventListener('click', function(event) {
        const formEl = document.querySelector('#open_ended_q');
        const answer = formEl.value;
        const formOldCor = formEl.style.backgroundColor;
        // Prepare element and styling to text alert under question element
        const textEl = document.createElement('span');
        const qElement = document.querySelector('#q2');
        qElement.style.display = 'block';
        textEl.style.display = 'block';
        textEl.style.fontSize = TEXT_ALERT_SIZE;
        textEl.style.color = TEXT_ALERT_COLOR;
        // Add child element where we will alert on correct / incorrect answers
        if (qElement.childElementCount == 0)
        {
            qElement.appendChild(textEl); // Acutally add text under question
        }
        if (answer.toLowerCase() == HOKAGE_8.toLowerCase())
        {
            // Edit text field color and add alert under question
            formEl.style.backgroundColor = CORRECT_COLOR;
            textEl.textContent = CORRECT_TEXT;
        }
        else
        {
            // Edit text field color and add alert under question
            formEl.style.backgroundColor = INCORRECT_COLOR;
            textEl.textContent = INCORRECT_TEXT;
        }
        // Cleanup to reset old state of things
        setTimeout(function() {
            formEl.style.backgroundColor = formOldCor;
            // Remove children text element
            while (qElement.firstChild)
            {
                qElement.removeChild(qElement.firstChild);
            }
        }, FORMS_RESET_TIME_MS)

        // event.preventDefault(); // This is needed, not clear why though
    });
});

// Figure our how to edit colors + how we can make functions more modular