/* "See it from above" player. Markup: .fly > .phone > video.fv + controls, and optional .clips > button[data-src][data-poster]. */
document.querySelectorAll('.fly').forEach(fly=>{
  const v=fly.querySelector('video.fv'),snd=fly.querySelector('.vsnd'),bar=fly.querySelector('.vbar i'),
        clips=[...fly.querySelectorAll('.clips button')],cap=fly.querySelector('.vcap');
  const reduce=matchMedia('(prefers-reduced-motion:reduce)').matches;
  const saver=navigator.connection&&navigator.connection.saveData;
  let loaded=false,visible=false,userPaused=false;

  function load(){if(loaded)return;loaded=true;v.src=v.dataset.src;v.load()}
  function tryPlay(){if(reduce||saver||userPaused||!visible)return;load();const p=v.play();if(p&&p.catch)p.catch(()=>{})}
  function sync(){fly.classList.toggle('playing',!v.paused&&!v.ended)}

  // load when near the screen, play only while on screen
  new IntersectionObserver(es=>es.forEach(e=>{
    if(e.isIntersecting)load();
    visible=e.intersectionRatio>=.5;
    if(visible)tryPlay();else v.pause();
  }),{threshold:[0,.5],rootMargin:'400px 0px'}).observe(fly.querySelector('.phone'));

  // tap the video to pause or play
  const toggle=()=>{load();if(v.paused){userPaused=false;v.play().catch(()=>{})}else{userPaused=true;v.pause()}};
  fly.querySelector('.phone').addEventListener('click',e=>{if(e.target.closest('.vsnd,.vbarw'))return;toggle()});
  ['play','pause','ended'].forEach(ev=>v.addEventListener(ev,sync));
  v.addEventListener('timeupdate',()=>{if(v.duration)bar.style.width=(v.currentTime/v.duration*100)+'%'});

  // sound is off until the visitor asks for it (only shown when the clip has audio)
  if(snd){
    snd.hidden=true;
    snd.addEventListener('click',()=>{v.muted=!v.muted;snd.classList.toggle('on',!v.muted);snd.setAttribute('aria-label',v.muted?'Turn sound on':'Turn sound off')});
  }

  // seek on the progress bar
  const bw=fly.querySelector('.vbarw');
  bw.addEventListener('click',e=>{const r=bw.getBoundingClientRect();load();if(v.duration)v.currentTime=(e.clientX-r.left)/r.width*v.duration});

  // switch between clips
  clips.forEach(b=>b.addEventListener('click',()=>{
    clips.forEach(c=>c.classList.toggle('on',c===b));    v.poster=b.dataset.poster;v.dataset.src=b.dataset.src;loaded=false;userPaused=false;bar.style.width='0';
    if(cap)cap.textContent=b.dataset.label||'';
    load();if(visible&&!reduce&&!saver)v.play().catch(()=>{});
  }));
});
