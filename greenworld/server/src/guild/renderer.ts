import type { Point, Guild } from '../defs';
const BUFFER_X = 100;
const BUFFER_Y = 50;
const VIEW_X = 1000;
const VIEW_Y = 500;

// Resets what's visible on the canvas
export function resetRender(canvas: HTMLCanvasElement, plantList: HTMLDivElement): void {
    const ctx = canvas.getContext('2d');
    if (ctx === null) {
        return;
    }
    canvas.width = VIEW_X + (BUFFER_X * 2);
    canvas.height = VIEW_Y + (BUFFER_Y * 2);
    ctx.font = '20px sans-serif';
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    plantList.innerHTML = '';
}

// Draws guild representation to the canvas
export function drawGuild(canvas: HTMLCanvasElement, guild: Guild): void {
    const ctx = canvas.getContext('2d');
    if (ctx === null) {
        return;
    }

    // Calculate labels
    const labels: Array<Point & { text: string }> = [];
    const dx = -guild.bounds.upperLeft.x;
    const dy = -guild.bounds.upperLeft.y;
    const scale = Math.min(
        VIEW_X / (guild.bounds.lowerRight.x - guild.bounds.upperLeft.x),
        VIEW_Y / (guild.bounds.lowerRight.y - guild.bounds.upperLeft.y)
    );

    // Draw lines
    for (let x = Math.floor(guild.bounds.upperLeft.x); x < Math.ceil(guild.bounds.lowerRight.x); x++) {
        ctx.fillStyle = x === 0 ? '#000000' : '#cccccc';
        const pos = (x + dx) * scale + BUFFER_X;
        if (pos < BUFFER_X || pos > VIEW_X + BUFFER_X) {
            continue;
        }
        const h = Math.min((Math.ceil(guild.bounds.lowerRight.y) + dy) * scale, VIEW_Y);
        ctx.fillRect(pos, BUFFER_Y, 1, h);
    }
    for (let y = Math.floor(guild.bounds.upperLeft.y); y < Math.ceil(guild.bounds.lowerRight.y); y++) {
        ctx.fillStyle = y === 0 ? '#000000' : '#cccccc';
        const pos = (y + dy) * scale + BUFFER_Y;
        if (pos < BUFFER_Y || pos > VIEW_Y + BUFFER_Y) {
            continue;
        }
        const w = Math.min((Math.ceil(guild.bounds.lowerRight.x) + dx) * scale, VIEW_X);
        ctx.fillRect(BUFFER_X, pos, w, 1);
    }

    // Draw plants
    ctx.fillStyle = '#00ff00';
    for (const p of guild.plants) {
        const x = (p.x + dx) * scale + BUFFER_X;
        const y = (p.y + dy) * scale + BUFFER_Y;
        ctx.beginPath();
        ctx.arc(x, y, 10, 0, Math.PI * 2);
        ctx.fill();
        labels.push({ text: `${p.uid}`, x, y: y + 5 });
    }

    // Draw labels
    ctx.fillStyle = '#000000';
    for (const l of labels) {
        const metrics = ctx.measureText(l.text);
        ctx.fillText(l.text, l.x - metrics.width / 2, l.y);
    }
}

export function listPlants(plantList: HTMLDivElement, guild: Guild): void {
    const items: Array<[number, string]> = [];
    for (const p of guild.plants) {
        const x = Math.round(p.x * 100) / 100;
        const y = Math.round(p.y * 100) / 100;
        items.push([p.uid, `<p>${p.uid}) ${p.name} (${p.species}) at (${x}m, ${y}m)</p>`]);
    }
    for (const p of guild.excluded) {
        items.push([p.uid, `<p>${p.uid}) <s>${p.name} (${p.species})</s></p>`]);
    }
    plantList.innerHTML += items
        .sort((x: [number, string], y: [number, string]) => x[0] - y[0])
        .map((x: [number, string]): string => x[1])
        .join('');
}
