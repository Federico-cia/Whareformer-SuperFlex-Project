// Read-only check of approved fields, endpoints, source registry and local server.
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const {spawn}=require('node:child_process');const root=path.resolve(__dirname,'..');
const read=p=>fs.readFileSync(path.join(root,p),'utf8');
const context={window:{}};vm.createContext(context);
vm.runInContext(read('mappa_interattiva/fonti.js'),context);vm.runInContext(read('mappa_interattiva/contenuti.js'),context);
const d=JSON.parse(read('mappa_interattiva/contenuti.json'));
assert.equal(JSON.stringify(d),JSON.stringify(context.window.MAP_DATA));assert.equal(d.version,2);
assert.equal(d.nodes.length,39);assert.equal(d.edges.length,53);
const ids=new Set([...d.nodes,...d.groups].map(n=>n.id));assert.equal(ids.size,40);
const snapshot=JSON.parse(read('context/evidence/map_20261122/approved_fields.json'));
const approved=new Map([...snapshot.nodes,...snapshot.edges].map(n=>[n.ref,n.fields]));
const fields=['summary','role','state','evidence','why','alternatives','improve','contract','failure'];
for(const item of [...d.nodes,...d.edges]){
 for(const key of fields){assert.equal(typeof item[key],'string');assert(item[key].trim());
  if(item.review==='Testo confermato da Marco'||item.review==='Testo manuale conservato')assert.equal(item[key],approved.get(item.id)?.[key],item.id+':'+key);}
 for(const source of item.sources||[])assert(context.window.MAP_SOURCE_PATHS[source],'Unconfigured source: '+source);
}
for(const e of d.edges)assert(ids.has(e.from)&&ids.has(e.to));
assert(!d.edges.some(e=>e.id==='C34'||e.id==='C40'));
assert.equal((d.canvas.svg.match(/data-node=/g)||[]).length,39);assert.equal((d.canvas.svg.match(/data-edge=/g)||[]).length,53);
const helper=read('mappa_interattiva/app.js').split('\n').find(l=>l.startsWith('const sourceHref='));vm.runInContext(helper,context);
assert.equal(vm.runInContext('sourceHref("missing")',context),null);
const port=Number(process.env.CHECK_MAP_PORT||18768);
const child=spawn(process.execPath,[path.join(root,'mappa_interattiva/server.cjs')],{env:{...process.env,MAP_PORT:String(port)},stdio:['ignore','pipe','pipe'],windowsHide:true});
let log='';child.stderr.on('data',b=>log+=b);
(async()=>{try{
 await new Promise((resolve,reject)=>{const timer=setTimeout(()=>reject(Error('Server timeout: '+log)),10000);child.once('error',e=>{clearTimeout(timer);reject(e)});child.once('exit',c=>{clearTimeout(timer);reject(Error('Server exit '+c+': '+log))});child.stdout.once('data',()=>{clearTimeout(timer);resolve()})});
 const base='http://127.0.0.1:'+port+'/';
 for(const name of ['mappa_interattiva/index.html','mappa_interattiva/fonti.js','api/map'])assert.equal((await fetch(base+name)).status,200,name);
 for(const target of new Set(Object.values(context.window.MAP_SOURCE_PATHS)))if(!/^https?:/.test(target))assert.equal((await fetch(base+target)).status,200,target);
 assert.equal((await fetch(base+'AGENTS.md')).status,404);
 const served=await(await fetch(base+'api/map')).json();assert.equal(JSON.stringify(served.data),JSON.stringify(d));assert.equal(Object.keys(served.revisions).length,92);
 console.log('Map checks passed: 39 nodes, 53 edges, 828 fields; approved comments, offline copy, source registry, SVG and local API. No writes.');
 }finally{child.kill();}})().catch(e=>{console.error(e);process.exitCode=1});
