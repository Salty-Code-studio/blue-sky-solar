const hdr=document.querySelector('header'),sticky=document.querySelector('.sticky-cta'),quote=document.getElementById('quote');
let quoteVisible=false;
if(quote)new IntersectionObserver(e=>{quoteVisible=e[0].isIntersecting;onScroll()}).observe(quote);
function onScroll(){const y=scrollY;hdr.classList.toggle('scrolled',y>8);if(sticky)sticky.classList.toggle('show',y>700&&!quoteVisible)}
addEventListener('scroll',onScroll,{passive:true});onScroll();

const mb=document.querySelector('.menu-btn'),mn=document.querySelector('.mobile-nav');
mb.addEventListener('click',()=>{const o=mn.classList.toggle('open');mb.setAttribute('aria-expanded',o)});
mn.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{mn.classList.remove('open');mb.setAttribute('aria-expanded',false)}));

const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
const io=new IntersectionObserver(es=>es.forEach(e=>{if(!e.isIntersecting)return;e.target.classList.add('in');io.unobserve(e.target);
  const b=e.target.querySelector('b[data-count]');if(b&&!reduce){const end=+b.dataset.count,suf=b.dataset.suffix||'',t0=performance.now();
    (function tick(t){const k=Math.min(1,(t-t0)/1400),v=Math.round(end*(1-Math.pow(1-k,3)));b.textContent=v.toLocaleString('en-US')+suf;if(k<1)requestAnimationFrame(tick)})(t0)}
}),{threshold:.15,rootMargin:'0px 0px -40px 0px'});
document.querySelectorAll('.rv').forEach(el=>io.observe(el));

const qf=document.getElementById('qform');if(qf)qf.addEventListener('submit',e=>{e.preventDefault();const f=e.target;
  const bad=[...f.querySelectorAll('[required]')].find(i=>!i.value.trim());if(bad){bad.focus();bad.style.borderColor='#d64545';return}
  f.classList.add('done')});

const here=location.pathname.split('/').pop()||'index.html';document.querySelectorAll('nav.main a,.mobile-nav a').forEach(a=>{if(a.getAttribute('href')===here)a.classList.add('on')});
if(/-bonaire\.html$/.test(here))document.querySelectorAll('nav.main a[href="systems.html"],.mobile-nav a[href="systems.html"]').forEach(a=>a.classList.add('on'));
const g=new URLSearchParams(location.search).get('goal');if(g){const r=document.querySelector('#qform input[name=goal][value="'+g+'"]');if(r)r.checked=true}
