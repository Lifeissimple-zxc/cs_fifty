const form = document.querySelector("form"); // Get element
        
form.addEventListener('submit', e => { // Listen to submit event
    if (!form.checkValidity()) {
        e.preventDefault()
    };

    form.classList.add('was-validated');
})

// No need to validate phone unless I have a specific regex in mind
// https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/tel