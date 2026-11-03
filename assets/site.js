/* Shared behaviour for every Tavasz page. Page config comes from window.TAVASZ = {wa, prop}. */
const T=window.TAVASZ||{};
const $=id=>document.getElementById(id);

// particle background
(function(){
  const cv=$('bg');if(!cv)return;const cx=cv.getContext('2d');let W,H,P=[];
  function rs(){W=cv.width=innerWidth;H=cv.height=innerHeight;P=Array.from({length:Math.min(90,W/14|0)},()=>({x:Math.random()*W,y:Math.random()*H,vx:(Math.random()-.5)*.25,vy:(Math.random()-.5)*.25}))}
  rs();addEventListener('resize',rs);
  (function f(){cx.clearRect(0,0,W,H);
    const g=cx.createRadialGradient(W*.8,H*.1,0,W*.8,H*.1,W*.7);g.addColorStop(0,'rgba(23,201,122,.18)');g.addColorStop(1,'rgba(5,10,8,0)');cx.fillStyle=g;cx.fillRect(0,0,W,H);
    for(const p of P){p.x+=p.vx;p.y+=p.vy;if(p.x<0||p.x>W)p.vx*=-1;if(p.y<0||p.y>H)p.vy*=-1;
      cx.fillStyle='rgba(61,255,160,.7)';cx.fillRect(p.x,p.y,1.6,1.6);
      for(const q of P){const d=Math.hypot(p.x-q.x,p.y-q.y);if(d<120){cx.strokeStyle=`rgba(61,255,160,${.12*(1-d/120)})`;cx.beginPath();cx.moveTo(p.x,p.y);cx.lineTo(q.x,q.y);cx.stroke()}}}
    requestAnimationFrame(f)})();
})();

// year in footer
document.querySelectorAll('[data-yr]').forEach(e=>e.textContent=new Date().getFullYear());

// scroll reveal
const io=new IntersectionObserver(es=>es.forEach(x=>{if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target)}}),{threshold:.12});
document.querySelectorAll('.rv').forEach(el=>io.observe(el));

// count-up numbers
document.querySelectorAll('[data-n]').forEach(el=>{const to=+el.dataset.n;let s=null;
  const step=ts=>{s??=ts;const p=Math.min((ts-s)/1400,1);el.textContent=Math.round(to*(1-Math.pow(1-p,3)));if(p<1)requestAnimationFrame(step)};requestAnimationFrame(step)});

// 3D tilt on cards
document.addEventListener('pointermove',e=>{const c=e.target.closest?.('.card,.pcard');if(!c||matchMedia('(pointer:coarse)').matches)return;
  const r=c.getBoundingClientRect(),x=(e.clientX-r.left)/r.width,y=(e.clientY-r.top)/r.height;
  c.style.setProperty('--mx',x*100+'%');c.style.setProperty('--my',y*100+'%');
  c.style.transform=`perspective(900px) rotateY(${(x-.5)*5}deg) rotateX(${(.5-y)*5}deg) translateY(-4px)`});
document.addEventListener('pointerout',e=>{const c=e.target.closest?.('.card,.pcard');if(c)c.style.transform=''});

