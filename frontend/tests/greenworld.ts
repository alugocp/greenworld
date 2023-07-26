import { expect } from 'chai';
import { Greenworld } from '../greenworld';

describe('./frontend/greenworld.ts', function () {
    it('Test coverage for getPlantsUrl()', function () {
        const gw = new Greenworld('greenworld.com/');
        expect(gw.getPlantsUrl('species1')).to.equal('greenworld.com/plant/species1');
        expect(gw.getPlantsUrl('species1', 'species2')).to.equal('greenworld.com/report/species1/species2');
    });
});