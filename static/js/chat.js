/**
 * YiğidoBear Interactive AI Chat Assistant (Client-Side Decision Tree)
 * PLUS Feature Integration • Free User Upgrade & Referral Invite Flow
 */

// 1. FREE USER DECISION TREE (PLUS'a Davet & Tanıtım & Demo Akışı)
const FREE_USER_TREE = {
    root: {
        yigido: "Merhaba! Ben YiğidoBear AI Sohbet Asistanı 🐻👑 Bu akıllı İngilizce pratik özelliği YiğidoBear PLUS üyelerine özeldir! Arkadaşlarını davet ederek veya PLUS'a geçerek sınırsız sohbet edebilirsin.",
        options: [
            { text: "🎁 1 Ay Ücretsiz PLUS Kazan (10 Davet)", next: "referral_info", action: "open_referral" },
            { text: "👑 PLUS Ayrıcalıkları Nelerdir?", next: "plus_benefits" },
            { text: "💬 1 Mesajlık Ücretsiz Deneme Yap", next: "demo_chat" }
        ]
    },

    plus_benefits: {
        yigido: "YiğidoBear PLUS Ayrıcalıkları: ⚡ Sınırsız Can, 🤖 Yapay Zeka Sohbet Asistanı, 🚫 Reklamsız Kesintisiz Deneyim ve 🏆 Özel Altın Profil Rozeti! 10 arkadaşını davet ederek 1 ay boyunca tamamen ücretsiz kullanabilirsin! 🌟",
        options: [
            { text: "🎁 Hemen Davet Linkimi Al (10 Davet)", next: "referral_info", action: "open_referral" },
            { text: "💬 İngilizce Demo Pratik Yap", next: "demo_chat" },
            { text: "👑 PLUS Avantajlarını İncele", next: "plus_modal_view", action: "open_plus_modal" }
        ]
    },

    referral_info: {
        yigido: "Harika bir karar! 🎁 Sana özel referans linkinle kayıt olan her arkadaşın için 1 davet kazanırsın. 10 davete ulaştığında 1 Ay Ücretsiz YiğidoBear PLUS anında hesabına tanımlanır!",
        options: [
            { text: "📋 Davet Linkini Aç & Kopyala", next: "referral_info", action: "open_referral" },
            { text: "💬 İngilizce Demo Konuşma Yap", next: "demo_chat" },
            { text: "👑 PLUS Ayrıcalıklarını Gör", next: "plus_benefits" }
        ]
    },

    demo_chat: {
        yigido: "Süper! İşte senin için kısa bir İngilizce pratik denemesi: 'Hi there! How are you doing today? 🐻'",
        options: [
            { text: "I am doing fantastic, thanks! 😊", next: "demo_reply_1" },
            { text: "I'm practicing English with you! 📖", next: "demo_reply_2" },
            { text: "What is your favorite hobby? 🎨", next: "demo_reply_3" }
        ]
    },

    demo_reply_1: {
        yigido: "That's wonderful to hear! 🌟 Konuşman gayet akıcı! İşte bunun gibi sınırsız İngilizce diyaloglar, deyimler ve fıkralar için PLUS seni bekliyor. 10 arkadaşını davet et, 1 ay ücretsiz PLUS ile kesintisiz sohbet et! 🚀",
        options: [
            { text: "🎁 Davet Et & 1 Ay Ücretsiz PLUS Kazan", next: "referral_info", action: "open_referral" },
            { text: "👑 PLUS Ayrıcalıklarını Gör", next: "plus_benefits" },
            { text: "🔄 Baştan Başlat", next: "root" }
        ]
    },

    demo_reply_2: {
        yigido: "Practicing English daily is the true secret to fluency! 🏆 YiğidoBear PLUS ile sınırsız can ve 7/24 AI asistan desteğiyle her gün pratik yapabilirsin. Arkadaşlarını davet et, hemen PLUS üyesi ol!",
        options: [
            { text: "🎁 Davet Et & 1 Ay Ücretsiz PLUS Kazan", next: "referral_info", action: "open_referral" },
            { text: "👑 PLUS Ayrıcalıklarını Gör", next: "plus_benefits" },
            { text: "🔄 Baştan Başlat", next: "root" }
        ]
    },

    demo_reply_3: {
        yigido: "I love eating sweet honey and helping bright learners like you! 🍯 Hobiler hakkında daha derin sohbet etmek ve İngilizce konuşma özgüvenini katlamak için PLUS'a davetlisin! 10 arkadaşını davet et, 1 ay ücretsiz kazan!",
        options: [
            { text: "🎁 Davet Et & 1 Ay Ücretsiz PLUS Kazan", next: "referral_info", action: "open_referral" },
            { text: "👑 PLUS Ayrıcalıklarını Gör", next: "plus_benefits" },
            { text: "🔄 Baştan Başlat", next: "root" }
        ]
    },

    plus_modal_view: {
        yigido: "YiğidoBear PLUS ile öğrenme hızını üçe katla! Sınırsız can sayesinde hata yapmaktan asla korkmazsın, AI asistanla dilediğince pratik yaparsın. 👑",
        options: [
            { text: "🎁 1 Ay Ücretsiz PLUS Al (10 Davet)", next: "referral_info", action: "open_referral" },
            { text: "💬 Demo Pratik Yap", next: "demo_chat" },
            { text: "🔄 Baştan Başlat", next: "root" }
        ]
    }
};

