import { Plant } from './defs';

export default class GuildFinder {
    private plantHandlers_: Record<number, Plant>;

    constructor(private baseUrl: string) {}

    // Getter for the relevant plant data object
    get plantHandlers(): Record<number, Plant> {
        return this.plantHandlers_;
    }

    // Sets up relevant plant data for the neighbors list
    private async updatePlantHandlers(ids: number[]): Promise<void> {
        const handlers: Plant[] = await fetch(`${this.baseUrl}handlers?ids=${ids.join(',')}`)
            .then((res) => res.json());
        this.plantHandlers_ = {};
        handlers.map((x: Plant) => {
            this.plantHandlers_[x.id] = x;
        });
    }

    // Guild finder algorithm from a given plant ID and desired threshold
    async discover(id: number, thresh: number): Promise<number[][]> {
        const threshFixed: string = thresh.toFixed(3);

        // Grab neighbor IDs
        const neighbors: number[] = await fetch(`${this.baseUrl}neighbors/${id}/${threshFixed}`)
            .then((res) => res.json());

        // Retrieve a graph of plants within the threshold
        const graph: [number, number][] = await fetch(`${this.baseUrl}neighborhood/${threshFixed}?ids=${neighbors.join(',')},${id}`)
            .then((res) => res.json())
            .then((res) => res.filter((x: [number, number]) => x[0] !== x[1]));

        // For debugging purposes
        if (graph.length > 100) {
            graph.splice(100, graph.length - 100);
        }
        console.log(neighbors);
        console.log(graph);

        // Discover clusters within the graph (maximal subgraphs) and return
        await this.updatePlantHandlers([...neighbors, id]);
        return this.bronKerbosch(id, graph, [id], neighbors.filter((u) => this.neighbors(graph, u, id)), [], []);
    }

    // Returns true if the two nodes share an edge in the graph
    private neighbors(graph: [number, number][], u: number, v: number): boolean {
        return graph.filter((x: [number, number]) => (x[0] === u && x[1] === v) || (x[0] === v && x[1] === u)).length > 0;
    }

    // Bron-Kerbosch algorithm (https://en.wikipedia.org/wiki/Bron%E2%80%93Kerbosch_algorithm)
    private bronKerbosch(id: number, graph: [number, number][], r: number[], p: number[], x: number[], guilds: number[][]): number[][] {
        if (!p.length && !x.length && r.length > 1 && r.indexOf(id) > -1) {
            guilds.push(r);
        }
        while (p.length > 0) {
            const v = p[0];
            this.bronKerbosch(
                id,
                graph,
                [...r, v],
                p.filter((u) => this.neighbors(graph, u, v)),
                x.filter((u) => this.neighbors(graph, u, v)),
                guilds
            );
            p.splice(0, 1);
            x.push(v);
        }
        return guilds;
    }
}