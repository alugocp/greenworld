import type { PlantHandle, Point, Guild, Edge } from '../defs';
import type { Report, Reports } from './algorithm';
import { collapseBounds } from './algorithm';

// Grabs a plant handle from a list of plant handles given the unique ID
function getPlantHandle<T extends PlantHandle>(plants: T[], uid: number): T {
    return plants.filter((x: T): boolean => x.uid === uid)[0];
}

// Rounds the number n to a given place
function round(n: number, place: number): number {
    const coeff = Math.pow(10, place);
    return Math.round(n * coeff) / coeff;
}

// Pythagorean distance formula
function distance(x: number, y: number, place: number | null = null): number {
    const dist: number = Math.sqrt(Math.pow(x, 2) + Math.pow(y, 2));
    return place === null ? dist : round(dist, place);
}

// Rotates point p about origin by theta
function rotateAbout(p: Point, origin: Point, dtheta: number): Point {
    const theta = Math.atan2(p.y - origin.y, p.x - origin.x) + dtheta;
    const dist = distance(p.x - origin.x, p.y - origin.y);
    return {
        x: Math.round((origin.x + Math.cos(theta) * dist) * 1000) / 1000,
        y: Math.round((origin.y + Math.sin(theta) * dist) * 1000) / 1000
    };
}

// Reflects point P about the line A -> B
function reflectAbout(p: Point, l1: Point, l2: Point): Point {
    if (l1.y === l2.y) {
        return {
            x: p.x,
            y: 2 * l1.y - p.y
        };
    }
    if (l1.x === l2.x) {
        return {
            x: 2 * l1.x - p.x,
            y: p.y
        };
    }
    const m = (l2.y - l1.y) / (l2.x - l1.x);
    const b = l1.y - l1.x * m;
    const m1 = -1 / m;
    const b1 = p.y - p.x * m1;
    const lx = (b1 - b) / (m - m1);
    const ly = b + lx * m;
    return {
        x: 2 * lx - p.x,
        y: 2 * ly - p.y
    };
}

// Grabs a common edge between two guilds
function grabCommonEdge(g1: Guild, g2: Guild): Edge | null {
    for (const e1 of g1.edges) {
        for (const e2 of g2.edges) {
            if (((e1.p1 === e2.p1 && e1.p2 === e2.p2) || (e1.p1 === e2.p2 && e1.p2 === e2.p1)) && e1.dist === e2.dist) {
                return e1;
            }
        }
    }
    return null;
}

// Builds a triangle guild from the three plants and side lengths
function buildTriangle(p1: PlantHandle, p2: PlantHandle, p3: PlantHandle, _a: number, _b: number, _c: number): Guild {
    const buffer = 0.025;
    const theta = Math.acos((Math.pow(_a, 2) + Math.pow(_c, 2) - Math.pow(_b, 2)) / (2 * _a * _c));
    const x = Math.round(Math.cos(theta) * _c * 1000) / 1000;
    const y = Math.round(Math.sin(theta) * _c * 1000) / 1000;
    return {
        plants: [
            { ...p1, x: 0, y: 0, r: buffer },
            { ...p2, x: _a, y: 0, r: buffer },
            { ...p3, x, y, r: buffer }
        ],
        edges: [
            { p1: p1.uid, p2: p2.uid, dist: _a },
            { p1: p2.uid, p2: p3.uid, dist: _b },
            { p1: p3.uid, p2: p1.uid, dist: _c }
        ],
        bounds: {
            upperLeft: { x: -buffer * 2, y: -buffer * 2 },
            lowerRight: { x: _a + buffer * 2, y: y + buffer * 2 }
        }
    };
}

// Returns a guild if the 3 provided reports can be made into a triangle
function findTriangle(plants: PlantHandle[], reports: Reports, p1: PlantHandle, p2: PlantHandle, p3: PlantHandle): Guild | null {
    const p12 = reports.getReport(p1, p2).clone().setUids(p1, p2);
    const p23 = reports.getReport(p2, p3).clone().setUids(p2, p3);
    const p13 = reports.getReport(p1, p3).clone().setUids(p1, p3);
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
    const l1: number = r1.range_union_min !== 0 ? r1.range_union_min : Math.min(0.16, r1.range_union_max);
    let l2: number = r2.range_union_min !== 0 ? r2.range_union_min : Math.min(0.16, r2.range_union_max);
    let l3: number = r3.range_union_min !== 0 ? r3.range_union_min : Math.min(0.16, r3.range_union_max);

    // If it's already a triangle then return that
    if (l2 + l3 > l1) {
        return buildTriangle(
            getPlantHandle(plants, r3.commonPlant(r1)),
            getPlantHandle(plants, r1.commonPlant(r2)),
            getPlantHandle(plants, r2.commonPlant(r3)),
            l1,
            l2,
            l3
        );
    }

    // Change a shorter side to try and make a triangle
    l2 = Math.min(r2.range_union_max, l1 - l3 + 0.033);
    if (l2 + l3 > l1) {
        return buildTriangle(
            getPlantHandle(plants, r3.commonPlant(r1)),
            getPlantHandle(plants, r1.commonPlant(r2)),
            getPlantHandle(plants, r2.commonPlant(r3)),
            l1,
            l2,
            l3
        );
    }

    // Change a shorter side to try and make a triangle
    l3 = Math.min(r3.range_union_max, l1 - l2 + 0.033);
    if (l2 + l3 > l1) {
        return buildTriangle(
            getPlantHandle(plants, r3.commonPlant(r1)),
            getPlantHandle(plants, r1.commonPlant(r2)),
            getPlantHandle(plants, r2.commonPlant(r3)),
            l1,
            l2,
            l3
        );
    }

    // Impossible to be a triangle
    return null;
}

