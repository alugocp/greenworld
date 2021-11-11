/**
 * This file implements unit conversion logic
 * Here is where we convert between nutrient uptake data units
 */
const pkg = {};

/**
 * This function converts any uptake rate into standardized units
 * @param {string} rate is the rate of nutrient uptake you want to convert
 * @param {object} conversions is a table of unit conversions
 * @returns {numeric} the standardized ratio of nutrient uptake
 */
pkg.convertUptakeUnits = (rate: string, conversions: object): numeric => {
  const parsed: RegExp = rate.match(/^([0-9]+(?:\.[0-9]+)?) ([A-Za-z]+)\/([A-Za-z]+)$/);
  if (!parsed) {
    throw `Could not parse rate '${rate}'`;
  }
  let ratio: numeric = parseFloat(parsed[1]);
  let unit1: string = parsed[2];
  let unit2: string = parsed[3];
  if (unit1 === 'oz') {
    ratio /= conversions['oz/lb'] as numeric;
    unit1 = 'lb';
  }
  if (unit2 === 'A') {
    ratio /= conversions['bu/A'] as numeric;
    unit2 = 'bu';
  }
  if (unit2 === 'bu') {
    ratio /= conversions['lb/bu'] as numeric;
    unit2 = 'lb';
  }
  if (unit1 !== 'lb' || unit2 !== 'lb') {
    throw `Incomplete conversion for rate '${rate}'`;
  }
  return ratio;
}

module.exports = pkg;