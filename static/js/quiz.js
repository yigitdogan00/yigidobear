// YiğidoBear Lesson Quiz Engine
// Strict 10-Question Standard + Blocking Retry on Incorrect Answer

class LessonQuiz {
    constructor(lessonId, initialHearts, isDemo = false, isPremium = false) {
        this.lessonId = lessonId;
        this.hearts = initialHearts;
        this.isDemo = isDemo;
        this.isPremium = isPremium || (document.querySelector('.lesson-hearts-premium') !== null);
        this.questions = [];
        this.currentIndex = 0;      // 0 to 9 (10 questions per lesson/exam)
        this.selectedAnswer = null; // string for MC, array of strings for word order
        this.placedWords = [];      // for word order: array of { id, word, bankIdx }
        
        // States: 'READY', 'CHECKING', 'CORRECT', 'WRONG_RETRY', 'FINISHED'
        this.state = 'READY';
        this.correctCount = 0;
        this.totalAttempts = 0;

        // DOM Elements
        this.progressBar = document.getElementById('lesson-progress');
        this.heartsCountEl = document.getElementById('lesson-hearts-count');
        this.workspaceEl = document.getElementById('question-workspace');
        this.footerEl = document.getElementById('lesson-footer');
        this.feedbackSectionEl = document.getElementById('feedback-section');
        this.actionBtn = document.getElementById('action-button');

        this.init();
    }

    async init() {
        this.updateHeartsUI();
        this.bindEvents();

        try {
            const res = await fetch(`/api/lesson/${this.lessonId}/questions`);
            const data = await res.json();
            if (data.success && data.questions.length > 0) {
                this.questions = data.questions;
                this.renderQuestion();
            } else {
                this.workspaceEl.innerHTML = '<p style="text-align:center; padding: 40px; font-weight:800;">Bu derste henüz soru bulunmuyor.</p>';
            }
        } catch (e) {
            console.error('Failed to load lesson questions:', e);
            this.workspaceEl.innerHTML = '<p style="text-align:center; padding: 40px; color:red;">Sorular yüklenirken hata oluştu.</p>';
        }
    }

