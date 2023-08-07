
// Type defining a plant's scientific and common name, and its database identifier
export interface Plant {
    id: number // Greenworld database ID
    species: string
    name: string
}

// Cartesian point type
export type Point = {
    x: number;
    y: number;
}
