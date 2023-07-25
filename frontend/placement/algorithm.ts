import type { PlantHandle, Guild, Bounds } from '../defs';

// Unions two Bounds objects
export function collapseBounds(b1: Bounds, b2: Bounds): Bounds {
    return {
        upperLeft: {
            x: Math.min(b1.upperLeft.x, b2.upperLeft.x),
            y: Math.min(b1.upperLeft.y, b2.upperLeft.y)
        },
        lowerRight: {
            x: Math.max(b1.lowerRight.x, b2.lowerRight.x),
            y: Math.max(b1.lowerRight.y, b2.lowerRight.y)
        }
    };
}

// Report object from the server
export class Report {
    plant1: number;
    plant2: number;
    range_union_min: number;
    range_union_max: number;
    report: any[];
    uids?: [number, number];

    constructor(plant1: number, plant2: number, rangeUnionMin: number, rangeUnionMax: number, report: any[]) {
        this.plant1 = plant1;
        this.plant2 = plant2;
        this.range_union_min = rangeUnionMin;
        this.range_union_max = rangeUnionMax;
        this.report = report;
    }

    // Returns the ID of the common plant between two reports
    commonPlant(other: Report): number {
        if (this.uids === undefined || other.uids === undefined) {
            throw new Error('UIDs are not set');
        }
        return this.uids[0] === other.uids[0] || this.uids[0] === other.uids[1] ? this.uids[0] : this.uids[1];
    }

    clone(): Report {
        return new Report(
            this.plant1,
            this.plant2,
            this.range_union_min,
            this.range_union_max,
            this.report
        );
    }

    setUids(p1: PlantHandle, p2: PlantHandle): Report {
        if (p1.id === this.plant1) {
            this.uids = [p1.uid, p2.uid];
        } else {
            this.uids = [p2.uid, p1.uid];
        }
        return this;
    }
}

// Handles logic surrounding a collection of Report obejcts
export class Reports {
    private reports: Record<string, Record<string, Report>> = {};

    // Orders the two plant IDs
    private orderedIds(p1: number, p2: number): [string, string] {
        return [
            `${Math.min(p1, p2)}`,
            `${Math.max(p1, p2)}`
        ];
    }

    // Return the report between two specified plants
    getReport(p1: PlantHandle, p2: PlantHandle): Report {
        const ids = this.orderedIds(p1.id, p2.id);
        return this.reports[ids[0]][ids[1]];
    }

    // Request a list of relevant reports from the server
    async populate(baseUrl: string, plants: PlantHandle[]): Promise<void> {
        const speciesList: string = [...new Set(plants.map((x: PlantHandle): number => x.id))].join(',');
        const results: Report[] = await fetch(`${baseUrl}reports?species_list=${speciesList}`)
            .then((res) => res.json())
            .then((reports: any[]) => reports.map((r: any) => new Report(
                r.plant1,
                r.plant2,
                parseFloat(`${r.range_union_min as number}`),
                parseFloat(`${r.range_union_max as number}`),
                r.report
            )));
        for (const report of results) {
            const ids = this.orderedIds(report.plant1, report.plant2);
            if (this.reports[ids[0]] === undefined) {
                this.reports[ids[0]] = {};
            }
            this.reports[ids[0]][ids[1]] = report;
        }
    }
}

// Implement algorithms for the guild placement
export type GuildAlgorithm = (plants: PlantHandle[], reports: Reports) => Guild | null;