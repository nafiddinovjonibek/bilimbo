(function () {
    'use strict';

    var joriyAudio = null;
    var joriyTugma = null;
    var ijroRaqami = 0;
    var holat = document.getElementById('ovoz-holat');

    function xabar(matn) {
        if (!holat) return;
        holat.textContent = matn || '';
        holat.hidden = !matn;
    }

    function toxtat() {
        ijroRaqami++;
        if (joriyAudio) {
            joriyAudio.pause();
            joriyAudio.onended = joriyAudio.onerror = null;
        }
        if (joriyTugma) {
            joriyTugma.classList.remove('gapiryapti');
            joriyTugma.removeAttribute('aria-busy');
        }
        joriyAudio = null;
        joriyTugma = null;
    }

    function ijroEt(tugma, avtomatik) {
        if (!avtomatik && joriyTugma === tugma) {
            toxtat();
            return;
        }
        toxtat();
        xabar('');
        // Haqiqiy tovushlar data-play, o'zbekcha savol ovozlari data-audio da.
        var manba = tugma.dataset.play || tugma.dataset.audio;
        if (!manba) {
            if (!avtomatik) xabar('Bu savolning ovozi hozircha tayyor emas.');
            return;
        }
        var audio = new Audio(manba);
        var raqam = ijroRaqami;
        joriyAudio = audio;
        joriyTugma = tugma;
        tugma.classList.add('gapiryapti');
        tugma.setAttribute('aria-busy', 'true');

        function tugat(matn) {
            // Oldingi ijroning kechikkan hodisasi yangi ovozni to'xtatmasin.
            if (raqam !== ijroRaqami) return;
            toxtat();
            if (matn) xabar(matn);
        }
        audio.onended = function () { tugat(); };
        audio.onerror = function () { tugat('Ovozni yuklab bo‘lmadi. Qayta urinib ko‘ring.'); };
        audio.play().catch(function (error) {
            if (error.name === 'NotAllowedError') {
                // Telefonlar sahifa ochilganda avtomatik ovozni cheklashi mumkin.
                tugat(avtomatik ? '' : 'Ovozni eshitish uchun 🔊 tugmasini yana bosing.');
            } else if (error.name !== 'AbortError') {
                tugat('Ovozni yuklab bo‘lmadi. Qayta urinib ko‘ring.');
            } else {
                tugat();
            }
        });
    }

    document.addEventListener('click', function (event) {
        var tugma = event.target.closest('.ovoz-btn, .audio-btn');
        if (!tugma) return;
        event.preventDefault();
        ijroEt(tugma, false);
    });
    window.addEventListener('pagehide', toxtat);

    window.bilimboOvoz = {
        birinchiniAyt: function () {
            var tugma = document.querySelector('.kvest-bosqich.faol .ovoz-btn') ||
                        document.querySelector('.topshiriq .ovoz-btn');
            if (tugma) ijroEt(tugma, true);
        }
    };
})();