    bindEvents() {
        // Main action button click dispatcher
        this.actionBtn.addEventListener('click', () => {
            if (this.actionBtn.classList.contains('btn-disabled')) return;

            if (this.state === 'READY') {
                this.submitAnswer();
            } else if (this.state === 'WRONG_RETRY') {
                this.retryCurrentQuestion();
            } else if (this.state === 'CORRECT') {
                this.nextQuestion();
            }
        });

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                if (!this.actionBtn.classList.contains('btn-disabled')) {
                    this.actionBtn.click();
                }
            } else if (this.state === 'READY' && this.currentQuestion && this.currentQuestion.type === 'multiple_choice') {
                const keyNum = parseInt(e.key);
                if (keyNum >= 1 && keyNum <= this.currentQuestion.options.length) {
                    const card = document.querySelectorAll('.option-card')[keyNum - 1];
                    if (card) card.click();
                }
            }
        });
    }

    get currentQuestion() {
        return this.questions[this.currentIndex];
    }

    updateHeartsUI(animate = false) {
        if (this.isPremium) return;
        if (this.heartsCountEl) {
            this.heartsCountEl.textContent = this.hearts;
        }
        if (animate) {
            const container = document.querySelector('.lesson-hearts-display');
            if (container) {
                container.classList.add('pulsing');
                setTimeout(() => container.classList.remove('pulsing'), 600);
            }
        }
    }

    // Progress bar advances by exactly 10% per correctly completed question (10 steps)
    updateProgressUI() {
        const total = Math.max(10, this.questions.length);
        const percent = Math.min(100, Math.round((this.currentIndex / total) * 100));
        this.progressBar.style.width = `${percent}%`;
    }

    renderQuestion() {
        const q = this.currentQuestion;
        this.state = 'READY';
        this.selectedAnswer = null;
        this.placedWords = [];
        this.updateProgressUI();

        // Reset bottom drawer to neutral
        this.footerEl.className = 'lesson-footer quiz-feedback-bar';
        this.feedbackSectionEl.innerHTML = '';
        this.actionBtn.textContent = 'KONTROL ET';
        this.actionBtn.className = 'btn-3d btn-blue btn-disabled';

        const isListening = (q.type === 'word_order');
        const questionInstruction = isListening ? 'Dinle ve cümleyi kur:' : q.instruction;

        // Auto speak question prompt if listening / word_order
        if (isListening && q.english_speech) {
            setTimeout(() => {
                const normalBtn = document.getElementById('audio-normal-btn');
                if (normalBtn) normalBtn.classList.add('playing');
                SpeechEngine.speak(q.english_speech, 0.9, () => {
                    if (normalBtn) normalBtn.classList.remove('playing');
                });
            }, 350);
        } else if (q.english_speech && q.type !== 'multiple_choice') {
            setTimeout(() => {
                SpeechEngine.speak(q.english_speech, 0.9);
            }, 350);
        }

        const questionNumber = this.currentIndex + 1;
        const totalQuestions = this.questions.length;

        let questionHtml = `
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                <span style="font-size: 13px; font-weight: 800; color: var(--ocean-primary); background: var(--ocean-soft-bg); padding: 4px 10px; border-radius: 8px;">
                    Soru ${questionNumber} / ${totalQuestions}
                </span>
                <span style="font-size: 12px; font-weight: 700; color: var(--gray-text);">
                    ${isListening ? '🎧 Dinleme & Kelime Sıralama' : (q.type === 'multiple_choice' ? 'Çoktan Seçmeli' : 'Kelime Sıralama')}
                </span>
            </div>

            <h1 class="question-instruction">${questionInstruction}</h1>
            
            <div class="prompt-container">
                <img src="/static/images/mascot_happy.svg" id="question-mascot" alt="Küçük Ayıcık" class="prompt-mascot" title="Ayıcık Yiğido">
                <div class="prompt-bubble ${isListening ? 'listening-bubble' : ''}" id="prompt-bubble">
                    ${isListening ? `
                        <div class="audio-btn-group listening-audio-group">
                            <button class="audio-btn audio-btn-large" id="audio-normal-btn" title="Cümleyi Dinle (Normal Hız)">
                                <svg width="26" height="26" viewBox="0 0 24 24" fill="currentColor">
                                    <path d="M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02zM14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z"/>
                                </svg>
                            </button>
                            <button class="audio-btn turtle audio-btn-turtle-large" id="audio-slow-btn" title="Yavaş Dinle (0.6x)">
                                🐢
                            </button>
                        </div>
                    ` : `
                        <span class="prompt-text">${q.prompt_text}</span>
                        ${q.english_speech ? `
                            <div class="audio-btn-group">
                                <button class="audio-btn" id="audio-normal-btn" title="Telaffuz Dinle (Web Speech API)">
                                    <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor">
                                        <path d="M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02zM14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z"/>
                                    </svg>
                                </button>
                                <button class="audio-btn turtle" id="audio-slow-btn" title="Yavaş Telaffuz Dinle">
                                    🐢
                                </button>
                            </div>
                        ` : ''}
                    `}
                </div>
            </div>
        `;

        if (q.type === 'multiple_choice') {
            questionHtml += `<div class="options-grid">`;
            q.options.forEach((opt, idx) => {
                questionHtml += `
                    <div class="option-card" data-index="${idx}" data-val="${opt.replace(/"/g, '&quot;')}">
                        <div class="option-key-badge">${idx + 1}</div>
                        <div class="option-text">${opt}</div>
                    </div>
                `;
            });
            questionHtml += `</div>`;
        } else if (q.type === 'word_order') {
            questionHtml += `
                <div class="word-order-area">
                    <div class="sentence-assembly-zone" id="assembly-zone">
                        <span class="assembly-placeholder" id="assembly-placeholder">Cümleyi oluşturmak için aşağıdaki kelimelere dokun</span>
                    </div>
                    <div class="word-bank" id="word-bank">
                        ${q.options.map((word, idx) => `
                            <div class="word-tile" data-bank-idx="${idx}" data-word="${word.replace(/"/g, '&quot;')}">
                                ${word}
                            </div>
                        `).join('')}
                    </div>
                </div>
            `;
        }

        this.workspaceEl.innerHTML = questionHtml;

        // Audio pronunciation bindings
        if (q.english_speech) {
            const normalBtn = document.getElementById('audio-normal-btn');
            const slowBtn = document.getElementById('audio-slow-btn');
            if (normalBtn) {
                normalBtn.addEventListener('click', () => {
                    SoundEffects.playTap();
                    normalBtn.classList.add('playing');
                    SpeechEngine.speak(q.english_speech, 0.9, () => {
                        normalBtn.classList.remove('playing');
                    });
                });
            }
            if (slowBtn) {
                slowBtn.addEventListener('click', () => {
                    SoundEffects.playTap();
                    slowBtn.classList.add('playing');
                    SpeechEngine.speakSlow(q.english_speech, () => {
                        slowBtn.classList.remove('playing');
                    });
                });
            }
        }

        // Interaction handlers
        if (q.type === 'multiple_choice') {
            this.bindMultipleChoice();
        } else if (q.type === 'word_order') {
            this.bindWordOrder();
        }
    }

    bindMultipleChoice() {
        const cards = document.querySelectorAll('.option-card');
        cards.forEach(card => {
            card.addEventListener('click', () => {
                if (this.state !== 'READY') return;
                SoundEffects.playTap();
                cards.forEach(c => c.classList.remove('selected'));
                card.classList.add('selected');
                this.selectedAnswer = card.getAttribute('data-val');

                // Enable submit button
                this.actionBtn.classList.remove('btn-disabled');
            });
        });
    }

    bindWordOrder() {
        const wordTiles = document.querySelectorAll('#word-bank .word-tile');

        wordTiles.forEach(tile => {
            tile.addEventListener('click', () => {
                if (this.state !== 'READY') return;
                const bankIdx = tile.getAttribute('data-bank-idx');
                const word = tile.getAttribute('data-word');

                SoundEffects.playTap();
                SpeechEngine.speak(word, 1.0);

                // Disable tile in bank
                tile.classList.add('in-bank-disabled');

                // Add to placed words
                const item = { id: Date.now() + Math.random(), word: word, bankIdx: bankIdx };
                this.placedWords.push(item);
                this.renderAssemblyZone();
            });
        });
    }

    renderAssemblyZone() {
        const assemblyZone = document.getElementById('assembly-zone');
        if (this.placedWords.length === 0) {
            assemblyZone.innerHTML = '<span class="assembly-placeholder" id="assembly-placeholder">Cümleyi oluşturmak için aşağıdaki kelimelere dokun</span>';
            this.selectedAnswer = null;
            this.actionBtn.classList.add('btn-disabled');
            return;
        }

        assemblyZone.innerHTML = '';
        this.placedWords.forEach((item, index) => {
            const placedChip = document.createElement('div');
            placedChip.className = 'word-tile placed';
            placedChip.textContent = item.word;
            placedChip.title = 'Kaldırmak için tıkla';

            placedChip.addEventListener('click', () => {
                if (this.state !== 'READY') return;
                SoundEffects.playTap();

                // Return to bank
                const originalTile = document.querySelector(`#word-bank .word-tile[data-bank-idx="${item.bankIdx}"]`);
                if (originalTile) {
                    originalTile.classList.remove('in-bank-disabled');
                }
                this.placedWords.splice(index, 1);
                this.renderAssemblyZone();
            });

            assemblyZone.appendChild(placedChip);
        });

        this.selectedAnswer = this.placedWords.map(p => p.word);
        this.actionBtn.classList.remove('btn-disabled');
    }

    async submitAnswer() {
        if (!this.selectedAnswer || this.state !== 'READY') return;
        this.state = 'CHECKING';
        this.totalAttempts++;

        const q = this.currentQuestion;
        const mascotEl = document.getElementById('question-mascot');

        try {
            const res = await fetch('/api/check-answer', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    question_id: q.id,
                    answer: this.selectedAnswer
                })
            });

            const result = await res.json();
            this.hearts = result.hearts;

            if (result.is_correct) {
                // CORRECT ANSWER
                this.state = 'CORRECT';
                this.correctCount++;
                SoundEffects.playCorrect();

                // Happy thumbs up Little Bear reaction
                if (mascotEl) {
                    mascotEl.src = '/static/images/mascot_cheer.svg';
                    mascotEl.className = 'prompt-mascot bear-react-cheer';
                }

                this.showCorrectFeedback(result.explanation);

                // Demo restriction check: if demo user correctly solved 3rd question (index 2)
                if (this.isDemo && this.currentIndex === 2) {
                    setTimeout(() => {
                        const demoModal = document.getElementById('demo-conversion-modal');
                        if (demoModal) {
                            SoundEffects.playComplete();
                            demoModal.classList.add('open');
                        }
                    }, 900);
                }

            } else {
                // INCORRECT ANSWER (Blocking retry mechanism)
                this.state = 'WRONG_RETRY';
                SoundEffects.playWrong();
                if (!this.isPremium) {
                    this.updateHeartsUI(true); // animate hearts loss only for non-premium
                }

                // Empathetic Little Bear reaction
                if (mascotEl) {
                    mascotEl.src = '/static/images/mascot_sad.svg';
                    mascotEl.className = 'prompt-mascot bear-react-sad';
                }

                // If out of hearts, halt test and trigger game over modal (never for premium)
                if (!this.isPremium && this.hearts <= 0) {
                    this.showIncorrectFeedback(result.correct_answer, result.explanation, true);
                    setTimeout(() => {
                        this.showOutOfHeartsModal();
                    }, 1100);
                } else {
                    this.showIncorrectFeedback(result.correct_answer, result.explanation, false);
                }
            }
        } catch (e) {
            console.error('Answer check error:', e);
            alert('Cevap kontrol edilirken bağlantı hatası oluştu.');
            this.state = 'READY';
        }
    }

    showCorrectFeedback(explanation) {
        this.footerEl.className = 'lesson-footer quiz-feedback-bar state-correct';
        const isDemoLock = (this.isDemo && this.currentIndex === 2);
        
        let explanationText = '';
        if (isDemoLock) {
            explanationText = '🎉 3 soruyu tamamladın! 4. soruya geçmek için Google ile giriş yapmalısın.';
        } else if (explanation) {
            explanationText = explanation;
        } else {
            explanationText = 'Doğru cevap! Bir sonraki soruya hazırsın.';
        }

        this.feedbackSectionEl.innerHTML = `
            <div class="feedback-icon-circle">
                <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#15803d" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="20 6 9 17 4 12"></polyline>
                </svg>
            </div>
            <div class="feedback-text-wrap">
                <div class="feedback-title">Harika!</div>
                <div class="feedback-explanation">${explanationText}</div>
            </div>
        `;
        this.actionBtn.textContent = isDemoLock ? '🔒 GİRİŞ YAP VE DEVAM ET' : 'DEVAM ET';
        this.actionBtn.className = isDemoLock ? 'btn-3d btn-blue' : 'btn-3d btn-emerald';
    }

    showIncorrectFeedback(correctAnswer, explanation, outOfHearts = false) {
        this.footerEl.className = 'lesson-footer quiz-feedback-bar state-incorrect';
        
        let errorHint = explanation || (correctAnswer ? `Doğru Çözüm: ${correctAnswer}` : 'Soruyu dikkatlice inceleyip tekrar dene.');

        this.feedbackSectionEl.innerHTML = `
            <div class="feedback-icon-circle">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#b91c1c" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="18" y1="6" x2="6" y2="18"></line>
                    <line x1="6" y1="6" x2="18" y2="18"></line>
                </svg>
            </div>
            <div class="feedback-text-wrap">
                <div class="feedback-title">Doğru Çözüm:</div>
                <div class="feedback-explanation">${errorHint}</div>
            </div>
        `;

        if (outOfHearts && !this.isPremium) {
            this.actionBtn.textContent = 'CANLARIN BİTTİ';
            this.actionBtn.className = 'btn-3d btn-disabled';
        } else {
            // "TEKRAR DENE" button (User cannot skip question without answering correctly)
            this.actionBtn.textContent = 'TEKRAR DENE';
            this.actionBtn.className = 'btn-3d btn-red';
        }
    }

    // Resets current question state for a retry without advancing currentIndex
    retryCurrentQuestion() {
        if (!this.isPremium && this.hearts <= 0) {
            this.showOutOfHeartsModal();
            return;
        }

        this.state = 'READY';
        this.selectedAnswer = null;

        // Reset mascot to cheerful
        const mascotEl = document.getElementById('question-mascot');
        if (mascotEl) {
            mascotEl.src = '/static/images/mascot_happy.svg';
            mascotEl.className = 'prompt-mascot';
        }

        // Reset footer to neutral
        this.footerEl.className = 'lesson-footer quiz-feedback-bar';
        this.feedbackSectionEl.innerHTML = '';
        this.actionBtn.textContent = 'KONTROL ET';
        this.actionBtn.className = 'btn-3d btn-blue btn-disabled';

        // Clear multiple-choice selection
        const cards = document.querySelectorAll('.option-card');
        cards.forEach(c => c.classList.remove('selected'));

        // Clear word-order slots and restore bank
        if (this.currentQuestion.type === 'word_order') {
            this.placedWords = [];
            this.renderAssemblyZone();
            const wordTiles = document.querySelectorAll('#word-bank .word-tile');
            wordTiles.forEach(t => t.classList.remove('in-bank-disabled'));
        }
    }

    // Only called when current question was answered correctly
    nextQuestion() {
        if (this.hearts <= 0) {
            this.showOutOfHeartsModal();
            return;
        }

        // Demo Restriction: Block transition to 4th question (index 3)
        if (this.isDemo && this.currentIndex >= 2) {
            SoundEffects.playComplete();
            const demoModal = document.getElementById('demo-conversion-modal');
            if (demoModal) {
                demoModal.classList.add('open');
            }
            return; // STRICTLY BLOCK MOVING TO QUESTION 4
        }

        this.currentIndex++; // ONLY advance on correct answer
        if (this.currentIndex < this.questions.length) {
            this.renderQuestion();
        } else {
            this.finishLesson();
        }
    }

    async finishLesson() {
        this.state = 'FINISHED';
        this.progressBar.style.width = '100%';
        SoundEffects.playComplete();
        launchConfetti();

        let xpGained = 20;
        try {
            const res = await fetch(`/api/lesson/${this.lessonId}/complete`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ score: 100 })
            });
            const data = await res.json();
            if (data.success) {
                xpGained = data.xp_gained;
                const newStreak = data.streak_count || data.streak || 1;
                const streakModalEl = document.getElementById('modal-streak-val');
                if (streakModalEl) streakModalEl.textContent = `🔥 ${newStreak}`;
                const topStreakEl = document.getElementById('lesson-streak-count');
                if (topStreakEl) topStreakEl.textContent = newStreak;
                const topStreakWrap = document.querySelector('.lesson-streak-display');
                if (topStreakWrap) {
                    topStreakWrap.classList.remove('streak-inactive');
                    topStreakWrap.classList.add('streak-active');
                    const flameEl = topStreakWrap.querySelector('.streak-flame');
                    if (flameEl) {
                        flameEl.classList.remove('streak-inactive');
                        flameEl.classList.add('streak-active');
                    }
                }
            }
        } catch (e) {
            console.error('Error saving lesson progress:', e);
        }

        const modal = document.getElementById('lesson-complete-modal');
        const xpEarnedEl = document.getElementById('modal-xp-earned');
        const accuracyEl = document.getElementById('modal-accuracy');

        if (xpEarnedEl) xpEarnedEl.textContent = `+${xpGained} XP`;
        if (accuracyEl) {
            const acc = Math.round((this.questions.length / Math.max(this.questions.length, this.totalAttempts)) * 100);
            accuracyEl.textContent = `%${acc}`;
        }

        modal.classList.add('open');
    }

    showOutOfHeartsModal() {
        const modal = document.getElementById('lesson-gameover-modal');
        if (modal) modal.classList.add('open');
    }
}

