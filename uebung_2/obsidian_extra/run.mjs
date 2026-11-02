// Native Obsidian-CLI auf Windows; Modell und bestehender Python-Code in Docker.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {execFileSync} from 'node:child_process';

const extra = path.dirname(fileURLToPath(import.meta.url));
const root = path.dirname(extra);
const vault = path.join(root, 'app', 'wissen');
const cli = process.env.OBSIDIAN_CLI || 'C:\\Program Files\\Obsidian\\Obsidian.com';
const phase = process.argv[2] || 'all';
function docker(action, capture=false) {
  return execFileSync('docker', ['compose','run','--rm','--no-deps','-T','-v',`${extra}:/extra`,'app','/extra/experiment.py', action],
               {cwd: root, stdio:capture?'pipe':'inherit', encoding:'utf8', windowsHide:true});
}
function obs(command, parameters=[]) {
  const start = performance.now();
  const output = execFileSync(cli, [command,...parameters], {cwd:vault, encoding:'utf8', windowsHide:true, timeout:30000}).trim();
  if (/not enabled|unable to find|Error:/i.test(output)) throw new Error(output);
  return {output, seconds:(performance.now()-start)/1000};
}
function search(query, enriched=false) {
  const scope = enriched ? 'path:_obsidian_extra' : '-path:_obsidian_extra';
  const r = obs('search',[`query=(${query}) ${scope} -file:README`, 'format=json']);
  if (!r.output.startsWith('[') && !/^No matches found\./.test(r.output)) throw new Error(`Unerwartete Suchausgabe: ${r.output}`);
  const list = r.output.startsWith('[') ? JSON.parse(r.output) : [];
  return {paths:list, seconds:r.seconds};
}
function names(paths, originals, enriched) {
  return [...new Set(paths.filter(p => enriched ? p.startsWith('_obsidian_extra/') : !p.includes('/'))
    .map(p=>path.posix.basename(p)).filter(n=>Object.hasOwn(originals,n)))];
}
function collect() {
  const prepared = JSON.parse(fs.readFileSync(path.join(extra,'vorbereitung.json'),'utf8'));
  // Einmal aus dem nativen Obsidian-Linkcache lesen, nicht aus JSON-Metadaten nachbauen.
  const graph = {};
  let graphSeconds = 0;
  for (const name of Object.keys(prepared.originals)) {
    const outgoing = obs('links', [`path=_obsidian_extra/${name}`]);
    const incoming = obs('backlinks', [`path=_obsidian_extra/${name}`, 'format=json']);
    graphSeconds += outgoing.seconds + incoming.seconds;
    let backlinks=[];
    if (incoming.output.startsWith('[') || incoming.output.startsWith('{')) {
      const parsed = JSON.parse(incoming.output);
      if (Array.isArray(parsed)) backlinks=parsed.map(x=>typeof x==='string'?x:x.file||x.path);
      else backlinks=Object.keys(parsed);
    }
    graph[name] = names([...outgoing.output.split(/\r?\n/), ...backlinks].filter(Boolean), prepared.originals, true).filter(n=>n!==name);
  }
  const editorial = JSON.parse(fs.readFileSync(path.join(extra,'metadaten.json'),'utf8'));
  for (const [name, entry] of Object.entries(editorial)) {
    const expected = [...new Set([...entry.links,...Object.entries(editorial).filter(([,e])=>e.links.includes(name)).map(([n])=>n)])].sort();
    if (JSON.stringify(expected)!==JSON.stringify([...graph[name]].sort())) throw new Error(`Obsidian-Linkcache noch unvollstaendig: ${name}`);
  }
  const data = {original_hashes:prepared.original_hashes, graph, graph_cache_s:graphSeconds, fragen:[]};
  for (const entry of prepared.fragen) {
    const q = entry.fall.frage;
    const terms = entry.begriffe;
    const escaped = terms.map(t=>t.replace(/[.*+?^${}()|[\]\\]/g,'\\$&').replaceAll('/','\\/'));
    const query = escaped.length ? `/${escaped.join('|')}/i` : '__kein_suchbegriff__';
    const a = search(query);
    const b = search(query,true);
    const metadataQuery = terms.flatMap(t=>['aliases','thema','tags'].map(k=>`[${k}:${JSON.stringify(t)}]`)).join(' OR ');
    const m = search(metadataQuery || '"__kein_suchbegriff__"',true);
    const ids = [...q.matchAll(/\b(?:[A-Z]-\d{3}|PA-\d{2})\b/gi)].map(x=>x[0]);
    for (const match of q.matchAll(/(?:§|Paragraph|Paragraf)\s*(\d+)/gi)) ids.push(`§ ${match[1]}`);
    let id = {paths:[], seconds:0};
    if (ids.length) id = search(ids.map(t=>`[kennungen:${JSON.stringify(t)}]`).join(' OR '),true);
    const preferred = names(ids.length && id.paths.length ? id.paths : m.paths, prepared.originals,true);
    const direct = names(ids.length && id.paths.length ? id.paths : [...m.paths,...b.paths],prepared.originals,true);
    data.fragen.push({frage:q, begriffe:terms, kennung:ids.length>0,
      basis:{dateien:names(a.paths,prepared.originals,false),suche:a.seconds},
      meta:{dateien:direct, bevorzugt:preferred, suche:b.seconds+m.seconds+id.seconds},
      links:{dateien:direct, bevorzugt:preferred, suche:b.seconds+m.seconds+id.seconds+graphSeconds/14},
      native:{query, metadataQuery, basis:a.paths, text_meta:b.paths, properties:m.paths, kennungen:id.paths}});
    console.log(`Obsidian ${data.fragen.length}/14: Basis=${a.paths.length}, Metadaten=${direct.length}`);
  }
  for (const [name, expected] of Object.entries(prepared.original_hashes)) {
    const text = fs.readFileSync(path.join(vault,name),'utf8').replace(/\r\n/g,'\n');
    if (crypto.createHash('sha256').update(text).digest('hex')!==expected) throw new Error(`Originaldatei veraendert: ${name}`);
  }
  fs.writeFileSync(path.join(extra,'obsidian_suche.json'), JSON.stringify(data,null,2),'utf8');
}

if (phase==='all' || phase==='prepare') docker('prepare');
if (phase==='all' || phase==='collect') collect();
if (phase==='all' || phase==='evaluate') docker('evaluate');
if (phase==='all' || phase==='audit') docker('audit');
if (phase==='all' || phase==='report') fs.writeFileSync(path.join(root,'OBSIDIAN_EXTRA.md'), docker('report',true),'utf8');
if (!['all','prepare','collect','evaluate','audit','report'].includes(phase)) throw new Error('Phase: all|prepare|collect|evaluate|audit|report');
