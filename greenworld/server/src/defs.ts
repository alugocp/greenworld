
// Type defining a plant's scientific and common name
export interface PlantHandle {
    id: number
    species: string
    name: string
}

export interface Report {
    plant1: number
    plant2: number
    range_union_min: number
    range_union_max: number
    report: any[]
}

export interface Point {
    x: number
    y: number
}

export interface Edge {
    p1: number
    p2: number
    dist: number
}

export interface Guild {
    plants: Array<PlantHandle & Point & { r: number }>
    bounds: { upperLeft: Point, lowerRight: Point }
    edges: Edge[]
}