// 2. PLUS USER DECISION TREE (Tam ve Sınırsız İngilizce Diyalog Akışı)
const PLUS_USER_TREE = {
    root: {
        yigido: "Hi! Welcome back, PLUS member! 👑 How are you doing today? 🐻",
        options: [
            { text: "I am doing great, thanks! 😊", next: "doing_great" },
            { text: "I'm a bit tired today. 🥱", next: "tired" },
            { text: "What is your name? ❓", next: "ask_name" }
        ]
    },

    doing_great: {
        yigido: "That's awesome to hear! 🌟 Positive energy makes learning English so much easier! What would you like to talk about?",
        options: [
            { text: "Tell me about your hobbies! 🎨", next: "hobbies" },
            { text: "What is your favorite food? 🍕", next: "food" },
            { text: "Teach me a new English word! 📚", next: "new_word" }
        ]
    },

    tired: {
        yigido: "Oh, take it easy! A cup of warm tea or hot chocolate might help. ☕ Do you have a lot of work or studying today?",
        options: [
            { text: "Yes, I'm studying English hard! 📖", next: "study_hard" },
            { text: "Just resting for a while. 🛋️", next: "resting" },
            { text: "Tell me a funny joke to cheer me up! 😄", next: "joke" }
        ]
    },

    ask_name: {
        yigido: "I am Yiğido! Your cheerful bear friend and English learning companion. 🐻 What do you like to do in your free time?",
        options: [
            { text: "I love listening to music! 🎵", next: "music" },
            { text: "I enjoy playing video games! 🎮", next: "games" },
            { text: "I love reading books! 📚", next: "reading" }
        ]
    },

    hobbies: {
        yigido: "I love eating sweet honey 🍯, solving English quizzes with students, and hiking in green forests! What kind of sports do you like?",
        options: [
            { text: "I like playing soccer! ⚽", next: "sports_soccer" },
            { text: "I prefer swimming in the sea! 🏊", next: "sports_swim" },
            { text: "Can you teach me a useful idiom? 💡", next: "idiom" }
        ]
    },

    sports_soccer: {
        yigido: "Soccer is exciting! In British English it's called 'football', while in American English it's 'soccer'. Did you know that? ⚽",
        options: [
            { text: "Yes, I knew that! Cool fact! 🧠", next: "doing_great" },
            { text: "Tell me a funny bear joke! 😂", next: "joke" },
            { text: "Teach me a new English word! 📚", next: "new_word" }
        ]
    },

    sports_swim: {
        yigido: "Swimming is wonderful for the whole body! Just like bears catching fresh salmon in mountain streams! 🐟🌊",
        options: [
            { text: "Haha you bears are great swimmers! 🐻", next: "doing_great" },
            { text: "Teach me a useful idiom! 💡", next: "idiom" },
            { text: "What is your favorite food? 🍕", next: "food" }
        ]
    },

    food: {
        yigido: "Honey and fresh blueberries are my absolute favorite! 🍯 But I also love Turkish kebabs and baklava! Do you prefer sweet or savory food?",
        options: [
            { text: "I definitely have a sweet tooth! 🍰", next: "sweet_food" },
            { text: "I prefer savory meals like pizza! 🍕", next: "savory_food" },
            { text: "Let's talk about something else! 🔄", next: "menu" }
        ]
    },

    sweet_food: {
        yigido: "'To have a sweet tooth' means you crave sweets and desserts! You and I are officially dessert buddies now! 🍩🍯",
        options: [
            { text: "Yay, dessert buddies! Tell me a joke! 😂", next: "joke" },
            { text: "Can you teach me another idiom? 💡", next: "idiom" },
            { text: "Back to topics menu 🏠", next: "menu" }
        ]
    },

    savory_food: {
        yigido: "Mmm, warm pizza with melted cheese is irresistible! In English, when food is super tasty, we say it's 'scrumptious'! 🍕✨",
        options: [
            { text: "'Scrumptious' is a great word! 🌟", next: "new_word" },
            { text: "Tell me a joke while I get hungry! 😄", next: "joke" },
            { text: "Back to topics menu 🏠", next: "menu" }
        ]
    },

    new_word: {
        yigido: "Here is a magnificent word for today: 'Ebullient' (adjective) — It means cheerful, lively and full of positive energy! Just like you and me! 🌟",
        options: [
            { text: "That's fantastic! Give me another! ✨", next: "another_word" },
            { text: "Can you tell me an idiom too? 💡", next: "idiom" },
            { text: "Back to topics menu 🏠", next: "menu" }
        ]
    },

    another_word: {
        yigido: "Here is another beauty: 'Serendipity' (noun) — Finding something delightful without looking for it! Meeting you was true serendipity! 🍀",
        options: [
            { text: "Aww you are the sweetest bear! 🐻❤️", next: "thank_bear" },
            { text: "Tell me a funny joke! 😂", next: "joke" },
            { text: "Back to topics menu 🏠", next: "menu" }
        ]
    },

    joke: {
        yigido: "Why don't bears wear shoes? ... Because they already have bear feet (bare feet)! Haha! 🐾 Did that make you smile?",
        options: [
            { text: "Haha that was cute! 😂", next: "joke_laughed" },
            { text: "Bear puns are the best! 🐻", next: "joke_laughed" },
            { text: "Teach me a new English word! 📚", next: "new_word" }
        ]
    },

    joke_laughed: {
        yigido: "Yay! A laughing student is a happy student! Smiling actually helps your brain remember new vocabulary faster! 😄 What's next?",
        options: [
            { text: "Teach me a useful idiom! 💡", next: "idiom" },
            { text: "Tell me about your hobbies! 🎨", next: "hobbies" },
            { text: "I have to leave for now! 👋", next: "goodbye" }
        ]
    },

    study_hard: {
        yigido: "Consistency is your superpower! 🚀 Even 10 minutes of daily practice keeps your streak alive and builds real fluency. You are doing great!",
        options: [
            { text: "Thank you for encouraging me! 💪", next: "thank_bear" },
            { text: "Teach me an English idiom! 💡", next: "idiom" },
            { text: "Back to topics menu 🏠", next: "menu" }
        ]
    },

    resting: {
        yigido: "Rest is just as important as studying. Relax, take deep breaths, and whenever you want to learn, Yiğido is right here! 🍯",
        options: [
            { text: "Thanks Yiğido, you're the best! ☕", next: "thank_bear" },
            { text: "Tell me a funny joke! 😄", next: "joke" },
            { text: "Back to topics menu 🏠", next: "menu" }
        ]
    },

    music: {
        yigido: "Listening to English songs is an awesome way to practice! Singing along improves your pronunciation and rhythm naturally! 🎤🎶",
        options: [
            { text: "I will listen to English music today! 🎧", next: "thank_bear" },
            { text: "Teach me a cool idiom! 💡", next: "idiom" },
            { text: "Back to topics menu 🏠", next: "menu" }
        ]
    },

    games: {
        yigido: "Gaming in English is super effective! You learn real-time reactions and teamwork vocabulary while having a blast! 🎮✨",
        options: [
            { text: "Yes! Video games taught me so much! 🕹️", next: "thank_bear" },
            { text: "Teach me a new English word! 📚", next: "new_word" },
            { text: "Back to topics menu 🏠", next: "menu" }
        ]
    },

    reading: {
        yigido: "Reading expands your mind! Have you visited our '📚 Hikayeler (Stories)' library in the left menu? It has levels from A1 to B2! 📖",
        options: [
            { text: "Yes, I love the stories module! 🌟", next: "thank_bear" },
            { text: "I'll go read a story right now! 🚀", next: "goodbye" },
            { text: "Teach me a cool idiom first! 💡", next: "idiom" }
        ]
    },

    idiom: {
        yigido: "Here is a classic idiom: 'Piece of cake' 🍰 — It means something is very easy to do! Example: 'Speaking English with Yiğido is a piece of cake!'",
        options: [
            { text: "Haha love that idiom! Give me another! ✨", next: "idiom_2" },
            { text: "Tell me a joke! 😂", next: "joke" },
            { text: "Back to topics menu 🏠", next: "menu" }
        ]
    },

    idiom_2: {
        yigido: "Another one: 'Break a leg'! 🎭 It means 'Good luck!' before a test or show. Don't actually break any bones though! Haha!",
        options: [
            { text: "That's hilarious! Thanks Yiğido! 😄", next: "thank_bear" },
            { text: "Teach me a new word! 📚", next: "new_word" },
            { text: "Back to topics menu 🏠", next: "menu" }
        ]
    },

    thank_bear: {
        yigido: "Aww, you're amazing! Never forget that making mistakes is simply proof that you are trying and improving! Proud of you! 🐻❤️",
        options: [
            { text: "Let's explore something new! 🔄", next: "menu" },
            { text: "Tell me a funny joke! 😂", next: "joke" },
            { text: "I have to go for now, goodbye! 👋", next: "goodbye" }
        ]
    },

    goodbye: {
        yigido: "Goodbye for now! Have a wonderful day, protect your flame streak 🔥, and see you soon! Take care! 👋🐻",
        options: [
            { text: "Wait, let's chat a bit more! 😊", next: "root" },
            { text: "See you later, Yiğido! 🐻", next: "root" },
            { text: "Start over from beginning 🔄", next: "root" }
        ]
    },

    menu: {
        yigido: "What would you like to explore together? 🐻",
        options: [
            { text: "Teach me vocabulary & idioms 📚", next: "new_word" },
            { text: "Tell me a funny bear joke 😄", next: "joke" },
            { text: "Chat about hobbies & free time 🎨", next: "hobbies" }
        ]
    }
};

