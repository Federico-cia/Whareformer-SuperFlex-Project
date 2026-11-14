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
        console.log('Map checks passed: resolver, assets, API, linked documents and unlisted-file rejection. No writes.');
    } finally {
        child.kill();
    }
})().catch(error => {console.error(error); process.exitCode = 1});
