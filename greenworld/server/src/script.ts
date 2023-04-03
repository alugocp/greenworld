
const cachedData = window as unknown as {
    greenworld_cached_html: string;
    greenworld_content: string;
};

// Triggers the search button if the enter key is pressed
function searchBarOnKeyDown(e: KeyboardEvent, plantToUrl: (_: string) => string) {
    if (e.keyCode === 13) {
        e.preventDefault();
        document.getElementById('search-button').click();
    } else {
        const content: string = (document.getElementById('search-field') as HTMLInputElement).value;
        const results: HTMLElement = document.getElementById('search-results');
        if (content.length >= 3) {
            if (cachedData.greenworld_content === content) {
                results.innerHTML = cachedData.greenworld_cached_html;
            } else {
                cachedData.greenworld_content = content;
                fetch(`{{ url_for('homepage_endpoint') }}search/${content}`)
                    .then(r => r.json())
                    .then((data) => {
                        cachedData.greenworld_cached_html = data
                            .map((plant: any): string => `<a href = "{{ url_for('homepage_endpoint') }}${plantToUrl(plant[0])}">${plant[1]} (${plant[0]})</a>`)
                            .reduce((acc: string, x: string): string => acc + x, '');
                        results.innerHTML = cachedData.greenworld_cached_html;
                    });
            }
        } else {
            results.innerHTML = '';
        }
    }
}

// Navigates to a page page by the entered text
function navigate(plantToUrl: (_: string) => string) {
    const input: HTMLInputElement = document.getElementById('search-field') as HTMLInputElement;
    window.location.assign(`{{ url_for('homepage_endpoint') }}${plantToUrl(input.value)}`);
}