let currentChatNode = "root";
let isChatOpen = false;
let isYigidoTyping = false;

// Get Active Tree depending on user's PLUS status
function getActiveTree() {
    const isPremium = (typeof window.IS_USER_PREMIUM !== 'undefined') ? Boolean(window.IS_USER_PREMIUM) : false;
    return isPremium ? PLUS_USER_TREE : FREE_USER_TREE;
}

// Audio speech synthesis helper
function speakChatText(text, btnElement) {
    if (typeof SoundEffects !== 'undefined' && SoundEffects.playTap) {
        SoundEffects.playTap();
    }
    if (btnElement) {
        btnElement.classList.add('speaking');
    }

    // Clean emojis for speech
    const cleanText = text.replace(/[\u{1F300}-\u{1FAFF}]/gu, '').trim();

    if (typeof SpeechEngine !== 'undefined' && SpeechEngine.speak) {
        SpeechEngine.speak(cleanText, 0.95, () => {
            if (btnElement) btnElement.classList.remove('speaking');
        });
    } else if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(cleanText);
        utterance.lang = 'en-US';
        utterance.rate = 0.95;
        utterance.pitch = 1.08;
        utterance.onend = () => {
            if (btnElement) btnElement.classList.remove('speaking');
        };
        utterance.onerror = () => {
            if (btnElement) btnElement.classList.remove('speaking');
        };
        window.speechSynthesis.speak(utterance);
    } else {
        if (btnElement) btnElement.classList.remove('speaking');
    }
}

