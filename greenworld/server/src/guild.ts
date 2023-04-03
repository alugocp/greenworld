import type { PlantHandle, Report } from './defs';

// Grab report between two plant species
function getReport(reports: Report[], plant1: PlantHandle, plant2: PlantHandle): Report {
    const lower: number = Math.min(plant1.id, plant2.id);
    const upper: number = Math.max(plant1.id, plant2.id);
    return reports.filter((x: Report): boolean => x.plant1 === lower && x.plant2 === upper)[0];
}

// Initializes the guild finder module
export async function init(): Promise<void> {
    console.log('Find guilds please');
    const plants: PlantHandle[] = [
        {
            id: 1,
            name: 'Hopi Turquoise Corn',
            species: 'zea mays'
        },
        {
            id: 2,
            name: 'Hopi Orange Squash',
            species: 'cucurbita maxima'
        },
        {
            id: 3,
            name: 'Hopi Purple String Bean',
            species: 'phaseolus vulgaris'
        }
    ];

    // Grab reports relevant to the plant list
    const baseUrl: string = (window as any).gw.base_url as string;
    const speciesList: string = plants.map((x: PlantHandle): number => x.id).join(',');
    const reports: Report[] = await fetch(`${baseUrl}reports?species_list=${speciesList}`)
        .then((res) => res.json())
        .then((reports: Report[]) => reports.map((r: Report) => {
            return { ...r, range_union_min: parseFloat(`${r.range_union_min}`), range_union_max: parseFloat(`${r.range_union_max}`) };
        }));

    // Triangulation algorithm
    findTriangle(
        getReport(reports, plants[0], plants[1]),
        getReport(reports, plants[1], plants[2]),
        getReport(reports, plants[0], plants[2])
    );
}

function distance(x: number, y: number): number {
    return Math.round(Math.sqrt(Math.pow(x, 2) + Math.pow(y, 2)) * 1000) / 1000;
}

function buildTriangle(_a: number, _b: number, _c: number): void {
    const theta = Math.acos((Math.pow(_a, 2) + Math.pow(_c, 2) - Math.pow(_b, 2)) / (2 * _a * _c));
    const x = Math.round(Math.cos(theta) * _c * 1000) / 1000;
    const y = Math.round(Math.sin(theta) * _c * 1000) / 1000;
    console.log(`(0, 0) -> ${_a} = ${distance(_a, 0)} -> (${_a}, 0) -> ${_b} = ${distance(x - _a, y)} -> (${x}, ${y}) -> ${_c} = ${distance(x, y)}`);
}

function findTriangle(p12: Report, p23: Report, p13: Report): void {
    let r1: Report;
    let r2: Report;
    let r3: Report;

    // Order the ranges by highest min value
    if (p12.range_union_min >= p23.range_union_min && p12.range_union_min >= p13.range_union_min) {
        r1 = p12;
        r2 = p23;
        r3 = p13;
    } else if (p23.range_union_min >= p12.range_union_min && p23.range_union_min >= p13.range_union_min) {
        r1 = p23;
        r2 = p12;
        r3 = p13;
    } else {
        r1 = p13;
        r2 = p23;
        r3 = p12;
    }

    // Pick the min value of each range
    const l1: number = r1.range_union_min;
    let l2: number = r2.range_union_min;
    let l3: number = r3.range_union_min;
    console.log(r1, r2, r3);

    // If it's already a triangle then return that
    if (l2 + l3 > l1) {
        buildTriangle(l1, l2, l3);
        return;
    }

    // Change shorter sides to try and make a triangle
    l2 = Math.min(r2.range_union_max, l1);
    l3 = Math.min(r3.range_union_max, l1);

    // If it satisfies a triangle then return that
    if (l2 + l3 > l1) {
        buildTriangle(l1, l2, l3);
    }

    // Impossible to be a triangle
}
