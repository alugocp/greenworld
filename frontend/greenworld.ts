import GuildPlacement from './guild';

export class Greenworld {
    guild: GuildPlacement;

    constructor(private readonly baseUrl: string) {
        this.guild = new GuildPlacement(baseUrl);
    }

    /**
     * Converts 1 or 2 plant species into a valid URL
     */
    getPlantsUrl(plant1: string, plant2?: string): string {
        return plant2 !== undefined
            ? `${this.baseUrl}report/${plant1}/${plant2}`
            : `${this.baseUrl}plant/${plant1}`;
    }
}
