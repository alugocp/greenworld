
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
