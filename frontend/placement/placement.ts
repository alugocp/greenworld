import type { PlantHandle, Guild } from '../defs';
import type { GuildAlgorithm } from './algorithm';
import { Reports } from './algorithm';
import { geometricAlgorithm } from './geometric';
import { dynamicAlgorithm } from './dynamic';

const algorithms: Record<string, GuildAlgorithm> = {
    geometric: geometricAlgorithm,
    dynamic: dynamicAlgorithm
};

export default class GuildPlacement {
    private plants: PlantHandle[] = [
        {
            uid: 1,
            id: 95,
            name: 'Hopi Turquoise Corn',
            species: 'zea mays'
        },
        {
            uid: 2,
            id: 96,
            name: 'Hopi Orange Squash',
            species: 'cucurbita maxima'
        },
        {
            uid: 3,
            id: 97,
            name: 'Hopi Purple String Bean',
            species: 'phaseolus vulgaris'
        },
        {
            uid: 4,
            id: 98,
            name: 'Hopi Black Dye Sunflower',
            species: 'helianthus annuus'
        },
        {
            uid: 5,
            id: 99,
            name: 'Purple Passionflower',
            species: 'passiflora incarnata'
        },
        {
            uid: 6,
            id: 100,
            name: 'American Black Elderberry',
            species: 'sambucus canadensis'
        },
        {
            uid: 7,
            id: 95,
            name: 'Hopi Turquoise Corn',
            species: 'zea mays'
        },
        {
            uid: 8,
            id: 99,
            name: 'Purple Passionflower',
            species: 'passiflora incarnata'
        },
        {
            uid: 9,
            id: 100,
            name: 'American Black Elderberry',
            species: 'sambucus canadensis'
        },
        {
            uid: 10,
            id: 95,
            name: 'Hopi Turquoise Corn',
            species: 'zea mays'
        }
    ];

    constructor(private readonly baseUrl: string) {}

    async calculate(algorithmType: keyof typeof algorithms): Promise<Guild | null> {
        const reports = new Reports();
        await reports.populate(this.baseUrl, this.plants);
        return algorithms[algorithmType](this.plants, reports);
    }

    private orderUids(): void {
        for (let a = 0; a < this.plants.length; a++) {
            this.plants[a].uid = a + 1;
        }
    }

    addPlant(plant: PlantHandle): void {
        this.plants.push(plant);
        this.orderUids();
    }

    dropPlant(uid: number): void {
        this.plants = this.plants.filter((x: PlantHandle): boolean => x.uid !== uid);
        this.orderUids();
    }
}