// hero carousel (slides: .s inside #hc, captions in data-caps JSON)
(function(){
  const hc=$('hc');if(!hc)return;
  const sl=[...hc.querySelectorAll('.s')],dots=$('hcDots'),cap=$('hcCap');
  const caps=JSON.parse(hc.dataset.caps||'[]');
  let i=0,t=null,paused=false;const reduce=matchMedia('(prefers-reduced-motion:reduce)').matches;
  sl.forEach((_,k)=>{const b=document.createElement('button');b.setAttribute('aria-label','Photo '+(k+1));b.onclick=()=>{go(k);restart()};dots.appendChild(b)});
  function load(k){const im=sl[k%sl.length].querySelector('img');if(im.dataset.src){im.src=im.dataset.src;delete im.dataset.src}}
  function go(k){i=(k+sl.length)%sl.length;load(i);load(i+1);sl.forEach((s,n)=>s.classList.toggle('on',n===i));[...dots.children].forEach((d,n)=>d.classList.toggle('on',n===i));cap.textContent=caps[i]||''}
  function restart(){clearInterval(t);if(!reduce)t=setInterval(()=>{if(!paused&&!document.hidden)go(i+1)},5000)}
  $('hcPrev').onclick=()=>{go(i-1);restart()};$('hcNext').onclick=()=>{go(i+1);restart()};
  let x0=null,y0=0;const host=hc.parentElement;
  host.addEventListener('touchstart',e=>{x0=e.touches[0].clientX;y0=e.touches[0].clientY;paused=true},{passive:true});
  host.addEventListener('touchend',e=>{paused=false;if(x0===null)return;const dx=e.changedTouches[0].clientX-x0,dy=e.changedTouches[0].clientY-y0;x0=null;if(Math.abs(dx)>45&&Math.abs(dx)>Math.abs(dy)*1.4){go(i+(dx<0?1:-1));restart()}},{passive:true});
  host.addEventListener('mouseenter',()=>paused=true);host.addEventListener('mouseleave',()=>paused=false);
  go(0);restart();
})();

// lightbox for any .ig gallery, with prev/next
(function(){
  const gal=document.querySelector('.ig');if(!gal)return;
  const lb=document.createElement('div');lb.id='lb';
  lb.innerHTML='<img alt=""><button class="lbn p" aria-label="Previous photo">←</button><button class="lbn n" aria-label="Next photo">→</button><span class="lbc"></span>';
  document.body.appendChild(lb);
  const links=[...gal.querySelectorAll('a[data-lb]')];let k=0;
  const img=lb.querySelector('img'),c=lb.querySelector('.lbc');
  function show(n){k=(n+links.length)%links.length;img.src=links[k].getAttribute('href');img.alt=links[k].querySelector('img').alt;c.textContent=(k+1)+' / '+links.length}
  gal.addEventListener('click',e=>{const a=e.target.closest('a[data-lb]');if(!a)return;e.preventDefault();show(links.indexOf(a));lb.classList.add('on')});
  lb.addEventListener('click',e=>{if(e.target.closest('.lbn.p'))show(k-1);else if(e.target.closest('.lbn.n'))show(k+1);else lb.classList.remove('on')});
  addEventListener('keydown',e=>{if(!lb.classList.contains('on'))return;if(e.key==='Escape')lb.classList.remove('on');if(e.key==='ArrowLeft')show(k-1);if(e.key==='ArrowRight')show(k+1)});
  let x0=null;lb.addEventListener('touchstart',e=>{x0=e.touches[0].clientX},{passive:true});
  lb.addEventListener('touchend',e=>{if(x0===null)return;const dx=e.changedTouches[0].clientX-x0;x0=null;if(Math.abs(dx)>50)show(k+(dx<0?1:-1))},{passive:true});
})();

// booking form -> WhatsApp
(function(){
  const f=$('bf');if(!f)return;
  const today=new Date().toISOString().slice(0,10);$('d1').min=$('d2').min=today;
  $('d1').addEventListener('change',()=>{$('d2').min=$('d1').value||today});
  f.addEventListener('submit',e=>{e.preventDefault();
    const prop=$('prop')?$('prop').value:T.prop;
    const lines=[`Hi Tavasz, I'd like to book a stay at ${prop}.`,`Name: ${$('n').value}`,`Check in: ${$('d1').value}`,`Check out: ${$('d2').value}`,`Guests: ${$('g').value}`,`Group: ${$('t').value}`];
    if($('note').value.trim())lines.push(`Note: ${$('note').value.trim()}`);
    window.open(`https://wa.me/${T.wa}?text=${encodeURIComponent(lines.join('\n'))}`,'_blank');
  });
})();
