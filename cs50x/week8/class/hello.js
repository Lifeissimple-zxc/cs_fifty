 // function greet()
// {
//     let name = document.querySelector('#name').value; // This is how we select an element by ID
//     alert('hello, ' + name);
// }

// Listen for smth
// Wait till the page loads
document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('form').addEventListener('submit', function(event) {
        let name = document.querySelector('#name').value; // This is how we select an element by ID
        alert('hello, ' + name);
        event.preventDefault(); // This is needed, not clear why though
    });
});