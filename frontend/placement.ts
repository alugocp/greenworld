import type { PlantHandle, Point } from './defs';
import type UiWrapper from './wrapper';
const DT = 0.05;

type ReportsTable = Record<number, Record<number, [number, number]>>;
type Node = Point & {
    vx: number
    vy: number
};

export default class GuildPlacement {
    private readonly simulation: Simulation = new Simulation();
    readonly plants: PlantHandle[] = [
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
        this.plants.push({ id, name, species });
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
        this.simulation.initialize(reports, this.plants.map((x: PlantHandle): number => x.id));
        while (this.simulation.shouldContinue()) {
            this.simulation.frame();
        }
        this.wrapper.drawGuildPlacement(this.simulation.points);
    }

    // Generate a reports table for the user-selected plant species
    private async pullReports(): Promise<ReportsTable> {
        const table: ReportsTable = {};
        const speciesList: string = [...new Set(this.plants.map((x: PlantHandle): number => x.id))].join(',');
        await fetch(`${this.baseUrl}reports?species_list=${speciesList}`)
            .then((res) => res.json())
            .then((reports: any[]): null[] => reports.map((r: any): null => {
                table[r.plant1] = (table[r.plant1] === undefined) ? [] : table[r.plant1];
                table[r.plant2] = (table[r.plant2] === undefined) ? [] : table[r.plant2];
                table[r.plant1][r.plant2] = [r.range_union_min, r.range_union_max];
                table[r.plant2][r.plant1] = [r.range_union_min, r.range_union_max];
                return null;
            }));
        return table;
    }
}

class Simulation {
    private previousEnergy: number;
    private reports: ReportsTable;
    private ids: number[];
    frameNumber: number;
    nodes: Node[];

    get points(): Point[] {
        return this.nodes.map((n: Node): Point => ({ x: n.x, y: n.y }));
    }

    initialize(reports: ReportsTable, ids: number[]): void {
        this.reports = reports;
        this.frameNumber = 0;
        this.nodes = [];
        this.ids = ids;
        if (this.ids.length > 0) {
            this.nodes.push({ x: -1, y: -1, vx: 0, vy: 0 });
        }
        if (this.ids.length > 1) {
            this.nodes.push({ x: 1, y: 1, vx: 0, vy: 0 });
        }
    }

    frame(): void {
        this.frameNumber++;
        if (this.nodes.length < this.ids.length && this.frameNumber % (5 / DT) === 0) {
            this.nodes.push({ x: 0, y: 0, vx: 0, vy: 0 });
        }

        // Inter-nodal spring forces
        for (let a = 0; a < this.nodes.length - 1; a++) {
            for (let b = a + 1; b < this.nodes.length; b++) {
                const accel: number = this.diffFromRange(this.nodes[a], this.nodes[b], this.ids[a], this.ids[b]) / 10;
                const angle: number = Math.atan2(this.nodes[b].y - this.nodes[a].y, this.nodes[b].x - this.nodes[a].x);
                const dvx: number = Math.cos(angle) * accel * DT;
                const dvy: number = Math.sin(angle) * accel * DT;
                this.nodes[b].vx += dvx;
                this.nodes[b].vy += dvy;
                this.nodes[a].vx -= dvx;
                this.nodes[a].vy -= dvy;
            }
        }

        // Friction forces and move by velocity
        for (let a = 0; a < this.nodes.length; a++) {
            const angle: number = Math.atan2(this.nodes[a].vy, this.nodes[a].vx);
            const dvx: number = Math.cos(angle) * 0.1 * DT;
            const dvy: number = Math.sin(angle) * 0.1 * DT;
            if (Math.abs(this.nodes[a].vx) - Math.abs(dvx) > 0) {
                this.nodes[a].vx -= dvx;
            } else {
                this.nodes[a].vx = 0;
            }
            if (Math.abs(this.nodes[a].vy) - Math.abs(dvy) > 0) {
                this.nodes[a].vy -= dvy;
            } else {
                this.nodes[a].vy = 0;
            }
            this.nodes[a].x += this.nodes[a].vx * DT;
            this.nodes[a].y += this.nodes[a].vy * DT;
        }
    }

    shouldContinue(): boolean {
        if (this.nodes.length < this.ids.length) {
            return true;
        }
        const energy = this.totalEnergy();
        if (energy === this.previousEnergy) {
            return false;
        }
        this.previousEnergy = energy;
        return this.frameNumber < 500 / DT;
    }

    private totalEnergy(): number {
        let energy: number = 0;
        for (let a = 0; a < this.nodes.length - 1; a++) {
            for (let b = a + 1; b < this.nodes.length; b++) {
                const diff: number = this.diffFromRange(this.nodes[a], this.nodes[b], this.ids[a], this.ids[b]);
                energy += Math.pow(diff, 2) / 20;
            }
        }
        return energy;
    }

    private diffFromRange(n1: Node, n2: Node, id1: number, id2: number): number {
        const dist = Math.sqrt(Math.pow(n1.x - n2.x, 2) + Math.pow(n1.y - n2.y, 2));
        const range: [number, number] = this.reports[id1][id2];
        if (dist < range[0]) {
            return range[0] - dist;
        }
        if (dist > range[1]) {
            return range[1] - dist;
        }
        return 0;
    }
}
