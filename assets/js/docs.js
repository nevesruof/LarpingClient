/* Documentation search, accessible navigation and catalog filtering. */
(() => {
 const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
 const input=$('[data-dsearch]'),box=$('.dresults');let cached=null,selected=0,results=[],sequence=0;
 const escape=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 const getIndex=()=>cached||(cached=fetch('/assets/data/search.json').then(r=>{if(!r.ok)throw Error();return r.json();}).catch(e=>{cached=null;throw e;}));
 function closeSearch(){if(!box)return;box.hidden=true;input.setAttribute('aria-expanded','false');input.removeAttribute('aria-activedescendant');}
 function draw(){box.innerHTML=results.length?results.map((r,i)=>'<a role="option" id="doc-result-'+i+'" aria-selected="'+String(i===selected)+'" href="'+escape(r.u)+'" class="'+(i===selected?'sel':'')+'"><b>'+escape(r.t)+'</b><span>'+escape(r.x)+'</span></a>').join(''):'<p class="none">No results for “'+escape(input.value)+'”.</p>';if(results.length)input.setAttribute('aria-activedescendant','doc-result-'+selected);else input.removeAttribute('aria-activedescendant');}
 async function search(){const current=++sequence,q=input.value.trim().toLowerCase();if(!q){closeSearch();return;}try{const all=await getIndex();if(current!==sequence)return;const words=q.split(/\s+/);results=all.map(item=>{const t=item.t.toLowerCase(),content=(t+' '+item.x+' '+(item.k||'')).toLowerCase();return [words.every(w=>content.includes(w))?words.reduce((n,w)=>n+(t===w?10:t.startsWith(w)?6:t.includes(w)?4:1),0):0,item];}).filter(x=>x[0]).sort((a,b)=>b[0]-a[0]).slice(0,8).map(x=>x[1]);selected=0;box.hidden=false;input.setAttribute('aria-expanded','true');draw();}catch{box.hidden=false;box.innerHTML='<p class="none">Search is unavailable. Use the navigation below.</p>';}}
 input?.addEventListener('focus',()=>{getIndex().catch(()=>{});if(input.value.trim())search();});
 input?.addEventListener('input',search);
 input?.addEventListener('keydown',e=>{if(e.key==='Escape'){closeSearch();return;}if(box.hidden)return;if(['ArrowDown','ArrowUp'].includes(e.key)){e.preventDefault();selected=(selected+(e.key==='ArrowDown'?1:results.length-1))%Math.max(1,results.length);draw();$('#doc-result-'+selected)?.scrollIntoView({block:'nearest'});}if(e.key==='Enter'&&results[selected]){e.preventDefault();location.href=results[selected].u;closeSearch();}});
 document.addEventListener('click',e=>{if(!e.target.closest('.dsearch'))closeSearch();});
 const toggle=$('.dside-toggle'),side=$('.dside'),mobile=matchMedia('(max-width:860px)');
 function closeDocs(){side?.classList.remove('open');toggle?.setAttribute('aria-expanded','false');if(side)side.inert=mobile.matches;}
 function openDocs(){side.classList.add('open');side.inert=false;toggle.setAttribute('aria-expanded','true');}
 toggle?.addEventListener('click',()=>{if(side.classList.contains('open'))closeDocs();else openDocs();});
 $('[data-close-docs]')?.addEventListener('click',()=>{closeDocs();toggle.focus();});
 side?.addEventListener('click',e=>{if(e.target.closest('.dgroup a'))closeDocs();});
 mobile.addEventListener('change',closeDocs);closeDocs();
 document.addEventListener('keydown',e=>{if(e.key==='/'&&!e.metaKey&&!e.ctrlKey&&!/INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName)){e.preventDefault();if(mobile.matches)openDocs();input?.focus();}if(e.key==='Escape'&&side?.classList.contains('open')){closeDocs();toggle.focus();}});
 const filter=$('[data-msearch]'),buttons=$$('[data-f]'),modules=$$('.mod'),heads=$$('.mcat');let category='all';
 function apply(){const words=filter.value.trim().toLowerCase().split(/\s+/).filter(Boolean),counts={};let count=0;modules.forEach(m=>{const show=(category==='all'||m.dataset.cat===category)&&words.every(w=>m.dataset.text.includes(w));m.hidden=!show;if(show){count++;counts[m.dataset.cat]=(counts[m.dataset.cat]||0)+1;}});heads.forEach(h=>h.hidden=!counts[h.dataset.cat]);$$('.dtoc a').forEach(a=>{if(a.hash.startsWith('#cat-'))a.hidden=!counts[a.hash.slice(5).toUpperCase()];});$('.mod-empty').hidden=count>0;$('[data-mcount]').textContent=count+' of '+modules.length+' modules';}
 filter?.addEventListener('input',apply);
 buttons.forEach(button=>button.addEventListener('click',()=>{category=button.dataset.f;buttons.forEach(b=>{b.classList.toggle('on',b===button);b.setAttribute('aria-pressed',String(b===button));});apply();}));
 function openHash(){let id;try{id=decodeURIComponent(location.hash.slice(1));}catch{return;}const target=document.getElementById(id);if(target?.classList.contains('mod')){if(filter){filter.value='';category='all';buttons.forEach(b=>{b.classList.toggle('on',b.dataset.f==='all');b.setAttribute('aria-pressed',String(b.dataset.f==='all'));});apply();}target.open=true;setTimeout(()=>target.scrollIntoView({block:'start'}),50);}}
 if(filter){apply();openHash();addEventListener('hashchange',openHash);}
 const links=$$('.dtoc a'),targets=links.map(a=>document.getElementById(a.hash.slice(1))).filter(Boolean);
 if(targets.length){const observer=new IntersectionObserver(entries=>{entries.forEach(entry=>{if(entry.isIntersecting)links.forEach(a=>a.classList.toggle('active',a.hash==='#'+entry.target.id));});},{rootMargin:'-100px 0px -60% 0px'});targets.forEach(t=>observer.observe(t));}
})();