// Toggle Widget Visibility
function toggleChatWidget(forceState) {
    const widget = document.getElementById('chat-widget-window');
    const launcher = document.getElementById('chat-launcher-btn');
    const tooltip = document.getElementById('chat-launcher-tooltip');
    if (!widget) return;

    if (typeof forceState === 'boolean') {
        isChatOpen = forceState;
    } else {
        isChatOpen = !isChatOpen;
    }

    if (isChatOpen) {
        widget.classList.add('open');
        widget.setAttribute('aria-hidden', 'false');
        if (launcher) launcher.classList.add('chat-active');
        if (tooltip) tooltip.style.display = 'none';

        if (typeof SoundEffects !== 'undefined' && SoundEffects.playTap) {
            SoundEffects.playTap();
        }

        // If conversation is empty, start with root
        const messagesContainer = document.getElementById('chat-messages-container');
        if (messagesContainer && messagesContainer.children.length === 0) {
            const activeTree = getActiveTree();
            renderYigidoMessage(activeTree.root.yigido, activeTree.root.options);
        } else {
            scrollChatToBottom();
        }
    } else {
        widget.classList.remove('open');
        widget.setAttribute('aria-hidden', 'true');
        if (launcher) launcher.classList.remove('chat-active');
        if (tooltip) tooltip.style.display = '';

        if (typeof SoundEffects !== 'undefined' && SoundEffects.playTap) {
            SoundEffects.playTap();
        }
    }
}

