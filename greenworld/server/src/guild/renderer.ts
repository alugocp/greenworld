import type { Point, Guild } from '../defs';

// Draws guild representation to the canvas
export function draw(canvas: HTMLCanvasElement, guild: Guild): void {
    const ctx = canvas.getContext('2d');
    if (ctx === null) {
        return;
    }

    // Set up canvas state
    const BUFFER_X = 100;
    const BUFFER_Y = 50;
    const VIEW_X = 1000;
    const VIEW_Y = 500;
    canvas.width = VIEW_X + (BUFFER_X * 2);
    canvas.height = VIEW_Y + (BUFFER_Y * 2);
    ctx.fillStyle = '#00ff00';
    ctx.strokeStyle = '#000000';
    ctx.font = '20px sans-serif';
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw plants and calculate labels
    const labels: Array<Point & { text: string }> = [];
    const dx = -guild.bounds.upperLeft.x;
    const dy = -guild.bounds.upperLeft.y;
    const scale = Math.min(
        VIEW_X / (guild.bounds.lowerRight.x - guild.bounds.upperLeft.x),
        VIEW_Y / (guild.bounds.lowerRight.y - guild.bounds.upperLeft.y)
    );
    for (const p of guild.plants) {
        const x = (p.x + dx) * scale + BUFFER_X;
        const y = (p.y + dy) * scale + BUFFER_Y;
        ctx.beginPath();
        ctx.arc(x, y, p.r * scale, 0, Math.PI * 2);
        ctx.fill();
        ctx.stroke();
        labels.push({ text: p.name, x, y });
    }

    // Draw labels
    ctx.fillStyle = '#000000';
    for (const l of labels) {
        const metrics = ctx.measureText(l.text);
        ctx.fillText(l.text, l.x - metrics.width / 2, l.y);
    }

    // Draw lines
    for (let x = 0; x < VIEW_X; x += scale) {
        ctx.fillRect(BUFFER_X + x, BUFFER_Y, 1, VIEW_Y);
    }
    for (let y = 0; y < VIEW_Y; y += scale) {
        ctx.fillRect(BUFFER_X, BUFFER_Y + y, VIEW_X, 1);
    }
}
