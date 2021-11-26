// Add new value input
function addValue() {
    let values = document.getElementById('values');
    // Count current input fields
    let x = values.getElementsByTagName('input').length;

    // Create new input field
    let new_input = document.createElement('input');
    let newName = 'value_' + x;
    new_input.type = 'text';
    new_input.className = 'form-control';
    new_input.name = newName;
    new_input.id = newName;
    new_input.required = true;

    values.appendChild(new_input);
}


// Event listener (instead of using onclick)
// https://developers.google.com/web/fundamentals/security/csp
document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('add-value').addEventListener('click', addValue);
});
