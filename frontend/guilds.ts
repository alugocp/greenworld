import { Plant } from './defs';

export default class GuildFinder {

    constructor(private baseUrl: string) {}

    // Guild finder algorithm from a given plant ID and desired threshold
    async discover(id: number, thresh: number): Promise<Plant[]> {
        const threshFixed: string = thresh.toFixed(3);

        // Grab neighbor IDs
        const ids: number[] = await fetch(`${this.baseUrl}neighbors/${id}/${threshFixed}`)
            .then((res) => res.json());

        // Return handlers for these IDs
        const handlers = await fetch(`${this.baseUrl}handlers?ids=${ids.join(',')}`)
            .then((res) => res.json());
        return handlers;
    }
}