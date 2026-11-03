/* River Hill "weekend map". Needs #mapSvg, #mPanel, #mList, #mapChips and window.TAVASZ.wa. */
(function(){
  const T=window.TAVASZ||{};
  // km: road km from River Hill (Aripara) or from Anakkampoyil town; null = ask us
  const P=[
   {id:'ar',n:'Aripara Waterfall',t:'water',km:4,a:250,src:'From River Hill',d:'Popular waterfall on the Thiruvambady to Anakkampoyil road. Best after rain.'},
   {id:'vm',n:'Vellarimala Trek',t:'trek',km:null,a:165,src:'Trailhead: Muthappanpuzha',d:'The trek starts at Muthappanpuzha, the village after Anakkampoyil. Olichuchattam falls is about a 6 km hike from there. Go with a guide.'},
   {id:'th',n:'Thusharagiri Falls',t:'water',km:13.6,a:20,src:'From River Hill, about 35 min by road',d:'One of Kozhikode\'s best known waterfalls, on the Chalippuzha river. Fullest in monsoon.'},
   {id:'pv',n:'Poovaranthode',t:'water',km:null,a:320,src:'Ask us for the route',d:'River, rocks and green hills. A good half-day outing.'},
   {id:'kk',n:'Kakkadampoyil',t:'trek',km:null,a:55,src:'Ask us for the route',d:'Cool hill area with viewpoints. It is a separate place from Anakkampoyil, so ask us how to plan both.'},
   {id:'ur',n:'Urumi Falls',t:'water',km:null,a:215,src:'Ask us for the route',d:'A lesser-known fall that guests love. Ask us for the trail guide.'},
   {id:'kz',n:'Kozhikode City',t:'town',km:46.5,a:285,src:'From Anakkampoyil town',d:'Railway station, beach and the airport side of your trip.'},
   {id:'wy',n:'Wayanad',t:'town',km:52.2,a:118,src:'From Anakkampoyil town',d:'Hill district next door. Easy to pair with your stay.'},
   {id:'sb',n:'Sulthan Bathery',t:'town',km:63.9,a:80,src:'From Anakkampoyil town',d:'Gateway town of north Wayanad.'}
  ];
  const C=300,R=(km)=>km==null?172:60+Math.sqrt(km)*23.75;
  const pos=p=>{const r=R(p.km),a=p.a*Math.PI/180;return[C+r*Math.sin(a),C-r*Math.cos(a)]};
  const svg=document.getElementById('mapSvg'),panel=document.getElementById('mPanel'),list=document.getElementById('mList'),chips=document.getElementById('mapChips');
  const NS='http://www.w3.org/2000/svg';let sel=null,filter='all';
  const rings=[[10,'10 km'],[25,'25 km'],[50,'50 km']];
  let h='<defs><radialGradient id="sg" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate(300 300) scale(260)"><stop offset="0" stop-color="#3dffa0" stop-opacity=".0"/><stop offset="1" stop-color="#3dffa0" stop-opacity=".35"/></radialGradient></defs>';
  h+='<g aria-hidden="true">';
  for(let i=0;i<5;i++)h+=`<path class="topo" style="animation-delay:${-i*2}s" d="M${40+i*22} ${330+i*10} C ${120+i*10} ${150+i*20}, ${260-i*8} ${90+i*18}, ${360+i*6} ${170+i*14} S ${540-i*14} ${300+i*8}, ${500-i*20} ${470-i*12}"/>`;
  rings.forEach(([k,l])=>{const r=60+Math.sqrt(k)*23.75;h+=`<circle class="ring" cx="300" cy="300" r="${r}"/><text class="rlab" x="${300+r*0.71+4}" y="${300-r*0.71-4}">${l}</text>`});
  h+='<circle class="ring" cx="300" cy="300" r="172" style="stroke:rgba(255,211,107,.22)"/>';
  h+='<g class="sweep"><path d="M300 300 L300 40 A260 260 0 0 1 430 75 Z" fill="url(#sg)"/></g>';
  h+='<circle class="ripple" cx="300" cy="300" r="22"/><circle class="ripple" cx="300" cy="300" r="22"/></g>';
  h+='<g id="routeG"></g><g id="nodes"></g>';
  h+='<g><circle cx="300" cy="300" r="15" fill="#3dffa0"/><circle cx="300" cy="300" r="6" fill="#032014"/><text x="300" y="338" text-anchor="middle" class="cl">River Hill</text></g>';
  svg.innerHTML=h;
  const nodes=document.getElementById('nodes'),routeG=document.getElementById('routeG');
  P.forEach((p,i)=>{const[x,y]=pos(p);const left=x<300;
    const g=document.createElementNS(NS,'g');g.setAttribute('class','node'+(p.km==null?' unk':''));g.setAttribute('tabindex','0');g.setAttribute('role','button');g.setAttribute('aria-label',p.n+(p.km!=null?', '+p.km+' kilometres':''));g.dataset.id=p.id;
    g.innerHTML=`<circle class="halo" cx="${x}" cy="${y}" r="20"/><circle class="dot" cx="${x}" cy="${y}" r="9"/><circle cx="${x}" cy="${y}" r="28" fill="transparent"/><text class="lab" x="${x+(left?-16:16)}" y="${y+5}" text-anchor="${left?'end':'start'}">${p.n.replace(' Waterfall','').replace(' Falls','').replace(' Trek','')}</text><text class="num" x="${x}" y="${y+7}" text-anchor="middle">${i+1}</text>`;
    g.onclick=()=>pick(p.id);g.onkeydown=e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();pick(p.id)}};
    nodes.appendChild(g);
    const b=document.createElement('button');b.dataset.id=p.id;b.innerHTML=`<span><i class="ix">${i+1}</i>${p.n}</span><em>${p.km!=null?p.km+' km':'ask us'}</em>`;b.onclick=()=>pick(p.id);list.appendChild(b)});
  [['all','All'],['water','Waterfalls'],['trek','Treks & hills'],['town','Towns']].forEach(([k,l])=>{const b=document.createElement('button');b.textContent=l;b.setAttribute('role','tab');b.className=k==='all'?'on':'';b.onclick=()=>{filter=k;[...chips.children].forEach(c=>c.classList.toggle('on',c===b));apply();if(sel&&k!=='all'&&P.find(x=>x.id===sel).t!==k)pick(P.find(x=>k==='all'||x.t===k).id)};chips.appendChild(b)});
  function apply(){const show=p=>filter==='all'||p.t===filter;nodes.querySelectorAll('.node').forEach(n=>n.classList.toggle('dim',!show(P.find(p=>p.id===n.dataset.id))));list.querySelectorAll('button').forEach(b=>b.classList.toggle('hide',!show(P.find(p=>p.id===b.dataset.id))))}
  function count(el,to){if(matchMedia('(prefers-reduced-motion:reduce)').matches){el.textContent=to;return}let s=null;const st=ts=>{s??=ts;const q=Math.min((ts-s)/700,1),v=to*(1-Math.pow(1-q,3));el.textContent=to%1?v.toFixed(1):Math.round(v);if(q<1)requestAnimationFrame(st)};requestAnimationFrame(st)}
  function pick(id){sel=id;const p=P.find(x=>x.id===id),[x,y]=pos(p);
    nodes.querySelectorAll('.node').forEach(n=>n.classList.toggle('on',n.dataset.id===id));list.querySelectorAll('button').forEach(b=>b.classList.toggle('on',b.dataset.id===id));
    const cx=(300+x)/2+(y-300)*.18,cy=(300+y)/2-(x-300)*.18;
    routeG.innerHTML=`<path id="rp" class="route" pathLength="1" d="M300 300 Q${cx} ${cy} ${x} ${y}"/><circle r="5" fill="#fff"><animateMotion dur="2.2s" repeatCount="indefinite" begin="1s"><mpath href="#rp"/></animateMotion></circle>`;
    const msg=encodeURIComponent(`Hi Tavasz, I'm planning a stay at River Hill and want to visit ${p.n}. Can you help with the route and timing?`);
    panel.innerHTML=`<span class="mono">${{water:'Waterfall',trek:'Trek / hills',town:'Town'}[p.t]}</span><h3>${p.n}</h3><div class="big-km">${p.km!=null?'<span id="kmv">0</span><small>km</small>':'<span style="font-size:.5em">Ask us</span>'}</div><span class="src">${p.src}</span><p>${p.d}</p><a class="btn solid" target="_blank" rel="noopener" href="https://wa.me/${T.wa}?text=${msg}">Plan this trip on WhatsApp</a>`;
    if(p.km!=null)count(document.getElementById('kmv'),p.km)}
  // On phones, zoom the drawing to its own content so it fills the full width instead of sitting small in a wide frame.
  const box=svg.parentElement,wideVB='-150 0 930 600',phone=matchMedia('(max-width:700px)');
  function fit(){
    svg.setAttribute('viewBox',wideVB);
    if(!phone.matches){box.style.aspectRatio='930/600';return}
    const b=nodes.getBBox(),pad=16;
    const x0=Math.min(b.x,270)-pad,y0=Math.min(b.y,270)-pad,x1=Math.max(b.x+b.width,330)+pad,y1=Math.max(b.y+b.height,354)+pad;
    svg.setAttribute('viewBox',`${x0} ${y0} ${x1-x0} ${y1-y0}`);
    box.style.aspectRatio=`${x1-x0}/${y1-y0}`;
  }
  fit();addEventListener('resize',fit);
  pick('ar');
})();
