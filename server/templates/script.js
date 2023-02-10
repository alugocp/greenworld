
// Triggers the search button if the enter key is pressed
function check_enter(e) {
    if (e.keyCode === 13) {
        e.preventDefault();
        document.getElementById('search-button').click();
    }
}

// Navigates to a plant page by the entered text
function search_plant() {
    const input = document.getElementById('search-field');
    window.location = `{{ url_for('homepage_endpoint') }}plant/${input.value}`;
}

// Navigates to a report page by the given species and entered text
function search_partner(first) {
    const input = document.getElementById('search-field');
    window.location = `http://localhost:2017/report/${first}/${input.value}`;
}
