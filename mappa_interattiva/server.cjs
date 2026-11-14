const http=require('node:http'),fs=require('node:fs/promises'),path=require('node:path'),crypto=require('node:crypto');
const ROOT=__dirname,PROJECT=path.dirname(ROOT),PORT=Number(process.env.MAP_PORT||8767);
const FIELDS=['summary','role','state','evidence','why','alternatives','improve','contract','failure'];
const hash=n=>crypto.createHash('sha256').update(JSON.stringify(FIELDS.map(k=>n[k]??''))).digest('hex');
const read=async()=>JSON.parse(await fs.readFile(path.join(ROOT,'contenuti.json'),'utf8'));
async function atomic(file,text){const tmp=file+'.'+crypto.randomUUID()+'.tmp';try{await fs.writeFile(tmp,text,'utf8');await fs.rename(tmp,file)}finally{await fs.rm(tmp,{force:true}).catch(()=>{})}}
function reply(res,status,obj){res.writeHead(status,{'Content-Type':'application/json; charset=utf-8','Cache-Control':'no-store'});res.end(JSON.stringify(obj))}
let queue=Promise.resolve();
async function handler(req,res){
 const url=new URL(req.url,'http://127.0.0.1:'+PORT);
 const allowedHosts=['127.0.0.1:'+PORT,'localhost:'+PORT];
 if(!allowedHosts.includes(req.headers.host)){return reply(res,403,{error:'Host non consentito'})}
 if(req.method==='GET'&&url.pathname==='/api/map'){const data=await read();return reply(res,200,{data,revisions:Object.fromEntries([...data.nodes,...data.edges].map(n=>[n.id,hash(n)]))})}
 if(req.method==='PATCH'&&/^\/api\/(nodes|edges)\//.test(url.pathname)){
  if(req.headers.origin&&!['http://127.0.0.1:'+PORT,'http://localhost:'+PORT].includes(req.headers.origin))return reply(res,403,{error:'Apri la mappa dal servizio locale'});
  if(!req.headers['content-type']?.startsWith('application/json'))return reply(res,415,{error:'Formato non valido'});
  let body='';for await(const chunk of req){body+=chunk;if(Buffer.byteLength(body)>180000)return reply(res,413,{error:'Testo troppo lungo'})}
  let input;try{input=JSON.parse(body)}catch{return reply(res,400,{error:'Richiesta non valida'})}
  if(!input.fields||typeof input.fields!=='object'||Object.keys(input.fields).some(k=>!FIELDS.includes(k))||FIELDS.some(k=>typeof input.fields[k]!=='string'||input.fields[k].length>18000))return reply(res,400,{error:'Sono modificabili solo i campi descrittivi di riquadri e collegamenti (massimo 18000 caratteri per campo)'});
  const kind=url.pathname.split('/')[2],id=decodeURIComponent(url.pathname.split('/').slice(3).join('/'));
  const work=queue.then(async()=>{
   const data=await read(),n=data[kind].find(n=>n.id===id);if(!n)return reply(res,404,{error:'Elemento non trovato'});
   if(input.revision!==hash(n))return reply(res,409,{error:'Questa scheda è stata modificata altrove. Copia il testo che vuoi conservare, poi annulla e ricarica la pagina prima di riprovare.'});
   if(hash({...n,...input.fields})===hash(n))return reply(res,200,{node:n,revision:hash(n)});
   const before=JSON.stringify(data,null,2);Object.assign(n,input.fields);n.review='Descrizione modificata · evidenze da verificare';n.editedAt=new Date().toISOString();
   const backups=path.join(ROOT,'backup');await fs.mkdir(backups,{recursive:true});await fs.writeFile(path.join(backups,'contenuti-'+Date.now()+'-'+crypto.randomUUID().slice(0,8)+'.json'),before,'utf8');
   await atomic(path.join(ROOT,'contenuti.json'),JSON.stringify(data,null,2)+'\n');
   let warning=null;try{await atomic(path.join(ROOT,'contenuti.js'),'window.MAP_DATA = '+JSON.stringify(data,null,2)+';\n')}catch{warning='JSON salvato; copia offline non aggiornata. Usa il servizio locale.'}
   return reply(res,200,{node:n,revision:hash(n),warning});
  });queue=work.catch(()=>{});await work;return;
 }
 if(req.method!=='GET')return reply(res,405,{error:'Operazione non disponibile'});
 const decoded=decodeURIComponent(url.pathname),relative=decoded==='/'?'mappa_interattiva/index.html':decoded.replace(/^\//,'');
 const filename=path.resolve(PROJECT,relative);const data=await read();
 const allowedSources=new Set([...data.nodes,...data.edges].flatMap(n=>n.sources||[]).map(s=>path.resolve(PROJECT,s)));
 const inMap=filename.startsWith(ROOT+path.sep)&&!filename.slice(ROOT.length+1).split(path.sep).includes('backup');
 if(!(inMap&&['.html','.css','.js','.json','.md'].includes(path.extname(filename)))&&!allowedSources.has(filename))return reply(res,404,{error:'File non disponibile'});
 try{const bytes=await fs.readFile(filename);res.writeHead(200,{'Content-Type':(({'.html':'text/html','.css':'text/css','.js':'text/javascript','.json':'application/json'})[path.extname(filename)]||'text/plain')+'; charset=utf-8','Cache-Control':'no-store','X-Content-Type-Options':'nosniff'});res.end(bytes)}catch(e){if(e.code==='ENOENT')reply(res,404,{error:'File non trovato'});else throw e}
}
const server=http.createServer((req,res)=>handler(req,res).catch(err=>{console.error(err.message);if(!res.headersSent)reply(res,500,{error:'Salvataggio o lettura non riusciti. Il testo rimane nel modulo: riprova.'});else res.end()}));
server.listen(PORT,'127.0.0.1',()=>console.log('Mappa: http://127.0.0.1:'+PORT+'/mappa_interattiva/index.html'));
server.on('error',e=>{console.error(e.code==='EADDRINUSE'?'Servizio già attivo sulla porta '+PORT:e.message);process.exitCode=1});
