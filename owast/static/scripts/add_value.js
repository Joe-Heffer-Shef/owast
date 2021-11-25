// Add new value input
function addValue() {
    console.log('addValue()')
    let values = document.getElementById('values');
    console.log(values)
}


// Event listener (instead of using onclick)
// https://developers.google.com/web/fundamentals/security/csp
document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('add-value').addEventListener('click', addValue);
});
