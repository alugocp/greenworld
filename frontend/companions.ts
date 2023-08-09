import type { Greenworld } from './greenworld';
import type { PlantHandle } from './defs';
import type UiWrapper from './wrapper';

// Query options for the companion search app
interface CompanionSearchQuery {
    id: number
    previous: number | null
};

export default class CompanionSearch {
    constructor(private readonly gw: Greenworld, private readonly baseUrl: string, private readonly wrapper: UiWrapper) {}

    getSearchLink(plant: PlantHandle): string {
        return `<a onclick="renderCompanions(${plant.id}, \`${plant.name}\`, '${plant.species}')">${plant.name} (<i>${plant.species}</i>)</a>`;
    }

    getLink(plant: PlantHandle, species: string): string {
        return `${plant.name} (<i>${plant.species}</i>) - <a onclick="renderCompanions(${plant.id}, \`${plant.name}\`, '${plant.species}')">Find companions</a>, <a href="${this.gw.getPlantsUrl(plant.species, species)}">View report</a>`;
    }

    // Companion search algorithm from a given plant ID
    async discover(query: CompanionSearchQuery): Promise<PlantHandle[]> {

        // Grab neighbor IDs, then get handlers for these IDs
        let neighborsUrl: string = `${this.baseUrl}neighbors/${query.id}`;
        if (query.previous !== null) {
            neighborsUrl += `/${query.previous}`;
        }
        const ids: number[] = await this.wrapper.fetch(neighborsUrl);
        const handlers: PlantHandle[] = await this.wrapper.fetch(`${this.baseUrl}handlers?ids=${ids.join(',')}`);
        return handlers.sort((a, b) => ids.indexOf(a.id) - ids.indexOf(b.id));
    }
}
