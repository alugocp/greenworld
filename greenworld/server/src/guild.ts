import type { PlantHandle, Report, Point, Guild } from './defs';

// Grab report between two plant species
function getReport(reports: Report[], plant1: PlantHandle, plant2: PlantHandle): Report {
    const lower: number = Math.min(plant1.id, plant2.id);
    const upper: number = Math.max(plant1.id, plant2.id);
    return reports.filter((x: Report): boolean => x.plant1 === lower && x.plant2 === upper)[0];
}

// Grabs a plant handle from a list of plant handles given the ID
function getPlantHandle<T extends PlantHandle>(plants: T[], id: number): T {
    return plants.filter((x: T): boolean => x.id === id)[0];
}

// Returns the plant ID in common amongst two reports
function commonPlant(r1: Report, r2: Report): number {
    return r1.plant1 === r2.plant1 || r1.plant1 === r2.plant2 ? r1.plant1 : r1.plant2;
}

// Initializes the guild finder module
export async function init(canvas: HTMLCanvasElement): Promise<void> {
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
    const guild: Guild | null = findTriangle(
        plants,
        getReport(reports, plants[0], plants[1]),
        getReport(reports, plants[1], plants[2]),
        getReport(reports, plants[0], plants[2])
    );
    console.log(guild);

    // Draw to canvas
    draw(canvas, guild);
}

// Draws guild representation to the canvas
function draw(canvas: HTMLCanvasElement, guild: Guild | null): void {
    const ctx = canvas.getContext('2d');
    if (ctx === null) {
        return;
    }
    canvas.width = 1000;
    canvas.height = 500;
    ctx.fillStyle = '#00ff00';
    ctx.strokeStyle = '#000000';
    ctx.font = '20px sans-serif';
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    if (guild === null) {
        return;
    }
    const labels: Array<Point & { text: string }> = [];
    const dx = -guild.bounds.upperLeft.x;
    const dy = -guild.bounds.upperLeft.y;
    const scale = Math.min(
        canvas.width / (guild.bounds.lowerRight.x - guild.bounds.upperLeft.x),
        canvas.height / (guild.bounds.lowerRight.y - guild.bounds.upperLeft.y)
    );
    ctx.lineWidth = scale / 320;
    for (const e of guild.edges) {
        const p1 = getPlantHandle(guild.plants, e.p1);
        const p2 = getPlantHandle(guild.plants, e.p2);
        ctx.beginPath();
        ctx.moveTo((p1.x + dx) * scale, (p1.y + dy) * scale);
        ctx.lineTo((p2.x + dx) * scale, (p2.y + dy) * scale);
        ctx.stroke();
        labels.push({
            text: `${e.dist}m`,
            x: (p1.x + dx + p2.x + dx) * scale / 2,
            y: (p1.y + dy + p2.y + dy) * scale / 2
        });
    }
    for (const p of guild.plants) {
        ctx.beginPath();
        ctx.arc((p.x + dx) * scale, (p.y + dy) * scale, p.r * scale, 0, Math.PI * 2);
        ctx.fill();
        ctx.stroke();
        labels.push({
            text: p.name,
            x: (p.x + dx) * scale,
            y: (p.y + dy) * scale
        });
    }
    ctx.fillStyle = '#000000';
    for (const l of labels) {
        ctx.fillText(l.text, l.x, l.y);
    }
}

// Pythagorean distance formula
function distance(x: number, y: number): number {
    return Math.round(Math.sqrt(Math.pow(x, 2) + Math.pow(y, 2)) * 1000) / 1000;
}

// Builds a triangle guild from the three plants and side lengths
function buildTriangle(p1: PlantHandle, p2: PlantHandle, p3: PlantHandle, _a: number, _b: number, _c: number): Guild {
    const buffer = 0.025;
    const theta = Math.acos((Math.pow(_a, 2) + Math.pow(_c, 2) - Math.pow(_b, 2)) / (2 * _a * _c));
    const x = Math.round(Math.cos(theta) * _c * 1000) / 1000;
    const y = Math.round(Math.sin(theta) * _c * 1000) / 1000;
    console.log(`(0, 0) -> ${_a} = ${distance(_a, 0)} -> (${_a}, 0) -> ${_b} = ${distance(x - _a, y)} -> (${x}, ${y}) -> ${_c} = ${distance(x, y)}`);
    return {
        plants: [
            { ...p1, x: 0, y: 0, r: buffer },
            { ...p2, x: _a, y: 0, r: buffer },
            { ...p3, x, y, r: buffer }
        ],
        edges: [
            { p1: p1.id, p2: p2.id, dist: _a },
            { p1: p2.id, p2: p3.id, dist: _b },
            { p1: p3.id, p2: p1.id, dist: _c }
        ],
        bounds: {
            upperLeft: { x: -buffer * 2, y: -buffer * 2 },
            lowerRight: { x: _a + buffer * 2, y: y + buffer * 2 }
        }
    };
}

// Returns a guild if the 3 provided reports can be made into a triangle
function findTriangle(plants: PlantHandle[], p12: Report, p23: Report, p13: Report): Guild | null {
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

    // If it's already a triangle then return that
    if (l2 + l3 > l1) {
        return buildTriangle(
            getPlantHandle(plants, commonPlant(r3, r1)),
            getPlantHandle(plants, commonPlant(r1, r2)),
            getPlantHandle(plants, commonPlant(r2, r3)),
            l1,
            l2,
            l3
        );
    }

    // Change shorter sides to try and make a triangle
    l2 = Math.min(r2.range_union_max, l1);
    l3 = Math.min(r3.range_union_max, l1);

    // If it satisfies a triangle then return that
    if (l2 + l3 > l1) {
        return buildTriangle(
            getPlantHandle(plants, commonPlant(r3, r1)),
            getPlantHandle(plants, commonPlant(r1, r2)),
            getPlantHandle(plants, commonPlant(r2, r3)),
            l1,
            l2,
            l3
        );
    }

    // Impossible to be a triangle
    return null;
}
