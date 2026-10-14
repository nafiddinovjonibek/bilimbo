const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const vm = require('node:vm');

const source = fs.readFileSync(path.join(__dirname, '../static/js/savol-ovozi.js'), 'utf8');

function setup() {
    const events = {};
    const audios = [];
    const status = { hidden: true, textContent: '' };
    let activeStage = null;
    let firstQuestion = null;
    const window = { addEventListener: (name, handler) => { events[name] = handler; } };
    const document = {
        getElementById: () => status,
        addEventListener: (name, handler) => { events[name] = handler; },
        querySelector: selector => selector.includes('.faol') ? activeStage : firstQuestion
    };
    class Audio {
        constructor(src) {
            this.src = src;
            this.paused = false;
            this.promise = new Promise((resolve, reject) => { this.reject = reject; });
            audios.push(this);
        }
        play() { return this.promise; }
        pause() { this.paused = true; }
    }
    vm.runInNewContext(source, { window, document, Audio });
    return {
        window, events, audios, status,
        click: button => events.click({ target: { closest: () => button }, preventDefault() {} }),
        stage: button => { activeStage = button; },
        first: button => { firstQuestion = button; }
    };
}

function button(dataset) {
    const classes = new Set();
    return { dataset, classes,
        classList: { add: value => classes.add(value), remove: value => classes.delete(value) },
        setAttribute() {}, removeAttribute() {} };
}

test('starting another sound stops the old one; a late rejection cannot stop the new sound', async () => {
    const app = setup();
    const first = button({ audio: '/static/first.mp3' });
    const second = button({ play: '/static/cow.wav' });
    app.click(first);
    app.click(second);
    app.audios[0].reject({ name: 'AbortError' });
    await Promise.resolve();
    assert.equal(app.audios[0].paused, true);
    assert.equal(app.audios[1].paused, false);
    assert.equal(first.classes.has('gapiryapti'), false);
    assert.equal(second.classes.has('gapiryapti'), true);
    assert.equal(app.audios[1].src, '/static/cow.wav');
});

test('a kvest reads the active stage even when an earlier hidden question exists', () => {
    const app = setup();
    app.first(button({ audio: '/static/hidden-first.mp3' }));
    app.stage(button({ audio: '/static/active-second.mp3' }));
    app.window.bilimboOvoz.birinchiniAyt();
    assert.equal(app.audios[0].src, '/static/active-second.mp3');
});

test('blocked autoplay clears the busy state and the speaker can be clicked again', async () => {
    const app = setup();
    const question = button({ audio: '/static/question.mp3' });
    app.first(question);
    app.window.bilimboOvoz.birinchiniAyt();
    app.audios[0].reject({ name: 'NotAllowedError' });
    await Promise.resolve();
    assert.equal(question.classes.has('gapiryapti'), false);
    assert.equal(app.status.hidden, true);
    app.click(question);
    assert.equal(app.audios.length, 2);
    assert.equal(question.classes.has('gapiryapti'), true);
});

test('missing speech shows a message and never starts a different language voice', () => {
    const app = setup();
    app.click(button({ say: 'O‘zbekcha yangi savol', audio: '' }));
    assert.equal(app.audios.length, 0);
    assert.equal(app.status.hidden, false);
    assert.match(app.status.textContent, /tayyor emas/);
});

test('clicking the speaking button again stops it; leaving the page stops playback', () => {
    const app = setup();
    const question = button({ audio: '/static/question.mp3' });
    app.click(question);
    app.click(question);
    assert.equal(app.audios.length, 1);
    assert.equal(app.audios[0].paused, true);
    assert.equal(question.classes.has('gapiryapti'), false);
    app.click(question);
    app.events.pagehide();
    assert.equal(app.audios[1].paused, true);
});
