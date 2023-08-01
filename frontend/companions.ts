import { Plant, CompanionSearchQuery } from './defs';
import UiWrapper from './wrapper';

export default class CompanionSearch {

    constructor(private baseUrl: string, private wrapper: UiWrapper) {}

    getLink(plant: Plant): string {
        return `<a onclick="renderCompanions(${plant.id}, \`${plant.name}\`, '${plant.species}')">${plant.name} (<i>${plant.species}</i>)</a>`;
    }

    // Companion search algorithm from a given plant ID and desired threshold
    async discover(query: CompanionSearchQuery): Promise<Plant[]> {
        const threshFixed: string = query.thresh.toFixed(3);

        // Grab neighbor IDs, then get handlers for these IDs
        const ids: number[] = await this.wrapper.fetch(`${this.baseUrl}neighbors/${query.id}/${threshFixed}`);
        const handlers: Plant[] = await this.wrapper.fetch(`${this.baseUrl}handlers?ids=${ids.join(',')}`);
        return handlers;
    }
}