// Confetti Particle Canvas Animation
function launchConfetti() {
    const canvas = document.getElementById('confetti-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const colors = ['#0284c7', '#38bdf8', '#0ea5e9', '#f59e0b', '#10b981', '#ffd900', '#f43f5e'];
    const particles = [];

    for (let i = 0; i < 95; i++) {
        particles.push({
            x: canvas.width / 2,
            y: canvas.height / 2,
            r: Math.random() * 6 + 4,
            dx: (Math.random() - 0.5) * 14,
            dy: (Math.random() - 0.7) * 16,
            color: colors[Math.floor(Math.random() * colors.length)],
            tilt: Math.random() * 10,
            tiltAngle: 0,
            tiltAngleIncrement: Math.random() * 0.08 + 0.04
        });
    }

    let animationFrame;
    const startTime = Date.now();

    function render() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        particles.forEach(p => {
            p.tiltAngle += p.tiltAngleIncrement;
            p.y += (Math.cos(p.tiltAngle) + 3 + p.r / 2) / 2;
            p.x += p.dx * 0.5;
            p.tilt = Math.sin(p.tiltAngle) * 12;

            ctx.beginPath();
            ctx.lineWidth = p.r;
            ctx.strokeStyle = p.color;
            ctx.moveTo(p.x + p.tilt + p.r / 4, p.y);
            ctx.lineTo(p.x + p.tilt, p.y + p.tilt + p.r / 4);
            ctx.stroke();
        });

        if (Date.now() - startTime < 3500) {
            animationFrame = requestAnimationFrame(render);
        } else {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            cancelAnimationFrame(animationFrame);
        }
    }
    render();
}
