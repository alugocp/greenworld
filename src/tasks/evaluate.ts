/**
 * This file is the script that evaluates companionship profiles for
 * the plants in the database
 */
 import * as conversions from '../lib/conversions';
 import data from '../database';

function overlaps(range1: number[], range2: number[]): boolean {
  return (range1[0] < range2[0]) ? (range1[1] >= range2[0]) : (range2[1] >= range1[0]);
}

function magnitude(input: number): number {
  input = Math.abs(input);
  let result: number = 0;
  while (input < 1) {
    input *= 10;
    result++;
  }
  if (Math.round(input) === 10) {
    result--;
  }
  return result;
}

for (let a = 0; a < data.plants.length - 1; a++) {
  const plant1 = data.plants[a];
  for (let b = a + 1; b < data.plants.length; b++) {
    const plant2 = data.plants[b];
    process.stdout.write(`\x1b[4m${plant1.name} x ${plant2.name}\x1b[0m\n`);
    if (overlaps(plant1.pH as number[], plant2.pH as number[])) {
      process.stdout.write(`• pH ranges overlap\n`);
    } else {
      process.stdout.write(`• pH ranges do not overlap\n`);
    }
    for (const nut1 of plant1.uptake) {
      for (const nut2 of plant2.uptake) {
        if (nut1.nutrient === nut2.nutrient) {
          const ratio1 = conversions.convertUptakeUnits(nut1.rate, plant1.conversions || {});
          const ratio2 = conversions.convertUptakeUnits(nut2.rate, plant2.conversions || {});
          const mag1 = magnitude(ratio1);
          const mag2 = magnitude(ratio2);
          if (mag1 === mag2) {
            process.stdout.write(`• Compete for ${nut1.nutrient}\n`);
          }
        }
      }
    }
    console.log('');
  }
}
