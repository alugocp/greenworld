import type { Point } from './defs';

export default class UiWrapper {
    // Wrapper for the window's fetch function
    async fetch(url: string): Promise<any> {}

    // Refresh list of plants in the guild placement app
    refreshPlantList(): void {}

    // Renders a guild based on a list of points
    drawGuildPlacement(points: Point[]): void {}
}