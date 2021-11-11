/**
 * This file tests the unit conversion logic
 */

const conversions = require('../tasks/lib/conversions.ts');
const {expect} = require('chai');

describe('Basic conversion tests', (): void => {
  it('Test lb/A conversions', (): void => {
    const ratio = conversions.convertUptakeUnits('10 lb/A', {
      'bu/A': 10,
      'lb/bu': 10
    });
    expect(ratio).to.equal(0.1);
  });

  it('Test lb/bu conversions', (): void => {
    const ratio = conversions.convertUptakeUnits('10 lb/bu', {
      'lb/bu': 10
    });
    expect(ratio).to.equal(1);
  });

  it('Test oz/A conversions', (): void => {
    const ratio = conversions.convertUptakeUnits('10 oz/A', {
      'oz/lb': 10,
      'bu/A': 10,
      'lb/bu': 10
    });
    expect(ratio).to.equal(0.01);
  });

  it('Test oz/bu conversions', (): void => {
    const ratio = conversions.convertUptakeUnits('10 oz/bu', {
      'oz/lb': 10,
      'lb/bu': 10
    });
    expect(ratio).to.equal(0.1);
  });
});
