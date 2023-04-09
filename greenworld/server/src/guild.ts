import type { PlantHandle, Guild } from './defs';
import type { GuildAlgorithm } from './guild/algorithm';
import { Reports } from './guild/algorithm';
import { geometricAlgorithm } from './guild/geometric';
import { resetRender, drawGuild, listPlants } from './guild/renderer';

// Initializes the guild finder module
export async function init(canvas: HTMLCanvasElement, plantList: HTMLDivElement): Promise<void> {
    const plants: PlantHandle[] = [
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
