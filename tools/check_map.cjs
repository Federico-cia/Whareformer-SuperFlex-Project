// Read-only smoke check of map source resolution and local document serving.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const {spawn} = require('node:child_process');
const root = path.resolve(__dirname, '..');
const context = {window: {}};
vm.createContext(context);
vm.runInContext(fs.readFileSync(path.join(root, 'mappa_interattiva/fonti.js'), 'utf8'), context);
const data = JSON.parse(fs.readFileSync(path.join(root, 'mappa_interattiva/contenuti.json'), 'utf8'));
vm.runInContext(fs.readFileSync(path.join(root, 'mappa_interattiva/contenuti.js'), 'utf8'), context);
assert.equal(JSON.stringify(context.window.MAP_DATA), JSON.stringify(data), 'Offline copy differs from authoritative JSON');
assert.equal(data.version, 2);
assert.equal(data.nodes.length, 39);
assert.equal(data.edges.length, 49);
const ids = new Set([...data.nodes, ...(data.groups || [])].map(item => item.id));
assert.equal(ids.size, data.nodes.length + (data.groups || []).length, 'Duplicate node or group ID');
const fields = ['summary', 'role', 'state', 'evidence', 'why', 'alternatives', 'improve', 'contract', 'failure'];
const approved = JSON.parse(fs.readFileSync(path.join(root, 'context/evidence/map_20261121/COMMENTI_STRUTTURA_APPROVATA.json'), 'utf8'));
const approvedById = new Map([...approved.nodes, ...approved.edges].map(item => [item.ref, item]));
const point3 = JSON.parse(fs.readFileSync(path.join(root, 'context/evidence/point3_20261121/approved_map_point3_fields.json'), 'utf8'));
for (const item of point3.nodes) approvedById.set(item.ref, item);
for (const item of [...data.nodes, ...data.edges]) {
    for (const field of fields) {
        assert.equal(typeof item[field], 'string', item.id + ':' + field);
        assert(item[field].trim(), item.id + ':' + field + ' is empty');
        // Subsequent manual edits are legitimate; the original confirmed text is checked only while its status is retained.
        if (point3.nodes.some(n => n.ref === item.id) || item.review === 'Testo confermato da Marco' || item.review === 'Testo manuale conservato') {
            assert.equal(item[field], approvedById.get(item.id)?.fields[field], item.id + ':' + field + ' differs from the confirmed text');
        }
    }
}
for (const edge of data.edges) {
    assert(ids.has(edge.from) && ids.has(edge.to), 'Missing endpoint: ' + edge.id);
}
assert.equal((data.canvas.svg.match(/data-node="/g) || []).length, data.nodes.length);
assert.equal((data.canvas.svg.match(/data-edge="/g) || []).length, data.edges.length);
const helper = fs.readFileSync(path.join(root, 'mappa_interattiva/app.js'), 'utf8').split('\n').find(line => line.startsWith('const sourceHref='));
vm.runInContext(helper, context);
assert.equal(vm.runInContext('sourceHref("ROADMAP_CICLO_GEOMETRICO.md")', context), '../context/memory/ROADMAP_CICLO_GEOMETRICO.md');
assert.equal(vm.runInContext('sourceHref("missing.md")', context), null);
assert(vm.runInContext('sourceHref("Whareformer-repo/src/feature_extraction/utils/common.py")', context).startsWith('https://github.com/jacobchalk/Whareformer/blob/82dd'));
const child = spawn(process.execPath, [path.join(root, 'mappa_interattiva/server.cjs')], {
    env: {...process.env, MAP_PORT: '18767'}, stdio: ['ignore', 'pipe', 'pipe'], windowsHide: true
});
let log = '';
child.stderr.on('data', data => {log += data});
(async () => {
    try {
        await new Promise((resolve, reject) => {
            const timer = setTimeout(() => reject(new Error('Map server did not start: '+log)), 5000);
            child.once('error', error => {clearTimeout(timer); reject(error)});
            child.once('exit', code => {clearTimeout(timer); reject(new Error('Map server exited '+code+': '+log))});
            child.stdout.once('data', () => {clearTimeout(timer); resolve()});
        });
        const base = 'http://127.0.0.1:18767/';
        for (const name of ['mappa_interattiva/index.html', 'mappa_interattiva/fonti.js', 'api/map']) {
            assert.equal((await fetch(base+name)).status, 200, name);
        }
        for (const target of Object.values(context.window.MAP_SOURCE_PATHS)) {
            if (!/^https?:/.test(target)) assert.equal((await fetch(base+target)).status, 200, target);
        }
        assert.equal((await fetch(base+'AGENTS.md')).status, 404);
        const served = await (await fetch(base+'api/map')).json();
        assert.equal(JSON.stringify(served.data), JSON.stringify(data), 'API differs from authoritative JSON');
        assert.equal(Object.keys(served.revisions).length, 88);
        console.log('Map checks passed: 39 nodes, 49 edges, 792 fields, offline copy, confirmed text, endpoints, SVG, resolver, assets, API and linked documents. No writes.');
    } finally {
        child.kill();
    }
})().catch(error => {console.error(error); process.exitCode = 1});
