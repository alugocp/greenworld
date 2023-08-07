import type { Plant, Point } from './defs';
import UiWrapper from './wrapper';

type ReportsTable = Record<number, Record<number, [number, number]>>;

export default class GuildPlacement {
    readonly plants: Plant[] = [
        {
            id: 95,
            name: 'Hopi Turquoise Corn',
            species: 'zea mays'
        },
        {
            id: 96,
            name: 'Hopi Orange Squash',
            species: 'cucurbita maxima'
        },
        {
            id: 97,
            name: 'Hopi Purple String Bean',
            species: 'phaseolus vulgaris'
        },
        {
            id: 98,
            name: 'Hopi Black Dye Sunflower',
            species: 'helianthus annuus'
        },
        {
            id: 99,
            name: 'Purple Passionflower',
            species: 'passiflora incarnata'
        },
        {
            id: 100,
            name: 'American Black Elderberry',
            species: 'sambucus canadensis'
        },
        {
            id: 95,
            name: 'Hopi Turquoise Corn',
            species: 'zea mays'
        },
        {
            id: 99,
            name: 'Purple Passionflower',
            species: 'passiflora incarnata'
        },
        {
            id: 100,
            name: 'American Black Elderberry',
            species: 'sambucus canadensis'
        },
        {
            id: 95,
            name: 'Hopi Turquoise Corn',
            species: 'zea mays'
        }
    ];

    constructor(private readonly baseUrl: string, private readonly wrapper: UiWrapper) {}

    // Adds a plant to the guild list
    addPlant(id: number, name: string, species: string): void {
        this.plants.push({id, name, species});
        this.wrapper.refreshPlantList();
    }

    // Removes a plant from the guild list
    dropPlant(index: number): void {
        this.plants.splice(index, 1);
        this.wrapper.refreshPlantList();
    }

    // Process that places plants in a guild
    async calculate(): Promise<void> {
        const reports: ReportsTable = await this.pullReports();
        // Calculate using FDG
        this.wrapper.drawGuildPlacement([
            { x: 0, y: 0 },
            { x: 1, y: 0 },
            { x: 0, y: 1 },
            { x: -1, y: 0 },
            { x: 0, y: -1 }
        ]);
    }

    // Generate a reports table for the user-selected plant species
    private async pullReports(): Promise<ReportsTable> {
        const table: ReportsTable = {};
        const speciesList: string = [...new Set(this.plants.map((x: Plant): number => x.id))].join(',');
        await fetch(`${this.baseUrl}reports?species_list=${speciesList}`)
            .then((res) => res.json())
            .then((reports: any[]): void[] => reports.map((r: any): void => {
                table[r.plant1] = table[r.plant1] || [];
                table[r.plant2] = table[r.plant2] || [];
                table[r.plant1][r.plant2] = [r.range_union_min, r.range_union_max];
                table[r.plant2][r.plant1] = [r.range_union_min, r.range_union_max];
            }));
        return table;
    }
}
