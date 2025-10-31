// js/main.js
// Main interactivity: 
// sentinel-driven hero text & bg crossfade,
// overlay dim,
// counters,
// filters, 
// modals,
// carousel
document.addEventListener('DOMContentLoaded', () => {
  // ------ Elements
  const sentinels = Array.from(document.querySelectorAll('.sentinel'));
  const heroTitle = document.getElementById('hero-title');
  const heroSub = document.getElementById('hero-sub');
  const bgA = document.getElementById('bg-layer-a');
  const bgB = document.getElementById('bg-layer-b');
  const overlay = document.getElementById('bg-overlay');
  const heroFixed = document.getElementById('hero-fixed');

  let activeBg = bgA;
  let inactiveBg = bgB;

  // ------ Preload helper
  function preload(url, cb){
    const img = new Image();
    img.src = url;
    img.onload = cb || function(){};
  }

  // ------ Crossfade
  function crossfadeBg(url){
    preload(url, () => {
      inactiveBg.style.backgroundImage = `url('${url}')`;
      inactiveBg.style.transition = 'opacity 900ms ease-in-out';
      inactiveBg.style.opacity = 1;
      activeBg.style.opacity = 0;
      setTimeout(() => {
        const tmp = activeBg;
        activeBg = inactiveBg;
        inactiveBg = tmp;
        inactiveBg.style.opacity = 0;
      }, 950);
    });
  }

  // Intersection observer to change texts when sentinel >55% visible
  const io = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      const node = entry.target;
      const title = node.dataset.title || '';
      const sub = node.dataset.sub || '';
      const bg = node.dataset.bg || '';

      // fade out > update > fade in
      heroTitle.style.opacity = 0;
      heroSub.style.opacity = 0;
      setTimeout(() => {
        heroTitle.textContent = title;
        heroSub.textContent = sub;
        heroTitle.style.opacity = 1;
        heroSub.style.opacity = 1;
      }, 220);

      if (bg) crossfadeBg(bg);
    });
  }, { threshold: 0.55 });

  sentinels.forEach(s => io.observe(s));

  // Scroll-driven overlay & subtle translate for hero
  function onScroll(){
    const center = window.innerHeight / 2;
    let best = null;
    let bestDist = Infinity;
    sentinels.forEach(s => {
      const r = s.getBoundingClientRect();
      const mid = r.top + r.height/2;
      const dist = Math.abs(mid - center);
      if (dist < bestDist){ bestDist = dist; best = { node: s, dist }; }
    });
    if (!best) return;
    const maxDist = window.innerHeight / 2;
    const progress = 1 - Math.min(bestDist / maxDist, 1); // 0..1
    // overlay more dark when not centered
    const overlayOpacity = clamp((1 - progress) * 0.8, 0, 0.9);
    overlay.style.opacity = overlayOpacity;
    // hero translate
    heroTitle.style.transform = `translateY(${(1 - progress) * 18}px)`;
    heroSub.style.transform = `translateY(${(1 - progress) * 10}px)`;
    heroTitle.style.opacity = clamp(0.35 + progress, 0, 1);
    heroSub.style.opacity = clamp(0.2 + progress, 0, 1);
  }
  window.addEventListener('scroll', debounce(onScroll, 12));
  window.addEventListener('resize', debounce(onScroll, 60));
  onScroll();

  /* ------------------ Counters ------------------ */
  const counters = Array.from(document.querySelectorAll('.stat-num'));
  if (counters.length){
    const cIo = new IntersectionObserver((entries, obs) => {
      entries.forEach(entry => {
        if (entry.isIntersecting){
          const el = entry.target;
          const target = parseInt(el.dataset.target || '0', 10);
          const dur = 1400;
          const start = performance.now();
          (function run(now){
            const t = Math.min(1, (now - start) / dur);
            const val = Math.floor(target * easeOutCubic(t));
            el.textContent = val.toLocaleString();
            if (t < 1) requestAnimationFrame(run);
            else obs.unobserve(el);
          })(start);
        }
      });
    }, { threshold: 0.4 });
    counters.forEach(c => cIo.observe(c));
  }

  function easeOutCubic(t){ return 1 - Math.pow(1 - t, 3); }

  /* ------------------ Filters ------------------ */
  const filters = Array.from(document.querySelectorAll('.filter'));
  const grid = document.getElementById('projects-grid');
  if (filters.length && grid){
    filters.forEach(btn => {
      btn.addEventListener('click', () => {
        filters.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const cat = btn.dataset.filter;
        Array.from(grid.children).forEach(tile => {
          if (cat === 'all') tile.style.display = '';
          else {
            const has = (tile.dataset.cat || '').split(' ').includes(cat);
            tile.style.display = has ? '' : 'none';
          }
        });
      });
    });
  }

  /* ------------------ Carousel (beta) ------------------ */
  (function initCarousel(){
    const carousel = document.getElementById('carousel');
    if (!carousel) return;
    const track = carousel.querySelector('.carousel-track');
    const prev = carousel.querySelector('.carousel-nav.prev');
    const next = carousel.querySelector('.carousel-nav.next');
    let idx = 0;
    const cards = Array.from(track.children);
    function update(){
      const gap = 18;
      const cardWidth = cards[0].offsetWidth + gap;
      const x = - (cardWidth * idx);
      track.style.transform = `translateX(${x}px)`;
    }
    prev.addEventListener('click', ()=> { idx = Math.max(0, idx-1); update(); });
    next.addEventListener('click', ()=> { idx = Math.min(cards.length-1, idx+1); update(); });
    window.addEventListener('resize', debounce(update, 60));
    update();
  })();

  /* ------------------ Modals & Tools ------------------ */
  const modalOverlay = document.getElementById('modal-overlay');
  const modalContent = document.getElementById('modal-content');
  const modalClose = document.getElementById('modal-close');

  function openModal(html){
    modalContent.innerHTML = html;
    modalOverlay.style.display = 'flex';
    modalOverlay.setAttribute('aria-hidden','false');
    document.body.style.overflow = 'hidden';
  }
  function closeModal(){ modalOverlay.style.display = 'none'; modalOverlay.setAttribute('aria-hidden','true'); modalContent.innerHTML = ''; document.body.style.overflow = ''; }

  document.addEventListener('click', (e) => {
    // ------ open triggers
    if (e.target.matches('#open-gpt, #tool-gpt')) openModal(getGptUI());
    if (e.target.matches('#open-files, #open-files-2, #tool-files')) openModal(getFilesUI());
    if (e.target.matches('#open-diag, #tool-diag')) openModal(getDiagUI());
    if (e.target.closest('#modal-close') || e.target === modalOverlay) closeModal();

    // ------ inside modal delegated actions
    if (e.target && e.target.id === 'chat-send') {
      const input = document.getElementById('chat-input');
      const log = document.getElementById('chat-log');
      if (!input || !log) return;
      const q = input.value.trim(); if (!q) return;
      appendChat(log, 'You', q);
      appendChat(log, 'hck-GPT', mockReply(q));
      input.value = ''; log.scrollTop = log.scrollHeight;
    }
    if (e.target && e.target.classList.contains('file')) {
      const path = e.target.dataset.path;
      const preview = document.getElementById('file-preview');
      if (preview) preview.textContent = `// Demo preview for ${path}\nprint("Hello from ${path}")\n`;
    }
    if (e.target && e.target.id === 'diag-run') {
      const logs = document.getElementById('diag-logs');
      if (!logs) return;
      logs.textContent = '[INFO] Starting diagnostics...\n';
      setTimeout(()=> logs.textContent += '[OK] Static files reachable.\n', 500);
      setTimeout(()=> logs.textContent += '[OK] Mock API ping: 200 OK.\n', 1100);
      setTimeout(()=> logs.textContent += '[WARN] DB connection: demo mode.\n', 1600);
      setTimeout(()=> logs.textContent += '[OK] Completed: 2 OK, 1 WARN.\n', 2100);
    }
  });

  function appendChat(el, who, text){
    const node = document.createElement('div');
    node.style.marginBottom = '8px';
    node.innerHTML = `<strong style="color:#8be6d8">${who}:</strong> ${escapeHtml(text)}`;
    el.appendChild(node);
  }
  function escapeHtml(s){ return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }
  function mockReply(q){
    q = q.toLowerCase();
    if (q.includes('minigpt')) return 'miniGPT is a minimal decoder-only model for learning — see README.';
    if (q.includes('diagn')) return 'Run Diagnostics → Diagnostic Console. In demo, checks are mocked.';
    return 'Demo agent: for full features, open repos or run local backend.';
  }

  function getGptUI(){
    return `
      <h2>hck-GPT (alpha)</h2>
      <div style="display:flex; gap:12px;">
        <div style="flex:1">
          <div id="chat-log" style="height:260px; overflow:auto; background:#071022; padding:10px; border-radius:8px;"></div>
          <div style="display:flex; gap:8px; margin-top:8px;">
            <input id="chat-input" placeholder="Ask about a project..." style="flex:1; padding:8px; border-radius:6px; border:1px solid rgba(255,255,255,0.04); background:transparent; color:inherit;">
            <button id="chat-send" class="btn">Send</button>
          </div>
        </div>
        <aside style="width:220px;">
          <h4>Quick prompts</h4>
          <button class="btn-sm" data-prompt="Tell me about miniGPT">miniGPT</button>
          <button class="btn-sm" data-prompt="How do I run diagnostics?">Diagnostics</button>
        </aside>
      </div>
    `;
  }

  function getFilesUI(){
    return `
      <h2>HCK_Files manager (alpha)</h2>
      <div style="display:grid; grid-template-columns: 320px 1fr; gap:12px;">
        <div style="background:#061223; padding:12px; border-radius:8px; height:360px; overflow:auto;">
          <ul style="list-style:none; padding-left:8px; color:var(--muted);">
            <li><strong>/projects</strong>
              <ul>
                <li class="file" data-path="projects/miniGPT/README.md">miniGPT/README.md</li>
                <li class="file" data-path="projects/miniGPT/train.py">miniGPT/train.py</li>
                <li class="file" data-path="projects/hck-files/README.md">hck-files/README.md</li>
              </ul>
            </li>
          </ul>
        </div>
        <div style="background:#071022; padding:12px; border-radius:8px; height:360px; overflow:auto;">
          <pre id="file-preview" style="white-space:pre-wrap; color:#cfeff0;"></pre>
        </div>
      </div>
    `;
  }

  function getDiagUI(){
    return `
      <h2>Diagnostic Console</h2>
      <p class="muted">Run connectivity tests and export reports (demo).</p>
      <div style="display:flex; gap:8px;">
        <button id="diag-run" class="btn">Run Full Test</button>
        <button id="diag-export" class="btn-outline">Export Report</button>
      </div>
      <pre id="diag-logs" style="margin-top:12px; background:#071022; padding:10px; border-radius:8px; height:260px; overflow:auto;"></pre>
    `;
  }

  /* ------------------ Contact form demo ------------------ */
  const contactForm = document.getElementById('contact-form');
  if (contactForm){
    contactForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const name = contactForm.name.value || 'Friend';
      alert(`Thanks ${name}! Message received (demo).`);
      contactForm.reset();
    });
  }

  /* ------------------ Utility functions ------------------ */
  function debounce(fn, wait=80){ return window.debounce ? window.debounce(fn, wait) : (function(){ let t; return (...a)=>{ clearTimeout(t); t = setTimeout(()=> fn(...a), wait); }; })(); }
  function clamp(v,a=0,b=1){ return window.clamp ? window.clamp(v,a,b) : Math.max(a, Math.min(b, v)); }
});

// HCK!