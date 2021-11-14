/**
 * This file implements unit conversion logic
 * Here is where we convert between nutrient uptake data units
 */

/**
 * This function converts any uptake rate into standardized units
 * @param {string} rate is the rate of nutrient uptake you want to convert
 * @param {object} conversions is a table of unit conversions
 * @returns {numeric} the standardized ratio of nutrient uptake
 */
export function convertUptakeUnits (rate: string, conversions: object, places: number = 4): number {
  const parsed: RegExpMatchArray = rate.match(/^([0-9]+(?:\.[0-9]+)?) ([A-Za-z]+)\/([A-Za-z]+)$/);
  if (!parsed) {
    throw new Error(`Could not parse rate '${rate}'`);
  }
  let ratio: number = parseFloat(parsed[1]);
  let unit1: string = parsed[2];
  let unit2: string = parsed[3];
  if (unit1 === 'oz') {
    ratio /= conversions['oz/lb'] as number;
    unit1 = 'lb';
  }
  if (unit2 === 'A') {
    ratio /= conversions['bu/A'] as number;
    unit2 = 'bu';
  }
  if (unit2 === 'bu') {
    ratio /= conversions['lb/bu'] as number;
    unit2 = 'lb';
  }
  if (unit1 === 'kg') {
    ratio *= conversions['g/kg'] as number;
    unit1 = 'g';
  }
  if (unit1 === 'g' && unit2 === 't') {
    ratio /= conversions['g/t'] as number;
    unit2 = 'g';
  }
  if (unit1 === 'g' && unit2 === 'kg') {
    ratio /= conversions['g/kg'] as number;
    unit2 = 'g';
  }
  if (unit1 !== unit2 || ['lb', 'g'].indexOf(unit1) < 0) {
    throw new Error(`Incomplete conversion for rate '${rate}'`);
  }
  const coeff = Math.pow(10, places);
  return Math.round(coeff * ratio) / coeff;
}
