
const cachedData = {
    greenworld_cached_html: '',
    greenworld_content: ''
};

// Triggers the search button if the enter key is pressed
export function searchBarOnKeyDown(e: KeyboardEvent, plantToUrl: (_: string) => string): void {
    const baseUrl: string = (window as any).gw.base_url as string;
    if (e.keyCode === 13) {
        e.preventDefault();
        document.getElementById('search-button')?.click();
    } else {
        const content: string = (document.getElementById('search-field') as HTMLInputElement).value;
        const results: HTMLElement | null = document.getElementById('search-results');
        if (results === null) {
            return;
        }
        if (content.length >= 3) {
            if (cachedData.greenworld_content === content) {
                results.innerHTML = cachedData.greenworld_cached_html;
            } else {
                cachedData.greenworld_content = content;
                void fetch(`${baseUrl}search/${content}`)
                    .then((r) => r.json())
                    .then((data) => {
                        cachedData.greenworld_cached_html = data
                            .map((plant: any): string => `<a href = "${baseUrl}${plantToUrl(plant[0] as string)}">${plant[1] as string} (${plant[0] as string})</a>`)
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
export function navigate(plantToUrl: (_: string) => string): void {
    const baseUrl: string = (window as any).gw.base_url as string;
    const input: HTMLInputElement = document.getElementById('search-field') as HTMLInputElement;
    window.location.assign(`${baseUrl}${plantToUrl(input.value)}`);
}
