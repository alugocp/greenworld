import { Plant, CompanionSearchQuery } from './defs';

export default class CompanionSearch {

    constructor(private baseUrl: string) {}

    // Companion search algorithm from a given plant ID and desired threshold
    async discover(query: CompanionSearchQuery): Promise<Plant[]> {
        const threshFixed: string = query.thresh.toFixed(3);

        // Grab neighbor IDs
        const ids: number[] = await fetch(`${this.baseUrl}neighbors/${query.id}/${threshFixed}`)
            .then((res) => res.json());

        // Return handlers for these IDs
        const handlers = await fetch(`${this.baseUrl}handlers?ids=${ids.join(',')}`)
            .then((res) => res.json());
        return handlers;
    }
}