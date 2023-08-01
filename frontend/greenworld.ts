import GuildPlacement from './placement/placement';
import CompanionSearch from './companions';
import UiWrapper from './wrapper';

export class Greenworld {
    placement: GuildPlacement;
    companions: CompanionSearch;
    wrapper: UiWrapper;

    constructor(private readonly baseUrl: string) {
        this.wrapper = new UiWrapper();
        this.placement = new GuildPlacement(baseUrl);
        this.companions = new CompanionSearch(baseUrl, this.wrapper);
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
