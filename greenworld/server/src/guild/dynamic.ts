import type { Guild, PlantHandle, Point, Bounds } from '../defs';
import type { Reports, Report } from './algorithm';
import { collapseBounds } from './algorithm';

const ranges: Record<number, Record<number, [number, number]>> = {};
const positions: Record<number, Point> = {};
const velocities: Record<number, Point> = {};

// Get the distance between two points
function distance(p1: Point, p2: Point): number {
    return Math.sqrt(Math.pow(p1.x - p2.x, 2) + Math.pow(p1.y - p2.y, 2));
}

// Returns the angle from p1 to p2
function angle(p1: Point, p2: Point): number {
    return Math.atan2(p2.y - p1.y, p2.x - p1.x);
}

function step(plants: PlantHandle[]): number {
    let total = 0;
    for (let a = 0; a < plants.length; a++) {
        for (let b = a + 1; b < plants.length; b++) {
            const u1 = plants[a].uid;
            const u2 = plants[b].uid;
            const d = distance(positions[u1], positions[u2]);
            let magnitude = 0;
            if (d < ranges[u1][u2][0]) {
                magnitude = 0.01;
            }
            if (d > ranges[u1][u2][1]) {
                magnitude = -0.01;
            }
            if (magnitude !== 0) {
                const alpha = angle(positions[u1], positions[u2]);
                velocities[u1].x -= Math.cos(alpha) * magnitude;
                velocities[u1].y -= Math.sin(alpha) * magnitude;
                velocities[u2].x += Math.cos(alpha) * magnitude;
                velocities[u2].y += Math.sin(alpha) * magnitude;
                total += Math.abs(magnitude);
            }
        }
    }
    const friction = 0.01;
    for (let a = 0; a < plants.length; a++) {
        const uid = plants[a].uid;
        positions[uid].x += velocities[uid].x;
        positions[uid].y += velocities[uid].y;
        if (Math.abs(velocities[uid].x) < friction) {
            velocities[uid].x = 0;
        } else {
            velocities[uid].x -= friction * velocities[uid].x / Math.abs(velocities[uid].x);
        }
        if (Math.abs(velocities[uid].y) < friction) {
            velocities[uid].y = 0;
        } else {
            velocities[uid].y -= friction * velocities[uid].y / Math.abs(velocities[uid].y);
        }
    }
    return total;
}

export function dynamicAlgorithm(plants: PlantHandle[], reports: Reports): Guild | null {
    for (let a = 0; a < plants.length; a++) {
        const angle = a * Math.PI * 2 / plants.length;
        positions[plants[a].uid] = { x: Math.cos(angle), y: Math.sin(angle) };
        velocities[plants[a].uid] = { x: 0, y: 0 };
        for (let b = a + 1; b < plants.length; b++) {
            const r: Report = reports.getReport(plants[a], plants[b]);
            ranges[plants[a].uid] = ranges[plants[a].uid] !== undefined ? ranges[plants[a].uid] : {};
            ranges[plants[b].uid] = ranges[plants[b].uid] !== undefined ? ranges[plants[b].uid] : {};
            ranges[plants[a].uid][plants[b].uid] = [r.range_union_min, r.range_union_max];
            ranges[plants[b].uid][plants[a].uid] = [r.range_union_min, r.range_union_max];
        }
    }
    for (let a = 0; a < 100; a++) {
        step(plants);
    }
    for (let a = 0; a < plants.length; a++) {
        for (let b = a + 1; b < plants.length; b++) {
            const report = reports.getReport(plants[a], plants[b]);
            const yes = report.range_union_min <= distance(positions[plants[a].uid], positions[plants[b].uid]) && distance(positions[plants[a].uid], positions[plants[b].uid]) <= report.range_union_max;
            console.log(`${plants[a].uid}, ${plants[b].uid}: ${report.range_union_min} <= ${distance(positions[plants[a].uid], positions[plants[b].uid])} <= ${report.range_union_max} (${yes ? 'YEP' : 'NOPE'})`);
        }
    }

    let bounds: Bounds = {
        upperLeft: { x: -2, y: -2 },
        lowerRight: { x: 2, y: 2 }
    };
    for (const plant of plants) {
        bounds = collapseBounds(bounds, {
            upperLeft: {
                x: positions[plant.uid].x - 0.05,
                y: positions[plant.uid].y - 0.05
            },
            lowerRight: {
                x: positions[plant.uid].x + 0.05,
                y: positions[plant.uid].y + 0.05
            }
        });
    }

    return {
        plants: plants.map((x) => ({ ...x, ...positions[x.uid], r: 1 })),
        excluded: [],
        edges: [],
        bounds
    };
}
