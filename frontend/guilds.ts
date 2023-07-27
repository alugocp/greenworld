import { Plant } from './defs';

interface Edge {
    p1: number; // Plant 1 ID
    p2: number; // Plant 2 ID
}

export default class GuildFinder {
    constructor(private baseUrl: string) {}

    async discover(id: number, thresh: number): Promise<any[]> {
        const threshFixed: string = thresh.toFixed(3);

        // Grab neighbor IDs
        const neighbors: any[] = await fetch(`${this.baseUrl}neighbors/${id}/${threshFixed}`)
            .then((res) => res.json());

        // Retrieve a graph of plants within the threshold
        const graph: Edge[] = await fetch(`${this.baseUrl}neighborhood/${threshFixed}?ids=${id},${neighbors.join(',')}`)
            .then((res) => res.json());

        // Discover clusters within the graph
        console.log(neighbors);
        console.log(graph);
        return graph;
    }
}