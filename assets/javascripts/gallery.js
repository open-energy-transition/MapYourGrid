console.log('[gallery] loaded', new Date().toISOString());

// Global: bind keyboard once
let __galleryKeyboardBound = false;

// Document-level CAPTURE: block any link under .gallery .thumbs-gallery (runs before theme handlers)
document.addEventListener('click', (e) => {
    const a = e.target.closest('.gallery .thumbs-gallery a');
    if (a) {
        e.preventDefault(); // block native navigation/lightbox
        // let it bubble so our own handlers can run
    }
}, true);

function initOneGallery(gallery) {
    // --- Guard against double init on same DOM node ---
    if (gallery.dataset.galleryInited === '1') return;
    gallery.dataset.galleryInited = '1';

    const main          = gallery.querySelector('.main-image');
    const viewerLink    = gallery.querySelector('.viewer-link');
    const prev          = gallery.querySelector('.prev');
    const next          = gallery.querySelector('.next');
    const thumbsContainer = gallery.querySelector('.thumbs-gallery');
    const viewer        = gallery.querySelector('.viewer');

    if (!main || !thumbsContainer || !viewer) return;

    // Swipe (mobile)
    let sx = 0, sy = 0, swiping = false;
    function onTouchStart(e){ const t=(e.touches&&e.touches[0])||e; sx=t.clientX; sy=t.clientY; swiping=true; }
    function onTouchMove(e){
        if (!swiping) return;
        const t=(e.touches&&e.touches[0])||e, dx=t.clientX-sx, dy=t.clientY-sy;
        if (Math.abs(dx)>10 && Math.abs(dx)>Math.abs(dy)*1.5) e.preventDefault();
    }
    function onTouchEnd(e){
        if (!swiping) return; swiping=false;
        const t=(e.changedTouches&&e.changedTouches[0])||e, dx=t.clientX-sx, dy=t.clientY-sy;
        const THRESHOLD=40, MAX_VERTICAL=80;
        if (Math.abs(dx)>THRESHOLD && Math.abs(dy)<MAX_VERTICAL) show(index + (dx>0 ? -1 : +1));
    }
    viewer.addEventListener('touchstart', onTouchStart, { passive: true });
    viewer.addEventListener('touchmove',  onTouchMove,  { passive: false });
    viewer.addEventListener('touchend',   onTouchEnd,   { passive: true });

    // Collect IMG thumbs (works even if wrapped in <a> or other wrappers)
    const thumbs = Array.from(gallery.querySelectorAll('.thumb-gallery')).map(node =>
    node.tagName === 'IMG' ? node : (node.querySelector('img.thumb-gallery, img') || node)
    ).filter(el => el && el.tagName === 'IMG');

    if (!thumbs.length) return;

    if (!main.hasAttribute('tabindex')) main.setAttribute('tabindex', '0');

    let index = Math.max(thumbs.findIndex(t => t.classList.contains('active')), 0);

    const srcFor = (imgEl) =>
    imgEl.dataset.full ||
    imgEl.closest('a')?.getAttribute('href') ||
    imgEl.currentSrc ||
    imgEl.src;

    function show(i) {
        index = (i + thumbs.length) % thumbs.length;
        const el = thumbs[index];
        const nextSrc = srcFor(el);

        if (nextSrc) {
            main.src = nextSrc;
            if (viewerLink) viewerLink.href = nextSrc;        // keep lightbox link in sync
            const glb = document.getElementById('gallery-img-glb'); // if you use this
            if (glb) glb.href = nextSrc;
            if (typeof lightbox !== 'undefined' && lightbox?.reload) lightbox.reload();
        }
        main.alt = el.alt || `Image ${index + 1}`;

        thumbs.forEach(t => t.classList.remove('active'));
        el.classList.add('active');

        if (prev) prev.style.display = (index === 0) ? 'none' : '';
        if (next) next.style.display = (index === thumbs.length - 1) ? 'none' : '';
    }

    // Thumbnails: swap image (stop other handlers)
    thumbsContainer.addEventListener('click', (e) => {
        const t = e.target.closest('.thumb-gallery');
        if (!t || !thumbsContainer.contains(t)) return;

        e.preventDefault();
        if (e.stopImmediatePropagation) e.stopImmediatePropagation();
        e.stopPropagation();

        const imgEl = (t.tagName === 'IMG') ? t : (t.querySelector('img.thumb-gallery, img') || null);
        const i = imgEl ? thumbs.indexOf(imgEl) : -1;
        if (i >= 0) show(i);
    });

        // Arrows: ensure only our handler runs, using the CURRENT index
        prev?.addEventListener('mousedown', (e) => e.preventDefault());
        next?.addEventListener('mousedown', (e) => e.preventDefault());

        prev?.addEventListener('click', (e) => {
            e.preventDefault();
            if (e.stopImmediatePropagation) e.stopImmediatePropagation();
            e.stopPropagation();
            show(index - 1);
        });
        next?.addEventListener('click', (e) => {
            e.preventDefault();
            if (e.stopImmediatePropagation) e.stopImmediatePropagation();
            e.stopPropagation();
            show(index + 1);
        });

        // Init once all listeners are in place
        show(index);

        // Bind keyboard once globally (Left/Right arrows)
        if (!__galleryKeyboardBound) {
            __galleryKeyboardBound = true;
            document.addEventListener('keydown', (e) => {
                // Find the first (or focused) gallery to control; simplest: the first one
                const g = document.querySelector('.gallery[data-gallery-inited="1"]');
                if (!g) return;
                const state = g.__galleryState;
                if (!state) return;

                if (e.key === 'ArrowLeft')  state.show(state.index - 1);
                if (e.key === 'ArrowRight') state.show(state.index + 1);
            }, { passive: true });
        }

        // Expose minimal state so the global keyboard handler can use the CURRENT index
        gallery.__galleryState = {
            get index(){ return index; },
            show
        };
}

function initGalleries(root = document) {
    root.querySelectorAll('.gallery').forEach(initOneGallery);
}

// Initial load + SPA
if (document.readyState !== 'loading') initGalleries(document);
else document.addEventListener('DOMContentLoaded', () => initGalleries(document));

if (window.document$) {
    window.document$.subscribe(() => initGalleries(document));
}
