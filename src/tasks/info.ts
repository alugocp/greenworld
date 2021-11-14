/**
 * This file is the script that prints standardized nutrient uptake data
 */
import * as conversions from '../lib/conversions';
import * as fs from 'fs';

const data: object = JSON.parse(fs.readFileSync('database.json').toString());

for (const plant of data['plants']) {
  process.stdout.write(`\x1b[1;32m\x1b[4;32m${plant.name}\x1b[0m - ${plant.species}\n`);
  if (plant.pH && plant.pH.length) {
    process.stdout.write(`\x1b[1;37mpH:\x1b[0m ${plant.pH[0]} - ${plant.pH[1]}\n`);
  }
  if (plant.uptake && plant.uptake.length) {
    process.stdout.write('\x1b[4;37mNutrient uptake\x1b[0m\n');
    const table = {...data['conversions'], ...(plant.conversions || {})};
    for (const nutrient of plant.uptake) {
      const ratio = conversions.convertUptakeUnits(nutrient.rate, table);
      process.stdout.write(`\x1b[1;37m${nutrient.nutrient}:\x1b[0m ${nutrient.rate} (${ratio})\n`);
    }
  }
  console.log('');
}
