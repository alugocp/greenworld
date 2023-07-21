import type { PlantHandle, Guild } from './defs';
import type { GuildAlgorithm } from './guild/algorithm';
import { Reports } from './guild/algorithm';
import { geometricAlgorithm } from './guild/geometric';
import { dynamicAlgorithm } from './guild/dynamic';
import { resetRender, drawGuild, listPlants } from './guild/renderer';

const algorithms: Record<string, GuildAlgorithm> = {
    geometric: geometricAlgorithm,
    dynamic: dynamicAlgorithm
};

let plants: PlantHandle[] = [
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

// Calculates and renders guild plant positions
export async function calculate(canvas: HTMLCanvasElement, plantList: HTMLDivElement, algorithmType: string): Promise<void> {
    let algorithm: GuildAlgorithm = geometricAlgorithm;
    if (algorithms[algorithmType] !== undefined) {
        algorithm = algorithms[algorithmType];
    }
    const reports: Reports = new Reports();
    await reports.populate(plants);
    const guild: Guild | null = algorithm(plants, reports);
    resetRender(canvas, plantList);
    if (guild !== null) {
        listPlants(plantList, guild);
        drawGuild(canvas, guild);
    }
}

function orderUids(): void {
    for (let a = 0; a < plants.length; a++) {
        plants[a].uid = a + 1;
    }
}

export function addPlant(plant: PlantHandle): void {
    plants.push(plant);
    orderUids();
}

export function dropPlant(uid: number): void {
    plants = plants.filter((x: PlantHandle): boolean => x.uid !== uid);
    orderUids();
}
