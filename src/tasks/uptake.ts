/**
 * This file is the script that prints standardized nutrient uptake data
 */
import * as conversions from '../lib/conversions';
import * as fs from 'fs';

const data: object = JSON.parse(fs.readFileSync('database.json').toString());

for (const plant of data['plants']) {
  console.log(`${plant.name} (${plant.species})`);
  const table = {...data['conversions'], ...(plant.conversions || {})};
  for (const nutrient of plant.uptake) {
    const ratio = conversions.convertUptakeUnits(nutrient.rate, table);
    console.log(`${nutrient.nutrient}: ${nutrient.rate} (${ratio} units/biomass)`);
  }
  console.log('');
}
