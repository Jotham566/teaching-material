const fs = require('fs'), vm = require('vm'), assert = require('assert'), crypto = require('crypto');
const c = {};
vm.createContext(c);
vm.runInContext(fs.readFileSync('IUEA_Teaching_Plan/assessment_operations/export_continuous_assessment.gs', 'utf8'), c);
const stored = new Map(), props = {CA_EXPORT_CUTOFF: '1794049321960'};
function add(name, value) { stored.set(name, {name, bytes: Buffer.from(value)}); }
function iterator(items) { let i = 0; return {hasNext: () => i < items.length, next: () => items[i++]}; }
function file(entry) {
  return {getName: () => entry.name, getId: () => entry.name,
    getBlob: () => ({getBytes: () => [...entry.bytes], getDataAsString: () => entry.bytes.toString()}),
    setTrashed: () => stored.delete(entry.name)};
}
const folder = {
  getFiles: () => iterator([...stored.values()].map(file)),
  getFilesByName: name => iterator(stored.has(name) ? [file(stored.get(name))] : []),
  getUrl: () => 'https://drive.example/folder'
};
c.caFolder_ = () => folder;
c.caJson_ = (_folder, name, data) => add(name, JSON.stringify(data));
c.caHash_ = bytes => crypto.createHash('sha256').update(Buffer.from(bytes)).digest('hex');
c.PropertiesService = {getScriptProperties: () => ({
  getProperty: key => props[key], setProperty: (key, value) => { props[key] = value; }
})};
c.DriveApp = {getFileById: id => file(stored.get(id))};
c.Logger = {log: () => {}};
let progress = null;
c.caProgress_ = (state, message) => { progress = {state, message}; };
for (const course of ['CML3111', 'CML3112', 'CML3113']) {
  for (let week = 1; week <= 5; week++) {
    add(`${course}_W0${week}_manifest.json`, '{}');
    add(`${course}_Q${week}_quiz.json`, '{}');
  }
}
add('quiz_deadlines.json', '{}');
add('CML3111_W01_files_1.zip', 'synthetic part');
assert.equal(c.finishCAGradingZip_(), false);
assert(stored.has('ca_index_checkpoint.json'));
assert.equal(progress, null);
let iterations = 1;
while (!c.finishCAGradingZip_()) iterations++;
assert(iterations > 1, 'indexing must resume across calls');
assert.deepEqual(progress, {state: 'COMPLETE', message: folder.getUrl()});
assert(!stored.has('ca_index_checkpoint.json'));
const index = JSON.parse(stored.get('ca_bundle.json').bytes);
assert.equal(index.files.length, 32);
assert(index.files.some(item => item.name === 'CML3111_W01_files_1.zip' &&
  item.sha256 === crypto.createHash('sha256').update('synthetic part').digest('hex')));
assert(![...stored.keys()].some(name => name.startsWith('IUEA_CA_')));
console.log('PASS: large export indexes parts incrementally and releases the folder without building a final ZIP');
