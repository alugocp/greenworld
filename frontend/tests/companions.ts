import sinon from 'sinon';
import chai from 'chai';
import { Greenworld } from '../greenworld';
import CompanionSearch from '../companions';
const expect = chai.expect;
chai.use(require('chai-as-promised'));

describe('./frontend/companions.ts', function () {
    it('Test coverage for getSearchLink()', function () {
        const gw = new Greenworld('greenworld.com/');
        expect(gw.companions.getSearchLink({
            species: 'zea mays',
            name: 'Corn',
            id: 1
        })).to.equal('<a onclick="renderCompanions(1, `Corn`, \'zea mays\')">Corn (<i>zea mays</i>)</a>');
        expect(gw.companions.getSearchLink({
            species: 'eutrochium purpureum',
            name: 'Joe Pye\'s Weed',
            id: 2
        })).to.equal('<a onclick="renderCompanions(2, `Joe Pye\'s Weed`, \'eutrochium purpureum\')">Joe Pye\'s Weed (<i>eutrochium purpureum</i>)</a>');
    });

    it('Test coverage for getResultLink()', function () {
        const gw = new Greenworld('greenworld.com/');
        expect(gw.companions.getResultLink(
            {
                species: 'zea mays',
                name: 'Corn',
                id: 1,
                score: -1.0
            },
            'phaseolus vulgaris'
        )).to.equal('<tr><td>Corn</td><td><i>zea mays</i></td><td>-1</td><td><a onclick="renderCompanions(1, `Corn`, \'zea mays\')">Find companions</a></td><td><a href="greenworld.com/report/zea mays/phaseolus vulgaris">View report</a></td></tr>');
        expect(gw.companions.getResultLink(
            {
                species: 'eutrochium purpureum',
                name: 'Joe Pye\'s Weed',
                id: 2,
                score: 0.0
            },
            'passiflora incarnata'
        )).to.equal('<tr><td>Joe Pye\'s Weed</td><td><i>eutrochium purpureum</i></td><td>0</td><td><a onclick="renderCompanions(2, `Joe Pye\'s Weed`, \'eutrochium purpureum\')">Find companions</a></td><td><a href="greenworld.com/report/eutrochium purpureum/passiflora incarnata">View report</a></td></tr>');
    });

    it('Mocked discover()', async function () {
        const gw = new Greenworld('greenworld.com/');
        const handlers = [
            {id: 2, species: 'species1', name: 'Plant 1'},
            {id: 3, species: 'species2', name: 'Plant 2'},
            {id: 4, species: 'species3', name: 'Plant 3'},
        ];
        const fetchStub = sinon.stub(gw.wrapper, 'fetch');
        fetchStub.onCall(0).returns([[3, 0.0], [4, 0.1], [2, -1.0]]);
        fetchStub.onCall(1).returns(handlers);
        await expect(gw.companions.discover({
            id: 1,
            thresh: 2
        })).to.eventually.equal(handlers);
    });
});