// Append User Bubble
function renderUserMessage(text) {
    const container = document.getElementById('chat-messages-container');
    if (!container) return;

    const msgRow = document.createElement('div');
    msgRow.className = 'chat-message-row user-row';

    const bubble = document.createElement('div');
    bubble.className = 'chat-bubble user-bubble';
    bubble.textContent = text;

    msgRow.appendChild(bubble);
    container.appendChild(msgRow);
    scrollChatToBottom();
}

// Append Yiğido Bubble with Speaker and Avatar
function renderYigidoMessage(text, options) {
    const container = document.getElementById('chat-messages-container');
    if (!container) return;

    const msgRow = document.createElement('div');
    msgRow.className = 'chat-message-row yigido-row';

    // Avatar
    const avatar = document.createElement('div');
    avatar.className = 'chat-avatar-small';
    const img = document.createElement('img');
    img.src = '/static/images/mascot_happy.svg';
    img.alt = 'Yiğido';
    avatar.appendChild(img);
    msgRow.appendChild(avatar);

    // Bubble Wrap
    const bubbleWrap = document.createElement('div');
    bubbleWrap.className = 'chat-bubble-wrap';

    const senderTag = document.createElement('span');
    senderTag.className = 'chat-sender-tag';
    senderTag.textContent = 'YiğidoBear AI';
    bubbleWrap.appendChild(senderTag);

    const bubble = document.createElement('div');
    bubble.className = 'chat-bubble yigido-bubble';

    const textSpan = document.createElement('span');
    textSpan.className = 'chat-text';
    textSpan.textContent = text;
    bubble.appendChild(textSpan);

    // Audio Speaker Icon
    const speakBtn = document.createElement('button');
    speakBtn.type = 'button';
    speakBtn.className = 'chat-bubble-speaker';
    speakBtn.title = 'İngilizce Telaffuzu Dinle';
    speakBtn.innerHTML = `
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round">
            <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon>
            <path d="M15.54 8.46a5 5 0 0 1 0 7.07"></path>
            <path d="M19.07 4.93a10 10 0 0 1 0 14.14"></path>
        </svg>
    `;
    speakBtn.onclick = function() {
        speakChatText(text, this);
    };
    bubble.appendChild(speakBtn);

    bubbleWrap.appendChild(bubble);
    msgRow.appendChild(bubbleWrap);

    container.appendChild(msgRow);
    scrollChatToBottom();

    // Render Options
    renderOptionButtons(options);
}

