import type { PlantHandle } from './defs';

const cachedSearchData = {
    html: '',
    term: ''
};

// Returns a link to some plant
export function plantLink(plantToUrl: (_: string) => string): (plant: PlantHandle) => string {
    const baseUrl: string = (window as any).gw.base_url as string;
    return (plant: PlantHandle): string => `<a href = "${baseUrl}${plantToUrl(plant.species)}">${plant.name} (${plant.species})</a>`;
}

// Triggers the search button if the enter key is pressed
export function searchBarOnKeyDown(e: KeyboardEvent, linkTransform: (plant: PlantHandle) => string): void {
    const baseUrl: string = (window as any).gw.base_url as string;
    if (e.keyCode === 13) {
        e.preventDefault();
        document.getElementById('search-button')?.click();
    } else {
        const term: string = (document.getElementById('search-field') as HTMLInputElement).value;
        const results: HTMLElement | null = document.getElementById('search-results');
        if (results === null) {
            return;
        }
        if (term.length >= 3) {
            if (cachedSearchData.term === term) {
                results.innerHTML = cachedSearchData.html;
            } else {
                cachedSearchData.term = term;
                void fetch(`${baseUrl}search/${term}`)
                    .then((r) => r.json())
                    .then((data) => {
                        cachedSearchData.html = data
                            .map(linkTransform)
                            .reduce((acc: string, x: string): string => acc + x, '');
                        results.innerHTML = cachedSearchData.html;
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
