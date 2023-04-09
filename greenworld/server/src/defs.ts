
// Type defining a plant's scientific and common name, and its database identifier
export interface PlantHandle {
    id: number
    species: string
    name: string
}

// A cartesian point (x, y)
export interface Point {
    x: number
    y: number
}

export interface Bounds {
    upperLeft: Point
    lowerRight: Point
}

// Represents an edge of a graph connecting two plants between a certain distance
export interface Edge {
    p1: number
    p2: number
    dist: number
}

// A network of plants that can exist within a certain distance of each other
export interface Guild {
    plants: Array<PlantHandle & Point & { r: number }>
    bounds: Bounds
    edges: Edge[]
}
