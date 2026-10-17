(() => {
    'use strict';
    const config = JSON.parse(document.getElementById('reader-config').textContent);
    const pages = document.getElementById('reader-pages');
    const position = document.getElementById('reader-position');
    const entries = [];
    const queue = [];
    let current = 1;
    let loading = 0;
    let suspended = false;
    let cooldownUntil = 0;
    let cooldownTimer;
    let scrollFrame;

    // Placeholders keep every page in the scroll flow, including unloaded pages.
    const fragment = document.createDocumentFragment();
    for (let number = 1; number <= config.pages; number += 1) {
        const element = document.createElement('section');
        element.className = 'reader-sheet';
        element.id = `book-page-${number}`;
        element.setAttribute('aria-label', `${number}-sahifa`);
        element.innerHTML = `
            <p class="reader-caption">${number} / ${config.pages}</p>
            <div class="reader-frame">
                <div class="reader-paper">
                    <canvas class="reader-page" width="1" height="1" role="img"
                        aria-label="${number}-sahifa. ${config.pages} sahifadan." hidden></canvas>
                    <div class="reader-placeholder">
                        <p class="reader-message">Sahifa yuklanmoqda…</p>
                        <button type="button" class="btn reader-retry" hidden>Qayta urinish</button>
                    </div>
                </div>
            </div>`;
        const entry = {
            number, element, state: 'idle', near: false, controller: null,
            paper: element.querySelector('.reader-paper'),
            canvas: element.querySelector('canvas'),
            placeholder: element.querySelector('.reader-placeholder'),
            message: element.querySelector('.reader-message'),
            retry: element.querySelector('.reader-retry'),
        };
        entry.retry.addEventListener('click', () => {
            if (entry.state === 'error') {
                entry.state = 'idle';
                enqueue(entry);
                pump();
            }
        });
        entries.push(entry);
        fragment.append(element);
    }
    pages.append(fragment);

    function release(entry) {
        entry.controller?.abort();
        // Release bitmap memory while retaining the page's measured aspect ratio.
        entry.canvas.width = 1;
        entry.canvas.height = 1;
        entry.canvas.hidden = true;
        entry.placeholder.hidden = false;
        entry.message.textContent = 'Sahifa yuklanmoqda…';
        entry.retry.hidden = true;
        if (entry.state !== 'loading') entry.state = 'idle';
    }

    function enqueue(entry) {
        if (!entry.near || entry.state !== 'idle' || suspended) return;
        entry.state = 'queued';
        entry.message.textContent = 'Sahifa yuklanmoqda…';
        entry.retry.hidden = true;
        queue.push(entry);
    }

    function pump() {
        if (suspended) return;
        clearTimeout(cooldownTimer);
        if (cooldownUntil > Date.now()) {
            cooldownTimer = setTimeout(pump, cooldownUntil - Date.now());
            return;
        }
        queue.sort((a, b) => Math.abs(a.number - current) - Math.abs(b.number - current));
        while (loading < 2 && queue.length) {
            const entry = queue.shift();
            if (!entry.near || entry.state !== 'queued') continue;
            entry.state = 'loading';
            loading += 1;
            load(entry).finally(() => {
                loading -= 1;
                pump();
            });
        }
    }

    async function load(entry) {
        const controller = new AbortController();
        entry.controller = controller;
        try {
            const url = new URL(config.pageUrl.replace(/\/1\/$/, `/${entry.number}/`), location.origin);
            const response = await fetch(url, {
                credentials: 'same-origin', cache: 'no-store', redirect: 'error',
                headers: { 'X-Book-Token': config.token }, signal: controller.signal,
            });
            if (response.status === 429) {
                const seconds = Number(response.headers.get('Retry-After')) || 60;
                cooldownUntil = Math.max(cooldownUntil, Date.now() + seconds * 1000);
                entry.state = 'queued';
                entry.message.textContent = 'Biroz kuting, sahifa avtomatik ochiladi…';
                queue.push(entry);
                return;
            }
            if (response.status === 403) throw new Error('O‘qishni davom ettirish uchun sahifani yangilang.');
            if (!response.ok || response.headers.get('Content-Type') !== 'image/webp') throw new Error();
            const image = await createImageBitmap(await response.blob());
            try {
                if (!entry.near || controller.signal.aborted || suspended) return;
                entry.paper.style.aspectRatio = `${image.width} / ${image.height}`;
                entry.canvas.width = image.width;
                entry.canvas.height = image.height;
                entry.canvas.getContext('2d').drawImage(image, 0, 0);
                entry.canvas.hidden = false;
                entry.placeholder.hidden = true;
                entry.state = 'loaded';
            } finally {
                image.close();
            }
        } catch (error) {
            if (!controller.signal.aborted && entry.near && !suspended) {
                entry.state = 'error';
                entry.message.textContent = error.message.startsWith('O‘qishni')
                    ? error.message : 'Sahifa ochilmadi. Internetni tekshirib, qayta urinib ko‘ring.';
                entry.retry.hidden = false;
            }
        } finally {
            entry.controller = null;
            if (entry.state === 'loading') entry.state = 'idle';
            if (!entry.near || suspended) release(entry);
            enqueue(entry);
            schedulePosition();
        }
    }

    const observer = new IntersectionObserver(changes => {
        for (const change of changes) {
            const entry = entries[Number(change.target.dataset.number) - 1];
            entry.near = change.isIntersecting;
            if (entry.near) enqueue(entry);
            else release(entry);
        }
        pump();
    }, { rootMargin: '1000px 0px' });

    function updatePosition() {
        scrollFrame = null;
        const line = Math.min(innerHeight * .35, 280);
        let low = 0;
        let high = entries.length - 1;
        while (low < high) {
            const middle = Math.ceil((low + high) / 2);
            if (entries[middle].element.getBoundingClientRect().top <= line) low = middle;
            else high = middle - 1;
        }
        const number = low + 1;
        position.textContent = `Sahifa ${number} / ${config.pages}`;
        if (number !== current) {
            current = number;
            history.replaceState(null, '', `#sahifa=${current}`);
        }
    }

    function schedulePosition() {
        if (!suspended && !scrollFrame) scrollFrame = requestAnimationFrame(updatePosition);
    }

    function goToHash() {
        const number = Number(new URLSearchParams(location.hash.slice(1)).get('sahifa'));
        if (Number.isInteger(number) && number >= 1 && number <= config.pages) {
            current = number;
            entries[number - 1].element.scrollIntoView({ block: 'start' });
        }
        schedulePosition();
    }

    document.getElementById('reader-zoom').addEventListener('change', event => {
        const anchor = entries[current - 1].element;
        const before = anchor.getBoundingClientRect();
        pages.style.setProperty('--reader-zoom', `${event.target.value}%`);
        const after = anchor.getBoundingClientRect();
        const offset = before.top < 0 ? before.top * after.height / before.height : before.top;
        window.scrollBy(0, after.top - offset);
        schedulePosition();
    });
    pages.addEventListener('contextmenu', event => {
        if (event.target.closest('.reader-paper')) event.preventDefault();
    });
    pages.addEventListener('dragstart', event => event.preventDefault());
    document.addEventListener('keydown', event => {
        if ((event.ctrlKey || event.metaKey) && ['s', 'p'].includes(event.key.toLowerCase())) {
            event.preventDefault();
        }
    });
    window.addEventListener('scroll', schedulePosition, { passive: true });
    window.addEventListener('resize', schedulePosition);
    window.addEventListener('hashchange', goToHash);
    window.addEventListener('pagehide', () => {
        suspended = true;
        observer.disconnect();
        clearTimeout(cooldownTimer);
        cancelAnimationFrame(scrollFrame);
        scrollFrame = null;
        queue.length = 0;
        for (const entry of entries) {
            entry.near = false;
            release(entry);
        }
    });
    window.addEventListener('pageshow', event => {
        if (!event.persisted) return;
        suspended = false;
        for (const entry of entries) observer.observe(entry.element);
        schedulePosition();
    });
    goToHash();
    for (const entry of entries) {
        entry.element.dataset.number = String(entry.number);
        observer.observe(entry.element);
    }
})();
