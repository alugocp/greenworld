import type { PlantHandle } from './defs';
import type UiWrapper from './wrapper';

// Query options for the companion search app
interface CompanionSearchQuery {
    id: number
    thresh: number
    previous: number | null
};

export default class CompanionSearch {
    constructor(private readonly baseUrl: string, private readonly wrapper: UiWrapper) {}

    getLink(plant: PlantHandle): string {
        return `<a onclick="renderCompanions(${plant.id}, \`${plant.name}\`, '${plant.species}')">${plant.name} (<i>${plant.species}</i>)</a>`;
    }

    // Companion search algorithm from a given plant ID and desired threshold
    async discover(query: CompanionSearchQuery): Promise<PlantHandle[]> {
        const threshFixed: string = query.thresh.toFixed(3);

        // Grab neighbor IDs, then get handlers for these IDs
        let neighborsUrl: string = `${this.baseUrl}neighbors/${query.id}/${threshFixed}`;
        if (query.previous !== null) {
            neighborsUrl += `/${query.previous}`;
        }
        const ids: number[] = await this.wrapper.fetch(neighborsUrl);
        const handlers: PlantHandle[] = await this.wrapper.fetch(`${this.baseUrl}handlers?ids=${ids.join(',')}`);
        return handlers;
    }
}