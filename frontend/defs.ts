
// Type defining a plant's scientific and common name, and its database identifier
export interface PlantHandle {
    uid: number // Unique ID
    id: number // Greenworld database ID
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
    p1: number // Plant unique ID
    p2: number // Plant unique ID
    dist: number // Cartesian distance
}

// A network of plants that can exist within a certain distance of each other
export interface Guild {
    excluded: PlantHandle[]
    plants: Array<PlantHandle & Point & { r: number }>
    bounds: Bounds
    edges: Edge[]
}
