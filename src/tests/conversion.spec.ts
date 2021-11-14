/**
 * This file tests the unit conversion logic
 */
import * as conversions from '../lib/conversions';
import {expect} from 'chai';

/**
 * Test out different starting units
 */
describe('Conversion unit tests', (): void => {
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
      'bu/A': 10,
      'lb/bu': 10
    });
    expect(ratio).to.equal(0.0063);
  });

  it('Test oz/bu conversions', (): void => {
    const ratio = conversions.convertUptakeUnits('10 oz/bu', {
      'lb/bu': 10
    });
    expect(ratio).to.equal(0.0625);
  });

  it('Test g/kg conversions', (): void => {
    const ratio = conversions.convertUptakeUnits('1000 g/kg');
    expect(ratio).to.equal(1);
  });

  it('Test g/t conversions', (): void => {
    const ratio = conversions.convertUptakeUnits('1000 g/t');
    expect(ratio).to.equal(0.0011);
  });

  it('Test kg/t conversions', (): void => {
    const ratio = conversions.convertUptakeUnits('1000 kg/t');
    expect(ratio).to.equal(1.1023);
  });
});

/**
 * Test out different starting values
 */
describe('Conversion number tests', (): void => {
  it('Test whole numbers', (): void => {
    const ratio = conversions.convertUptakeUnits('1000 g/kg', {
      'g/kg': 1000
    });
    expect(ratio).to.equal(1);
  });

  it('Test floating point numbers', (): void => {
    const ratio = conversions.convertUptakeUnits('1234.567 g/kg', {
      'g/kg': 1000
    }, 6);
    expect(ratio).to.equal(1.234567);
  });
});
