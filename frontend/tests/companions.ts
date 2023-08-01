import sinon from 'sinon';
import chai from 'chai';
import { Greenworld } from '../greenworld';
import CompanionSearch from '../companions';
const expect = chai.expect;
chai.use(require('chai-as-promised'));

describe('./frontend/companions.ts', function () {
    it('Test coverage for getLink()', function () {
        const companions = new CompanionSearch('greenworld.com/', undefined);
        expect(companions.getLink({
            species: 'zea mays',
            name: 'Corn',
            id: 1
        })).to.equal('<a onclick="renderCompanions(1, `Corn`, \'zea mays\')">Corn (<i>zea mays</i>)</a>');
        expect(companions.getLink({
            species: 'eutrochium purpureum',
            name: 'Joe Pye\'s Weed',
            id: 2
        })).to.equal('<a onclick="renderCompanions(2, `Joe Pye\'s Weed`, \'eutrochium purpureum\')">Joe Pye\'s Weed (<i>eutrochium purpureum</i>)</a>');
    });

    it('Mocked discover()', async function () {
        const gw = new Greenworld('greenworld.com/');
        const handlers = [
            {id: 2, species: 'species1', name: 'Plant 1'},
            {id: 3, species: 'species2', name: 'Plant 2'},
            {id: 4, species: 'species3', name: 'Plant 3'},
        ];
        const fetchStub = sinon.stub(gw.wrapper, 'fetch');
        fetchStub.onCall(0).returns([2, 3, 4]);
        fetchStub.onCall(1).returns(handlers);
        await expect(gw.companions.discover({
            id: 1,
            thresh: 2
        })).to.eventually.equal(handlers);
    });
});