function checkOtherPlants(reports: Reports, guild: Guild, result: Point, plantA: PlantHandle, plantB: PlantHandle, plantC: PlantHandle): Edge[] | null {
    const edgesToAdd: Edge[] = [];
    for (const p of guild.plants) {
        if (p === plantA || p === plantB) {
            continue;
        }
        const d = distance(result.x - p.x, result.y - p.y);
        if (d < reports.getReport(p, plantC).range_union_min) {
            return null;
        }
        edgesToAdd.push({ p1: plantC.uid, p2: p.uid, dist: d });
    }
    return edgesToAdd;
}

// subalgorithm for n > 2 guild
export function triangulationAlgorithm(plants: PlantHandle[], reports: Reports): Guild | null {
    const guild: Guild | null = findTriangle(
        plants,
        reports,
        plants[0],
        plants[1],
        plants[2]
    );
    if (guild === null) {
        return null;
    }
    for (let a = 3; a < plants.length; a++) {
        const plantC = plants[a];
        for (const e of guild.edges) {
            const plantA: PlantHandle = getPlantHandle(plants, e.p1);
            const plantB: PlantHandle = getPlantHandle(plants, e.p2);
            const newGuild: Guild | null = findTriangle(
                plants,
                reports,
                plantA,
                plantB,
                plantC
            );
            if (newGuild === null) {
                continue;
            }
            if (grabCommonEdge(guild, newGuild) === null) {
                continue;
            }

            // Rotate onto cumulative guild structure
            const plantPoint = getPlantHandle(newGuild.plants, plantC.uid);
            const ax = getPlantHandle(guild.plants, plantA.uid).x;
            const ay = getPlantHandle(guild.plants, plantA.uid).y;
            const dx = ax - getPlantHandle(newGuild.plants, plantA.uid).x;
            const dy = ay - getPlantHandle(newGuild.plants, plantA.uid).y;
            const b1x = getPlantHandle(guild.plants, plantB.uid).x;
            const b1y = getPlantHandle(guild.plants, plantB.uid).y;
            const b2x = getPlantHandle(newGuild.plants, plantB.uid).x + dx;
            const b2y = getPlantHandle(newGuild.plants, plantB.uid).y + dy;
            const theta = Math.atan2(b1y - ay, b1x - ax) - Math.atan2(b2y - ay, b2x - ax);
            let result: Point = rotateAbout(
                { x: plantPoint.x + dx, y: plantPoint.y + dy },
                getPlantHandle(guild.plants, plantA.uid),
                theta
            );

            // If new plant is too close then check its reflection
            let edgesToAdd = checkOtherPlants(reports, guild, result, plantA, plantB, plantC);
            if (edgesToAdd === null) {
                result = reflectAbout(result, { x: ax, y: ay }, { x: b1x, y: b1y });
                edgesToAdd = checkOtherPlants(reports, guild, result, plantA, plantB, plantC);
                if (edgesToAdd === null) {
                    continue;
                }
            }

            // Update the guild
            guild.plants.push({ ...plantC, ...result, r: 0.025 });
            guild.edges = guild.edges.concat(newGuild.edges.filter((e: Edge) => e.p1 === plantC.uid || e.p2 === plantC.uid)).concat(edgesToAdd);
            guild.bounds = collapseBounds(guild.bounds, {
                upperLeft: {
                    x: result.x - 0.05,
                    y: result.y - 0.05
                },
                lowerRight: {
                    x: result.x + 0.05,
                    y: result.y + 0.05
                }
            });
            break;
        }
    }
    return guild;
}

// Geometry-based algorithm to plan a guild
export function geometricAlgorithm(plants: PlantHandle[], reports: Reports): Guild | null {
    if (plants.length === 0) {
        return null;
    }
    if (plants.length === 1) {
        return {
            plants: [
                {
                    ...plants[0],
                    x: 0,
                    y: 0,
                    r: 0.025
                }
            ],
            bounds: {
                upperLeft: {
                    x: -0.05,
                    y: -0.05
                },
                lowerRight: {
                    x: 0.05,
                    y: 0.05
                }
            },
            edges: []
        };
    }
    if (plants.length === 2) {
        const report: Report = reports.getReport(plants[0], plants[1]);
        const dist = report.range_union_min !== 0 ? report.range_union_min : 0.16;
        return {
            plants: [
                {
                    ...plants[0],
                    x: 0,
                    y: 0,
                    r: 0.025
                },
                {
                    ...plants[1],
                    x: dist,
                    y: 0,
                    r: 0.025
                }
            ],
            bounds: {
                upperLeft: {
                    x: -0.05,
                    y: -0.05
                },
                lowerRight: {
                    x: dist + 0.05,
                    y: 0.05
                }
            },
            edges: [{
                p1: plants[0].uid,
                p2: plants[1].uid,
                dist
            }]
        };
    }
    return triangulationAlgorithm(plants, reports);
}
