const sourceHref=s=>{const target=window.MAP_SOURCE_PATHS?.[s];return target?(/^https?:\/\//.test(target)?target:'../'+encodeURI(target)):null};
(() => {
  'use strict';
  const storageKey = 'cv-process-map-v2-rami-paralleli';
  const fields = {summary:'In una frase',role:'Funzione e dati scambiati',state:'Stato attuale',evidence:'Evidenze e limiti',why:'Perché questa scelta',alternatives:'Alternative e loro stato',improve:'Possibili miglioramenti',contract:'Coerenza dei dati',failure:'Possibili errori'};
  const $ = selector => document.querySelector(selector);
  const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const originNames = {w:'Whareformer',s:'SuperFlex',p:'Progetto',external:'Dati o modelli esterni',mixed:'Whareformer e progetto'};
  let data = structuredClone(window.MAP_DATA), selected = null, pinned = false, editing = false;
  let online = false, revisions = {}, saving = false, scale = 1, panX = 0, panY = 0;
  const viewport = $('.viewport'), board = $('.board');
  const nodeById = id => data.nodes.find(n => n.id === id);
  const item = id => [...data.nodes, ...data.edges].find(n => n.id === id);
  const notice = text => { $('#notice').textContent = text; };
  function readPositions() { try { const saved = JSON.parse(localStorage.getItem(storageKey)); return saved?.layoutId === data.layoutId ? saved.positions : null; } catch { return null; } }
  function applyPositions(positions) {
    if (!positions) return;
    data.nodes.forEach(n => { const pos = positions[n.id]; if (pos && Number.isFinite(pos.x) && Number.isFinite(pos.y)) { n.x = Math.max(n.width / 2 + 20, Math.min(data.canvas.width - n.width / 2 - 20, pos.x)); n.y = Math.max(n.height / 2 + 10, Math.min(data.canvas.height - n.height / 2 - 10, pos.y)); } });
  }
  function persistPositions() { try { localStorage.setItem(storageKey, JSON.stringify({layoutId:data.layoutId,positions:Object.fromEntries(data.nodes.map(n => [n.id,{x:n.x,y:n.y}]))})); notice('Disposizione salvata in questo browser'); } catch { notice('Per conservare la disposizione usa Esporta'); } }
  function applyView() { board.style.transform = `translate(${panX}px,${panY}px) scale(${scale})`; $('#zoom-label').textContent = Math.round(scale * 100) + '%'; }
  function zoom(next, x = viewport.clientWidth / 2, y = viewport.clientHeight / 2) { next = Math.max(.07, Math.min(2.5, next)); const ratio = next / scale; panX = x - (x - panX) * ratio; panY = y - (y - panY) * ratio; scale = next; applyView(); }
  function fitAll() { scale = Math.max(.07, Math.min(1, (viewport.clientWidth - 24) / data.canvas.width, (viewport.clientHeight - 24) / data.canvas.height)); panX = (viewport.clientWidth - data.canvas.width * scale) / 2; panY = (viewport.clientHeight - data.canvas.height * scale) / 2; applyView(); }
  function fitWidth() { scale = Math.min(1.1, (viewport.clientWidth - 20) / data.canvas.width); panX = (viewport.clientWidth - data.canvas.width * scale) / 2; panY = 8; applyView(); }
  function setPanel(open) { $('#inspector').hidden = !open; $('#toggle-panel').setAttribute('aria-expanded', String(open)); }
  function focusItem(id, move = true) {
    if (editing) return; const n = item(id); if (!n) return;
    selected = id; pinned = true; setPanel(true); renderDetail(); highlight();
    if (move) requestAnimationFrame(() => { const points = n.from ? movedPoints(n) : null, point = points ? points[Math.floor(points.length / 2)] : [n.x,n.y]; scale = Math.max(.55, Math.min(.9, (viewport.clientWidth - 40) / (n.width || 900))); panX = viewport.clientWidth / 2 - point[0] * scale; panY = viewport.clientHeight / 2 - point[1] * scale; applyView(); });
  }
  function highlight() { board.querySelectorAll('[data-node]').forEach(el => el.classList.toggle('active', el.dataset.node === selected)); board.querySelectorAll('[data-edge]').forEach(el => el.classList.toggle('active-edge', el.dataset.edge === selected)); }
  function renderDetail() {
    const n = item(selected); if (!n) { $('#detail').innerHTML = '<p>Seleziona un riquadro o un collegamento.</p>'; return; }
    $('#detail').innerHTML = `<div class="pin"><span class="meta">${esc(n.id)} · ${n.from ? 'Collegamento' : 'Riquadro'}</span><button id="pin">${pinned ? 'Sblocca scheda' : 'Fissa scheda'}</button></div><h2>${esc(n.title)}</h2><p class="review">${esc(n.review)}</p><div class="status">${esc(n.summary)}</div>${Object.entries(fields).filter(([key]) => key !== 'summary').map(([key,label]) => `<section><h3>${label}</h3><p>${esc(n[key] || '-')}</p></section>`).join('')}<section class="sources"><h3>Fonti</h3>${(n.sources || []).map(source => sourceHref(source) ? `<a href="${esc(sourceHref(source))}" target="_blank" rel="noopener">${esc(source)}</a>` : `<span>${esc(source)} (fonte non configurata)</span>`).join('') || '<p>-</p>'}</section><p class="meta">${esc(n.verified || '')}</p><button id="edit" ${online ? '' : 'disabled'}>Modifica descrizione</button><p class="meta">${online ? 'Le modifiche vengono salvate nei file del progetto.' : 'Consultazione offline. Avvia il servizio locale per modificare i commenti.'}</p>`;
    $('#pin').onclick = () => { pinned = !pinned; renderDetail(); }; $('#edit').onclick = edit;
  }
  function edit() {
    if (!online) return; const n = item(selected); editing = true; pinned = true;
    $('#detail').innerHTML = `<h2>${esc(n.title)}</h2><p>Modifica i commenti e salva nei file del progetto.</p>${Object.entries(fields).map(([key,label]) => `<label class="editor" for="field-${key}">${label}</label><textarea id="field-${key}" maxlength="18000">${esc(n[key] || '-')}</textarea>`).join('')}<div class="save-actions"><button id="save">Salva</button><button id="cancel">Annulla</button><p id="save-status" role="status"></p></div>`;
    $('#save').onclick = async () => {
      if (saving) return; saving = true; $('#save').disabled = true; $('#cancel').disabled = true; $('#save-status').textContent = 'Salvataggio…';
      try { const values = Object.fromEntries(Object.keys(fields).map(key => [key,$('#field-' + key).value])); const response = await fetch('/api/' + (n.from ? 'edges' : 'nodes') + '/' + encodeURIComponent(n.id), {method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify({revision:revisions[n.id],fields:values})}); const result = await response.json(); if (!response.ok) throw Error(result.error || 'Salvataggio non riuscito'); Object.assign(n,result.node); revisions[n.id] = result.revision; editing = false; renderDetail(); notice(result.warning || 'Descrizione salvata nei file del progetto'); }
      catch (error) { $('#save-status').textContent = error.message; }
      finally { saving = false; if ($('#save')) $('#save').disabled = false; if ($('#cancel')) $('#cancel').disabled = false; }
    };
    $('#cancel').onclick = () => { editing = false; renderDetail(); }; $('#detail').scrollTop = 0;
  }
  function movedPoints(edge) {
    const points = structuredClone(edge.originalPoints || edge.points), a = nodeById(edge.from), b = nodeById(edge.to), first = points[0], last = points.at(-1);
    const originalFirst = [...first], originalLast = [...last];
    const endpoint = b && (Math.abs(Math.abs(originalLast[0] - b.originalX) - b.width / 2) < 3 || Math.abs(Math.abs(originalLast[1] - b.originalY) - b.height / 2) < 3);
    if (a) { const dx = a.x - a.originalX, dy = a.y - a.originalY, next = points[1]; if (points.length > 2 && originalFirst[0] === next[0]) next[0] += dx; else if (points.length > 2) next[1] += dy; first[0] += dx; first[1] += dy; }
    if (endpoint) { const dx = b.x - b.originalX, dy = b.y - b.originalY, previous = points.at(-2); if (points.length > 2 && originalLast[0] === previous[0]) previous[0] += dx; else if (points.length > 2) previous[1] += dy; last[0] += dx; last[1] += dy; }
    if (points.length === 2 && first[0] !== last[0] && first[1] !== last[1]) { const mid = (first[1] + last[1]) / 2; return [first,[first[0],mid],[last[0],mid],last]; }
    return points;
  }
  function updateGeometry() {
    for (const n of data.nodes) board.querySelector(`[data-node="${n.id}"]`)?.setAttribute('transform', `translate(${n.x - n.originalX},${n.y - n.originalY})`);
    for (const edge of data.edges) { const d = movedPoints(edge).map((p,i) => (i ? 'L' : 'M') + p.join(',')).join(' '), line = board.querySelector(`[data-edge="${edge.id}"]`); line?.setAttribute('d', d); if (line?.previousElementSibling?.tagName.toLowerCase() === 'path') line.previousElementSibling.setAttribute('d', d); board.querySelector(`[data-hit="${edge.id}"]`)?.setAttribute('d', d); }
  }
  function render() {
    board.style.width = data.canvas.width + 'px'; board.style.height = data.canvas.height + 'px'; board.innerHTML = data.canvas.svg;
    const svg = board.querySelector('svg'); svg.setAttribute('role','group'); svg.setAttribute('aria-label','Mappa completa Whareformer–SuperFlex, disposizione Rami paralleli'); const firstNode = svg.querySelector('[data-node]');
    for (const n of data.nodes) {
      const el = svg.querySelector(`[data-node="${n.id}"]`); if (!el) continue;
      el.classList.add('map-node'); el.setAttribute('role','button'); el.setAttribute('tabindex','0'); el.setAttribute('aria-label',n.id + ' · ' + n.title + ' · ' + (originNames[n.origin] || '')); let drag = null;
      el.addEventListener('pointerenter', () => { if (!editing && !pinned && !$('#inspector').hidden) { selected = n.id; renderDetail(); highlight(); } });
      el.addEventListener('pointerdown', event => { if (editing || event.button !== 0) return; event.stopPropagation(); drag = {x:event.clientX,y:event.clientY,nx:n.x,ny:n.y,moved:false}; el.setPointerCapture(event.pointerId); });
      el.addEventListener('pointermove', event => { if (!drag) return; const dx = (event.clientX - drag.x) / scale, dy = (event.clientY - drag.y) / scale; if (Math.abs(dx) + Math.abs(dy) < 7 && !drag.moved) return; drag.moved = true; n.x = Math.max(n.width / 2 + 20, Math.min(data.canvas.width - n.width / 2 - 20, drag.nx + dx)); n.y = Math.max(n.height / 2 + 10, Math.min(data.canvas.height - n.height / 2 - 10, drag.ny + dy)); updateGeometry(); });
      el.addEventListener('pointerup', () => { if (drag?.moved) persistPositions(); else if (drag) focusItem(n.id,false); drag = null; }); el.addEventListener('pointercancel', () => { drag = null; });
      el.addEventListener('keydown', event => { if (editing) return; if (event.altKey && event.key.startsWith('Arrow')) { event.preventDefault(); n.x = Math.max(n.width / 2 + 20,Math.min(data.canvas.width - n.width / 2 - 20,n.x + (event.key === 'ArrowRight' ? 15 : event.key === 'ArrowLeft' ? -15 : 0))); n.y = Math.max(n.height / 2 + 10,Math.min(data.canvas.height - n.height / 2 - 10,n.y + (event.key === 'ArrowDown' ? 15 : event.key === 'ArrowUp' ? -15 : 0))); updateGeometry(); persistPositions(); } else if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); focusItem(n.id,false); } });
    }
    for (const edge of data.edges) {
      const line = svg.querySelector(`[data-edge="${edge.id}"]`); if (!line) continue; const hit = document.createElementNS('http://www.w3.org/2000/svg','path'); hit.setAttribute('d',line.getAttribute('d')); hit.setAttribute('class','edge-hit'); hit.dataset.hit = edge.id; hit.setAttribute('role','button'); hit.setAttribute('tabindex','0'); hit.setAttribute('aria-label',edge.id + ' · ' + edge.title); hit.addEventListener('pointerdown', event => event.stopPropagation()); hit.addEventListener('pointerenter', () => { if (!editing && !pinned && !$('#inspector').hidden) { selected = edge.id; renderDetail(); highlight(); } }); hit.addEventListener('click', () => focusItem(edge.id,false)); hit.addEventListener('keydown', event => { if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); focusItem(edge.id,false); } }); svg.insertBefore(hit,firstNode);
    }
    $('#node-select').innerHTML = '<option value="">Riquadri…</option>' + data.nodes.map(n => `<option value="${n.id}">${esc(n.id + ' · ' + n.title + (n.title === 'Memoria precedente' ? ' · ' + n.subtitle : ''))}</option>`).join('');
    $('#edge-select').innerHTML = '<option value="">Collegamenti…</option>' + data.edges.map(e => `<option value="${e.id}">${esc(e.id + ' · ' + e.title)}</option>`).join(''); updateGeometry(); highlight();
  }
  $('#node-select').onchange = event => { if (event.target.value) focusItem(event.target.value); }; $('#edge-select').onchange = event => { if (event.target.value) focusItem(event.target.value); };
  $('#toggle-panel').onclick = () => { if (editing) return; setPanel($('#inspector').hidden); if (!selected) { selected = data.nodes[0].id; renderDetail(); } }; $('#close-panel').onclick = () => { if (!editing) setPanel(false); };
  $('#fit').onclick = fitAll; $('#width').onclick = fitWidth; $('#actual').onclick = () => zoom(1); $('#zoomin').onclick = () => zoom(scale * 1.2); $('#zoomout').onclick = () => zoom(scale / 1.2);
  $('#reset').onclick = () => { data.nodes.forEach(n => { n.x = n.originalX; n.y = n.originalY; }); persistPositions(); updateGeometry(); fitWidth(); };
  $('#export').onclick = () => { const url = URL.createObjectURL(new Blob([JSON.stringify(data,null,2)],{type:'application/json'})), link = document.createElement('a'); link.href = url; link.download = 'mappa-rami-paralleli.json'; link.click(); setTimeout(() => URL.revokeObjectURL(url),5000); };
  $('#import').onchange = async event => {
    try { if (editing) throw Error('Salva o annulla prima di importare'); const file = event.target.files[0]; if (!file) return; const imported = JSON.parse(await file.text()); if (imported.version !== 2 || imported.layoutId !== data.layoutId || !Array.isArray(imported.nodes)) throw Error('Usa un’esportazione della mappa Rami paralleli'); const ids = new Set(); for (const n of imported.nodes) { if (ids.has(n.id) || !nodeById(n.id) || !Number.isFinite(n.x) || !Number.isFinite(n.y)) throw Error('Disposizione non valida'); ids.add(n.id); } if (ids.size !== data.nodes.length) throw Error('L’esportazione non contiene tutti i riquadri'); applyPositions(Object.fromEntries(imported.nodes.map(n => [n.id,{x:n.x,y:n.y}]))); persistPositions(); updateGeometry(); fitWidth(); notice('Disposizione importata; commenti conservati'); }
    catch (error) { notice(error.message); } finally { event.target.value = ''; }
  };
  viewport.addEventListener('wheel', event => { event.preventDefault(); const rect = viewport.getBoundingClientRect(); zoom(scale * Math.exp(-Math.max(-100,Math.min(100,event.deltaY)) * .004),event.clientX - rect.left,event.clientY - rect.top); },{passive:false});
  let pan = null;
  viewport.addEventListener('pointerdown', event => { if (event.button !== 0 || event.target.closest('[data-node],.edge-hit')) return; pan = {x:event.clientX,y:event.clientY,px:panX,py:panY}; viewport.setPointerCapture(event.pointerId); viewport.classList.add('panning'); }); viewport.addEventListener('pointermove', event => { if (pan) { panX = pan.px + event.clientX - pan.x; panY = pan.py + event.clientY - pan.y; applyView(); } });
  function endPan() { pan = null; viewport.classList.remove('panning'); } viewport.addEventListener('pointerup',endPan); viewport.addEventListener('pointercancel',endPan);
  document.addEventListener('keydown', event => { if (event.key === 'Escape' && !editing) setPanel(false); }); window.addEventListener('beforeunload', event => { if (editing) { event.preventDefault(); event.returnValue = ''; } });
  async function initialize() {
    if (location.protocol === 'http:' && ['127.0.0.1','localhost'].includes(location.hostname)) { try { const response = await fetch('/api/map',{cache:'no-store'}); if (!response.ok) throw Error(); const result = await response.json(); if (result.data.version !== 2) throw Error(); data = result.data; revisions = result.revisions; online = true; notice('Commenti salvati nel progetto'); } catch { notice('Consultazione offline'); } } else notice('Consultazione offline');
    applyPositions(readPositions()); render(); fitWidth();
  }
  initialize().catch(error => { notice('Impossibile aprire la mappa: ' + error.message); });
})();
