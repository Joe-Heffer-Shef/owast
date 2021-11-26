// Remove the last child element
function deleteValue() {
    let values = document.getElementById('values');
    // Always keep at least one value
    if (values.childElementCount > 1) {
        values.lastChild.remove();
    }
}


// Event listener (instead of using onclick)
// https://developers.google.com/web/fundamentals/security/csp
document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('delete-value').addEventListener('click', deleteValue);
});
