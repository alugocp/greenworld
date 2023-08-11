import type { Greenworld } from './greenworld';
import type { PlantHandle } from './defs';
import type UiWrapper from './wrapper';

// Query options for the companion search app
interface CompanionSearchQuery {
    id: number
};

type ScoredPlantHandle = PlantHandle & { score: number };

export default class CompanionSearch {
    constructor(private readonly gw: Greenworld, private readonly baseUrl: string, private readonly wrapper: UiWrapper) {}

    getSearchLink(plant: PlantHandle): string {
        return `<a onclick="renderCompanions(${plant.id}, \`${plant.name}\`, '${plant.species}')">${plant.name} (<i>${plant.species}</i>)</a>`;
    }

    getResultLink(plant: ScoredPlantHandle, species: string): string {
        return `<tr><td>${plant.name}</td><td><i>${plant.species}</i></td><td>${Math.round(plant.score * 1000) / 1000}</td><td><a onclick="renderCompanions(${plant.id}, \`${plant.name}\`, '${plant.species}')">Find companions</a></td><td><a href="${this.gw.getPlantsUrl(plant.species, species)}">View report</a></td></tr>`;
    }

    // Companion search algorithm from a given plant ID
    async discover(query: CompanionSearchQuery): Promise<ScoredPlantHandle[]> {

        // Grab neighbor IDs, then get handlers for these IDs
        let neighborsUrl: string = `${this.baseUrl}neighbors/${query.id}`;
        const idsAndScores: [number, number][] = await this.wrapper.fetch(neighborsUrl);
        const ids = idsAndScores.map((x) => x[0]);
        const handlers: ScoredPlantHandle[] = await this.wrapper.fetch(`${this.baseUrl}handlers?ids=${ids.join(',')}`);
        for (const handler of handlers) {
            handler.score = idsAndScores[ids.indexOf(handler.id)][1];
        }
        return handlers.sort((a, b) => ids.indexOf(a.id) - ids.indexOf(b.id));
    }
}