// Show Typing Indicator
function showTypingIndicator() {
    const container = document.getElementById('chat-messages-container');
    if (!container) return null;

    const typingRow = document.createElement('div');
    typingRow.className = 'chat-message-row yigido-row typing-row';
    typingRow.id = 'chat-typing-row';

    const avatar = document.createElement('div');
    avatar.className = 'chat-avatar-small';
    const img = document.createElement('img');
    img.src = '/static/images/mascot_happy.svg';
    img.alt = 'Yiğido';
    avatar.appendChild(img);
    typingRow.appendChild(avatar);

    const typingBubble = document.createElement('div');
    typingBubble.className = 'chat-typing-bubble';
    typingBubble.innerHTML = '<span></span><span></span><span></span>';
    typingRow.appendChild(typingBubble);

    container.appendChild(typingRow);
    scrollChatToBottom();
    return typingRow;
}

function removeTypingIndicator() {
    const el = document.getElementById('chat-typing-row');
    if (el) el.remove();
}

// Render 3 Option Buttons
function renderOptionButtons(options) {
    const tray = document.getElementById('chat-options-tray');
    if (!tray) return;

    tray.innerHTML = '';
    if (!options || options.length === 0) return;

    options.forEach((opt, idx) => {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'chat-option-btn';
        
        // Highlight referral or plus options
        if (opt.action === 'open_referral' || opt.text.includes('PLUS')) {
            btn.classList.add('chat-opt-plus-promo');
        }

        btn.innerHTML = `<span class="opt-bullet">${idx + 1}</span> <span class="opt-text">${opt.text}</span>`;
        btn.onclick = () => selectChatOption(opt.text, opt.next, opt.action);
        tray.appendChild(btn);
    });
}

// Handle User Option Click
function selectChatOption(text, nextNodeKey, action) {
    if (isYigidoTyping) return;
    isYigidoTyping = true;

    // Play tap sound
    if (typeof SoundEffects !== 'undefined' && SoundEffects.playTap) {
        SoundEffects.playTap();
    }

    // If option has action like open_referral or open_plus_modal
    if (action === 'open_referral') {
        if (typeof openReferralModal === 'function') {
            setTimeout(() => {
                openReferralModal();
            }, 300);
        }
    } else if (action === 'open_plus_modal') {
        if (typeof openPlusModal === 'function') {
            setTimeout(() => {
                openPlusModal();
            }, 300);
        }
    }

    // Disable option buttons during transition
    const tray = document.getElementById('chat-options-tray');
    if (tray) {
        tray.querySelectorAll('.chat-option-btn').forEach(b => {
            b.disabled = true;
            b.classList.add('disabled');
        });
    }

    // 1. Add User Message
    renderUserMessage(text);

    // 2. Show Typing Indicator
    showTypingIndicator();

    // 3. After short delay, respond as Yiğido
    setTimeout(() => {
        removeTypingIndicator();
        isYigidoTyping = false;

        const activeTree = getActiveTree();
        const nextNode = activeTree[nextNodeKey] || activeTree.root;
        currentChatNode = nextNodeKey;

        // Play message sound
        if (typeof SoundEffects !== 'undefined' && SoundEffects.playCorrect) {
            SoundEffects.playCorrect();
        }

        renderYigidoMessage(nextNode.yigido, nextNode.options);
    }, 450);
}

// Reset Conversation
function resetChatConversation() {
    if (typeof SoundEffects !== 'undefined' && SoundEffects.playTap) {
        SoundEffects.playTap();
    }
    const container = document.getElementById('chat-messages-container');
    if (container) container.innerHTML = '';

    currentChatNode = "root";
    const activeTree = getActiveTree();
    renderYigidoMessage(activeTree.root.yigido, activeTree.root.options);
}

// Auto Scroll to Bottom
function scrollChatToBottom() {
    const container = document.getElementById('chat-messages-container');
    if (container) {
        setTimeout(() => {
            container.scrollTop = container.scrollHeight;
        }, 40);
    }
}
