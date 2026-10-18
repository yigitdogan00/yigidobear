// YiğidoBear Audio Engine
// Web Audio API Sound Effects + Web Speech API TTS

let audioCtx = null;

function getAudioContext() {
    if (!audioCtx) {
        const AudioContextClass = window.AudioContext || window.webkitAudioContext;
        if (AudioContextClass) {
            audioCtx = new AudioContextClass();
        }
    }
    if (audioCtx && audioCtx.state === 'suspended') {
        audioCtx.resume();
    }
    return audioCtx;
}

// Synthesized Sound Effects
const SoundEffects = {
    playTap: function() {
        try {
            const ctx = getAudioContext();
            if (!ctx) return;
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();

            osc.type = 'sine';
            osc.frequency.setValueAtTime(480, ctx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(320, ctx.currentTime + 0.06);

            gain.gain.setValueAtTime(0.18, ctx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.06);

            osc.connect(gain);
            gain.connect(ctx.destination);

            osc.start();
            osc.stop(ctx.currentTime + 0.07);
        } catch (e) {
            console.warn('Audio playTap error:', e);
        }
    },

    playCorrect: function() {
        try {
            const ctx = getAudioContext();
            if (!ctx) return;
            const now = ctx.currentTime;

            // Cheerful two-tone Duolingo-style chord (E5 -> G#5 -> B5)
            const notes = [
                { freq: 659.25, time: 0.0, dur: 0.14 }, // E5
                { freq: 830.61, time: 0.12, dur: 0.14 }, // G#5
                { freq: 987.77, time: 0.24, dur: 0.35 }  // B5
            ];

            notes.forEach(note => {
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();
                osc.type = 'triangle';
                osc.frequency.setValueAtTime(note.freq, now + note.time);

                gain.gain.setValueAtTime(0.0, now + note.time);
                gain.gain.linearRampToValueAtTime(0.25, now + note.time + 0.02);
                gain.gain.exponentialRampToValueAtTime(0.001, now + note.time + note.dur);

                osc.connect(gain);
                gain.connect(ctx.destination);

                osc.start(now + note.time);
                osc.stop(now + note.time + note.dur);
            });
        } catch (e) {
            console.warn('Audio playCorrect error:', e);
        }
    },

    playWrong: function() {
        try {
            const ctx = getAudioContext();
            if (!ctx) return;
            const now = ctx.currentTime;

            // Descending low dissonant buzz (F3 -> D3)
            const notes = [
                { freq: 280, time: 0.0, dur: 0.15 },
                { freq: 210, time: 0.12, dur: 0.35 }
            ];

            notes.forEach(note => {
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();
                osc.type = 'sawtooth';
                osc.frequency.setValueAtTime(note.freq, now + note.time);
                osc.frequency.linearRampToValueAtTime(note.freq * 0.85, now + note.time + note.dur);

                gain.gain.setValueAtTime(0.18, now + note.time);
                gain.gain.exponentialRampToValueAtTime(0.001, now + note.time + note.dur);

                osc.connect(gain);
                gain.connect(ctx.destination);

                osc.start(now + note.time);
                osc.stop(now + note.time + note.dur);
            });
        } catch (e) {
            console.warn('Audio playWrong error:', e);
        }
    },

    playComplete: function() {
        try {
            const ctx = getAudioContext();
            if (!ctx) return;
            const now = ctx.currentTime;

            // Victory fanfare: C5, E5, G5, C6 triumph!
            const fanfare = [
                { freq: 523.25, time: 0.0, dur: 0.12 },
                { freq: 659.25, time: 0.12, dur: 0.12 },
                { freq: 783.99, time: 0.24, dur: 0.16 },
                { freq: 1046.50, time: 0.42, dur: 0.55 }
            ];

            fanfare.forEach(n => {
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();
                osc.type = 'triangle';
                osc.frequency.setValueAtTime(n.freq, now + n.time);

                gain.gain.setValueAtTime(0.01, now + n.time);
                gain.gain.linearRampToValueAtTime(0.3, now + n.time + 0.02);
                gain.gain.exponentialRampToValueAtTime(0.001, now + n.time + n.dur);

                osc.connect(gain);
                gain.connect(ctx.destination);

                osc.start(now + n.time);
                osc.stop(now + n.time + n.dur);
            });
        } catch (e) {
            console.warn('Audio playComplete error:', e);
        }
    }
};

// Web Speech API - Text to Speech
const SpeechEngine = {
    voices: [],
    
    init: function() {
        if ('speechSynthesis' in window) {
            const loadVoices = () => {
                this.voices = window.speechSynthesis.getVoices();
            };
            loadVoices();
            if (window.speechSynthesis.onvoiceschanged !== undefined) {
                window.speechSynthesis.onvoiceschanged = loadVoices;
            }
        } else {
            console.warn('Web Speech API is not supported in this browser.');
        }
    },

    getEnglishVoice: function() {
        if (!this.voices || this.voices.length === 0) {
            if ('speechSynthesis' in window) {
                this.voices = window.speechSynthesis.getVoices();
            }
        }
        // Prefer natural / google en-US or en-GB voices
        const enVoices = this.voices.filter(v => v.lang.startsWith('en'));
        const preferred = enVoices.find(v => v.name.includes('Google') || v.name.includes('Natural') || v.name.includes('Samantha') || v.name.includes('Zira'));
        return preferred || enVoices[0] || null;
    },

    speak: function(text, rate = 0.9, onEndCallback = null) {
        if (!('speechSynthesis' in window)) {
            alert('Tarayıcınız ses sentezini (SpeechSynthesis) desteklemiyor.');
            if (onEndCallback) onEndCallback();
            return;
        }

        window.speechSynthesis.cancel(); // Stop any pending speech

        const cleanText = text.replace(/[_*~#]/g, '').trim();
        if (!cleanText) return;

        const utterance = new SpeechSynthesisUtterance(cleanText);
        utterance.lang = 'en-US';
        utterance.rate = rate; // 0.9 for friendly clear learning pace, 0.6 for slow
        utterance.pitch = 1.05; // Slightly cheerful pitch

        const voice = this.getEnglishVoice();
        if (voice) {
            utterance.voice = voice;
        }

        if (onEndCallback) {
            utterance.onend = onEndCallback;
            utterance.onerror = onEndCallback;
        }

        window.speechSynthesis.speak(utterance);
    },

    speakSlow: function(text, onEndCallback = null) {
        this.speak(text, 0.6, onEndCallback);
    }
};

// Initialize SpeechEngine on DOM load
document.addEventListener('DOMContentLoaded', () => {
    SpeechEngine.init();
});
