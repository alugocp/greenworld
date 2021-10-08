/*
  This file is the script that evaluates companionship profiles for
  the plants in the database
*/
import fs = require('fs');
const data = JSON.parse(fs.readFileSync('database.json').toString());
let companions = [];
let identified = [];
const scores = {};
const thresh = 0;

function getKey(a, b) {
  return `${a.species}, ${b.species}`;
}

function getScore(a, b) {
  return scores[getKey(a, b)] || scores[getKey(b, a)];
}

// Do pairwise comparison
for (let a = 0; a < data.plants.length - 1; a++) {
  for (let b = a + 1; b < data.plants.length; b++) {
    let score = data.plants[a].inputs.map(x => data.plants[b].outputs.indexOf(x) > -1 ? 1 : 0).reduce((acc, x) => acc + x, 0);
    score += data.plants[b].inputs.map(x => data.plants[a].outputs.indexOf(x) > -1 ? 1 : 0).reduce((acc, x) => acc + x, 0);
    score -= data.plants[a].inputs.map(x => data.plants[b].inputs.indexOf(x) > -1 ? 1 : 0).reduce((acc, x) => acc + x, 0);
    scores[getKey(data.plants[a], data.plants[b])] = score;
    if (score >= thresh) {
      companions.push([data.plants[a], data.plants[b]]);
    }
    console.log(`${data.plants[a].species}, ${data.plants[b].species}: ${score}`);
  }
}
console.log('');

// Identify compatible groups
identified = [...identified, ...companions];
while (companions.length > 0) {
  const groups = [...companions];
  companions = [];
  for (const group of groups) {
    for (const plant of data.plants) {
      if (group.map(x => x.species).indexOf(plant.species) > -1) {
        continue;
      }
      let accept = true;
      for (const plant1 of group) {
        if (getScore(plant1, plant) < thresh) {
          accept = false;
          break;
        }
      }
      if (accept) {
        companions.push([...group, plant]);
      }
    }
  }
  identified = [...identified, ...companions];
}

// Log output
console.log(`${identified.length} group(s):`);
identified.map(x => x.map(y => y.species).join(', ')).sort().map(x => console.log(x));
