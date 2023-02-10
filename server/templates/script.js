
// Triggers the search button if the enter key is pressed
function searchBarOnKeyDown(e, plantToUrl) {
    if (e.keyCode === 13) {
        e.preventDefault();
        document.getElementById('search-button').click();
    } else {
        const content = document.getElementById('search-field').value;
        const results = document.getElementById('search-results');
        console.log(content);
        if (content.length >= 3) {
            fetch(`{{ url_for('homepage_endpoint') }}search/${content}`)
            .then(r => r.json())
            .then((data) => {
                console.log(plantToUrl);
                results.innerHTML = data
                    .map(plant => `<a href = "{{ url_for('homepage_endpoint') }}${plantToUrl(plant[0])}">${plant[1]} (${plant[0]})</a>`)
                    .reduce((acc, x) => acc + x, '');
            });
        } else {
            results.innerHTML = '';
        }
    }
}

// Navigates to a page page by the entered text
function navigate(plantToUrl) {
    const input = document.getElementById('search-field');
    window.location = `{{ url_for('homepage_endpoint') }}${plantToUrl(input.value)}`;
}
