import type { PlantHandle, Guild } from './defs';
import type { GuildAlgorithm } from './guild/algorithm';
import { Reports } from './guild/algorithm';
import { geometricAlgorithm } from './guild/geometric';
import { resetRender, drawGuild, listPlants } from './guild/renderer';

// Initializes the guild finder module
export async function init(canvas: HTMLCanvasElement, plantList: HTMLDivElement): Promise<void> {
    const plants: PlantHandle[] = [
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

    const reports: Reports = new Reports();
    await reports.populate(plants);
    const algorithm: GuildAlgorithm = geometricAlgorithm;
    const guild: Guild | null = algorithm(plants, reports);
    resetRender(canvas, plantList);
    if (guild !== null) {
        listPlants(plantList, guild);
        drawGuild(canvas, guild);
    }
}
