/* build: securinets-workshop bundle :: strip debug before release
   SECURINETS{d0nt_trust_th3_cl13nt} */

/* Minimal, self-contained typewriter: types once, then stops.
   Supports "\n" (line break) and "^<ms>" (pause) tokens. */
(function () {
    var el = document.getElementById('typed');
    if (!el) return;

    var MESSAGE = 'welcome to the web pentesting workshop.';
    var TYPE_SPEED = 50;    // ms per character
    var START_DELAY = 1200; // ms before typing begins

    var textNode = document.createTextNode('');
    var cursor = document.createElement('span');
    cursor.className = 'typed-cursor';
    cursor.textContent = '_';
    el.appendChild(textNode);
    el.appendChild(cursor);

    var i = 0;
    var out = '';

    function step() {
        if (i >= MESSAGE.length) return; // done — no loop

        var ch = MESSAGE.charAt(i++);

        // pause token: ^<milliseconds>
        if (ch === '^') {
            var m = /^\d+/.exec(MESSAGE.slice(i));
            if (m) {
                i += m[0].length;
                setTimeout(step, parseInt(m[0], 10));
                return;
            }
        }

        out += ch;
        textNode.nodeValue = out;
        setTimeout(step, TYPE_SPEED);
    }

    setTimeout(step, START_DELAY);
})();

/* Scroll-spy for the "modules" section: whichever item sits closest
   to the vertical center of the viewport is the active one, and its
   matching image is shown. Recomputed on every scroll frame. */
(function () {
    var items = Array.prototype.slice.call(document.querySelectorAll('.module-item'));
    var images = Array.prototype.slice.call(document.querySelectorAll('.module-image'));
    if (!items.length) return;

    function setActive(index) {
        items.forEach(function (item) {
            item.classList.toggle('is-active', item.dataset.index === String(index));
        });
        images.forEach(function (img) {
            img.classList.toggle('is-active', img.dataset.index === String(index));
        });
    }

    function updateActive() {
        var center = window.innerHeight / 2;
        var closest = items[0];
        var closestDist = Infinity;

        items.forEach(function (item) {
            var rect = item.getBoundingClientRect();
            var dist = Math.abs((rect.top + rect.height / 2) - center);
            if (dist < closestDist) {
                closestDist = dist;
                closest = item;
            }
        });

        setActive(closest.dataset.index);
    }

    var ticking = false;
    function onScroll() {
        if (ticking) return;
        ticking = true;
        requestAnimationFrame(function () {
            updateActive();
            ticking = false;
        });
    }

    updateActive();
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll);

    items.forEach(function (item) {
        item.addEventListener('click', function () {
            item.scrollIntoView({ behavior: 'smooth', block: 'center' });
        });
    });
})();
