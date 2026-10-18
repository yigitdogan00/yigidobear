# -*- coding: utf-8 -*-
"""
YiğidoBear - Curriculum Data
Unit 1: 7 Core Topics (70 Authentic CEFR A1 Sentences) + 6 Assessment Exams (60 Questions)
Total: Exactly 13 Steps, 130 Questions.
Every sentence and question is pedagogically verified for natural native English usage,
authentic grammar distractors, zero text leaks, and Duolingo-style listening challenges.
"""

CURRICULUM_STEPS = [
    {
        'title': 'Konu 1: Selamlaşma & Temel Nezaket',
        'description': 'Günlük hayatta en sık kullanılan doğal selamlaşma ve nezaket kalıpları.',
        'is_exam': 0, 'difficulty': 1, 'icon': '👋', 'xp': 15, 'order': 1,
        'questions': [
            (
                'multiple_choice',
                '"How are you doing?" ifadesinin en doğal Türkçe karşılığı nedir?',
                'How are you doing?',
                'How are you doing?',
                ['Nasıl gidiyor, nasılsın?', 'Şu anda ne yapıyorsun?', 'Nereye gidiyorsun?', 'Bunu nasıl yapıyorsun?'],
                'Nasıl gidiyor, nasılsın?',
                '"How are you doing?" anadili İngilizce olanların en sık kullandığı samimi bir selamlaşmadır ("Nasılsın / Nasıl gidiyor?"). "What are you doing?" (Ne yapıyorsun?) ile karıştırılmamalıdır.'
            ),
            (
                'word_order',
                'Dinle ve cümleyi kur:',
                '',
                'I am doing well thank you',
                ['I', 'am', 'doing', 'well', 'thank', 'you', 'is', 'good'],
                ['I', 'am', 'doing', 'well', 'thank', 'you'],
                '"I am doing well, thank you." = İyiyim, teşekkür ederim.'
            ),
            (
                'multiple_choice',
                '"Nice to meet you!" ifadesinin Türkçe karşılığı hangisidir?',
                'Nice to meet you!',
                'Nice to meet you!',
                ['Tanıştığımıza memnun oldum!', 'Kendine iyi bak!', 'Lütfen içeri buyrun.', 'Sonra görüşürüz, hoşça kal.'],
                'Tanıştığımıza memnun oldum!',
                '"Nice to meet you!" ilk tanışmalarda "Tanıştığımıza memnun oldum!" anlamında standart ve zarif bir kalıptır.'
            ),
            (
                'word_order',
                'Dinle ve cümleyi kur:',
                '',
                'Nice to meet you',
                ['Nice', 'to', 'meet', 'you', 'for', 'meeting'],
                ['Nice', 'to', 'meet', 'you'],
                '"Nice to meet you" = Tanıştığıma memnun oldum.'
            ),
            (
                'multiple_choice',
                '"Have a nice day!" ifadesinin Türkçe karşılığı hangisidir?',
                'Have a nice day!',
                'Have a nice day!',
                ['İyi günler dilerim!', 'Günaydın!', 'İyi akşamlar!', 'Eve hoş geldin!'],
                'İyi günler dilerim!',
                '"Have a nice day!" ayrılırken "İyi günler dilerim!" anlamında kullanılır.'
            ),
            (
                'word_order',
                'Dinle ve cümleyi kur:',
                '',
                'See you later goodbye',
                ['See', 'you', 'later', 'goodbye', 'look', 'soon'],
                ['See', 'you', 'later', 'goodbye'],
                '"See you later, goodbye" = Sonra görüşürüz, hoşça kal.'
            ),
            (
                'multiple_choice',
                '"Good morning" ve "Good night" ifadeleri sırasıyla hangi durumlarda kullanılır?',
                'Good morning / Good night',
                'Good morning and Good night',
                ['Sabah selamlarken - Gece yatarken veya ayrılırken', 'Öğle yemeğinde - Sabah uyanınca', 'İlk tanışmada - Akşam üzeri', 'İkindi çayında - Akşam yemeğinde'],
                'Sabah selamlarken - Gece yatarken veya ayrılırken',
                '"Good morning" sabah karşılaştığınızda; "Good night" ise gece yatmadan önce veya gece ayrılırken söylenir.'
            ),
            (
                'word_order',
                'Dinle ve cümleyi kur:',
                '',
                'Excuse me can you help me',
                ['Excuse', 'me', 'can', 'you', 'help', 'me', 'please', 'do'],
                ['Excuse', 'me', 'can', 'you', 'help', 'me'],
                '"Excuse me, can you help me?" = Afedersiniz, bana yardım edebilir misiniz?'
            ),
            (
                'multiple_choice',
                'Biri size "Thank you so much!" dediğinde verilecek en doğal karşılık hangisidir?',
                'Thank you so much!',
                'Thank you so much!',
                ["You're welcome!", 'No, thank you.', 'Yes, please.', 'Excuse me.'],
                "You're welcome!",
                'Teşekkür edildiğinde "Rica ederim / Bir şey değil" demek için "You\'re welcome!" kullanılır.'
            ),
            (
                'word_order',
                'Dinle ve cümleyi kur:',
                '',
                'Take care see you soon',
                ['Take', 'care', 'see', 'you', 'soon', 'careful', 'look'],
                ['Take', 'care', 'see', 'you', 'soon'],
                '"Take care, see you soon" = Kendine iyi bak, yakında görüşürüz.'
            ),
        ]
    },
    {
        'title': 'Konu 2: Kendini Tanıtma & Nereli Olduğunu Söyleme',
        'description': 'Adını, nereli olduğunu, yaşadığın şehri ve dilleri doğal şekilde anlat.',
        'is_exam': 0, 'difficulty': 2, 'icon': '🌍', 'xp': 15, 'order': 2,
        'questions': [
            (
                'word_order',
                'Dinle ve cümleyi kur:',
                '',
                'My name is Sarah',
                ['My', 'name', 'is', 'Sarah', 'are', 'am'],
                ['My', 'name', 'is', 'Sarah'],
                '"My name is Sarah" = Benim adım Sarah.'
            ),
            (
                'multiple_choice',
                'Boşluğa hangisi gelmelidir? "Where ___ you from?"',
                'Where ___ you from?',
                '',
                ['are', 'is', 'do', 'come'],
                'are',
                '"Where are you from?" standart nerelisin sorusudur. "you" öznesiyle "to be" fiilinin "are" çekimi kullanılır.'
            ),
            (
                'word_order',
                'Dinle ve cümleyi kur:',
                '',
                'I am from Turkey',
                ['I', 'am', 'from', 'Turkey', 'is', 'in'],
                ['I', 'am', 'from', 'Turkey'],
                '"I am from Turkey" = Ben Türkiye\'denim. Ülke / köken belirtirken "from" kullanılır.'
            ),
            (
                'multiple_choice',
                '"I live in Istanbul." cümlesinin doğru anlamı hangisidir?',
                'I live in Istanbul.',
                'I live in Istanbul.',
                ["İstanbul'da yaşıyorum.", "İstanbul'a gidiyorum.", "İstanbul'dan geliyorum.", "İstanbul'u özlüyorum."],
                "İstanbul'da yaşıyorum.",
                '"live in" bir şehirde veya ülkede ikamet etmek, yaşamak anlamına gelir.'
            ),
            (
                'word_order',
                'Dinle ve cümleyi kur:',
                '',
                'Do you speak English',
                ['Do', 'you', 'speak', 'English', 'are', 'speaks'],
                ['Do', 'you', 'speak', 'English'],
                '"Do you speak English?" = İngilizce konuşuyor musun / biliyor musun?'
            ),
            (
                'multiple_choice',
                'Boşluğa hangisi gelmelidir? "Yes, I speak a ___ English."',
                'Yes, I speak a ___ English.',
                '',
                ['little', 'few', 'small', 'short'],
                'little',
                'Diller sayılamayan kavramlar olduğu için "biraz İngilizce" derken "a little English" kullanılır; "few" sayılabilenlerle kullanılır.'
            ),
            (
                'word_order',
                'Dinle ve cümleyi kur:',
                '',
                'How old are you',
                ['How', 'old', 'are', 'you', 'years', 'is'],
                ['How', 'old', 'are', 'you'],
                '"How old are you?" = Kaç yaşındasın? Yaş sorulurken "How old" kalıbı kullanılır.'
            ),
            (
                'multiple_choice',
                '"I am twenty-five years old." cümlesinde yaş hangi yardımcı fiille ifade edilmiştir?',
                'I am twenty-five years old.',
                'I am twenty-five years old.',
                ['am (to be fiili)', 'have (sahip olmak)', 'do', 'make'],
                'am (to be fiili)',
                'İngilizcede yaş belirtirken "have" değil, "to be" (am/is/are) kullanılır: "I am 25 years old".'
            ),
            (
                'word_order',
                'Dinle ve cümleyi kur:',
                '',
                'I am a student here',
                ['I', 'am', 'a', 'student', 'here', 'an', 'study'],
                ['I', 'am', 'a', 'student', 'here'],
                '"I am a student here" = Ben burada bir öğrenciyim. Meslek veya statü tekil olduğunda "a/an" kullanılır.'
            ),
            (
                'multiple_choice',
                '"Nice to meet you, I am Alex." diyen birine en doğal karşılık hangisidir?',
                'Nice to meet you, I am Alex.',
                'Nice to meet you, I am Alex.',
                ['Nice to meet you too, Alex!', 'No problem at all.', 'I am from Canada.', 'Goodbye, see you.'],
                'Nice to meet you too, Alex!',
                '"Nice to meet you" diyen birine "Ben de tanıştığıma memnun oldum" demek için cümlenin sonuna "too" (de/da) eklenir.'
            ),
        ]
    },
    {
        'title': '🏆 Test 1: Ara Değerlendirme 1',
        'description': 'Selamlaşma, tanışma ve kendini tanıtma konularındaki ustalığını test et.',
        'is_exam': 1, 'difficulty': 2, 'icon': '🏆', 'xp': 25, 'order': 3,
        'questions': [
            (
                'multiple_choice',
                'Hangisi resmi ve nazik bir şekilde "Afedersiniz" demek için kullanılır?',
                'Afedersiniz',
                '',
                ['Excuse me', 'Look at me', 'I am sorry to hear that', 'Take it easy'],
                'Excuse me',
                'Birinin dikkatini çekmek veya izin istemek için "Excuse me" (Afedersiniz) denir.'
            ),
            (
                'word_order',
                'Dinle ve cümleyi kur:',
                '',
                'Where are you from',
                ['Where', 'are', 'you', 'from', 'do', 'is'],
                ['Where', 'are', 'you', 'from'],
                '"Where are you from?" = Nerelisin?'
            ),
            (
                'multiple_choice',
                'Diyaloğu tamamla: "___" - "I am doing great, thank you!"',
                'Diyaloğu tamamla:',
                '',
                ['How are you doing?', 'Where do you work?', 'What is this?', 'Who are you?'],
                'How are you doing?',
                '"I am doing great, thank you!" (Harikayım, teşekkürler!) cevabı "How are you doing?" sorusuna verilir.'
            ),
            (
                'word_order',
                'Dinle ve cümleyi kur:',
                '',
                'I speak a little English',
                ['I', 'speak', 'a', 'little', 'English', 'speaks', 'few'],
                ['I', 'speak', 'a', 'little', 'English'],
                '"I speak a little English" = Biraz İngilizce konuşuyorum.'
            ),
            (
                'multiple_choice',
                'Boşluğa hangisi gelmelidir? "She is ___ England, but she lives ___ Germany."',
                'She is ___ England, but she lives ___ Germany.',
                '',
                ['from / in', 'in / from', 'at / on', 'to / at'],
                'from / in',
                'Köken / memleket için "from" (from England), yaşanan yer için "in" (lives in Germany) kullanılır.'
            ),
            (
                'word_order',
                'Dinle ve cümleyi kur:',
                '',
                'Have a nice day',
                ['Have', 'a', 'nice', 'day', 'good', 'time'],
                ['Have', 'a', 'nice', 'day'],
                '"Have a nice day" = İyi günler dilerim.'
            ),
            (
                'multiple_choice',
                'Hangisi İngilizcede "Hoş geldiniz!" anlamına gelir?',
                'Hoş geldiniz!',
                '',
                ['Welcome!', 'Goodbye!', 'Please!', 'Thank you!'],
                'Welcome!',
                '"Welcome!" = Hoş geldiniz!'
            ),
            (
                'word_order',
                'Dinle ve cümleyi kur:',
                '',
                'I live in Istanbul',
                ['I', 'live', 'in', 'Istanbul', 'at', 'on'],
                ['I', 'live', 'in', 'Istanbul'],
                '"I live in Istanbul" = İstanbul\'da yaşıyorum.'
            ),
            (
                'multiple_choice',
                '"Take care, see you soon!" ifadesini söyleyen biri ne amaçlamaktadır?',
                'Take care, see you soon!',
                'Take care, see you soon!',
                ['Dostça vedalaşmak ve iyi dilek iletmek', 'Özür dilemek', 'Yemek siparişi vermek', 'Yardım istemek'],
                'Dostça vedalaşmak ve iyi dilek iletmek',
                '"Take care, see you soon!" = Kendine iyi bak, yakında görüşürüz! Sevgi dolu bir vedalaşmadır.'
            ),
            (
                'word_order',
                'Dinle ve cümleyi kur:',
                '',
                'You are welcome',
                ['You', 'are', 'welcome', 'is', 'welcomes'],
                ['You', 'are', 'welcome'],
                '"You are welcome" = Rica ederim / Bir şey değil.'
            ),
        ]
    },
    {
        'title': 'Konu 3: Günlük Hayat & Temel İhtiyaçlar',
        'description': 'Kafede sipariş ver, hesap iste, soru sor ve temel ihtiyaçlarını belirt.',
        'is_exam': 0, 'difficulty': 2, 'icon': '☕', 'xp': 15, 'order': 4,
        'questions': [
            (
                'multiple_choice',
                'Kafede nazikçe sipariş verirken "Bir fincan kahve alabilir miyim, lütfen?" demek için hangisi en doğaldır?',
                'Bir fincan kahve alabilir miyim, lütfen?',
                '',
                ['I would like a cup of coffee, please.', 'Give me coffee right now.', 'I want drink coffee.', 'Coffee is mine please.'],
                'I would like a cup of coffee, please.',
                '"I would like..." (kısaca I\'d like) sipariş verirken en kibar ve yaygın kalıptır.'
            ),
            (
                'word_order',
                'Dinle ve cümleyi kur:',
                '',
                'I would like some water please',
                ['I', 'would', 'like', 'some', 'water', 'please', 'want', 'a'],
                ['I', 'would', 'like', 'some', 'water', 'please'],
                '"I would like some water, please" = Biraz su rica edebilir miyim, lütfen?'
            ),
            (
                'multiple_choice',
                'Restoranda yemek bitince hesabı istemek için hangi kalıp kullanılır?',
                'Hesabı alabilir miyim, lütfen?',
                '',
                ['Can I have the bill, please?', 'Where is the kitchen?', 'I want more menu please.', 'How is the food today?'],
                'Can I have the bill, please?',
                '"Can I have the bill, please?" restoranlarda hesabı istemek için standart ve kibar ifadedir.'
            ),
            (
                'word_order',
                'Dinle ve cümleyi kur:',
                '',
                'Where is the nearest supermarket',
                ['Where', 'is', 'the', 'nearest', 'supermarket', 'there', 'near'],
                ['Where', 'is', 'the', 'nearest', 'supermarket'],
                '"Where is the nearest supermarket?" = En yakın süpermarket nerede?'
            ),
            (
                'multiple_choice',
                'Bir mağazada fiyat sorarken "Bu gömlek ne kadar?" nasıl söylenir?',
                'Bu gömlek ne kadar?',
                '',
                ['How much is this shirt?', 'How many is this shirt?', 'How price is this shirt?', 'How money is this shirt?'],
                'How much is this shirt?',
                'Fiyat sorarken daima "How much" kullanılır; "How many" sayılabilen adetleri sormak içindir.'
            ),
            (
                'word_order',
                'Dinle ve cümleyi kur:',
                '',
                'Do you accept credit cards',
                ['Do', 'you', 'accept', 'credit', 'cards', 'are', 'card'],
                ['Do', 'you', 'accept', 'credit', 'cards'],
                '"Do you accept credit cards?" = Kredi kartı kabul ediyor musunuz?'
            ),
            (
                'multiple_choice',
                '"The bathroom is on the right." cümlesi ne bildirir?',
                'The bathroom is on the right.',
                'The bathroom is on the right.',
                ['Tuvalet sağ taraftadır.', 'Tuvalet sol taraftadır.', 'Banyo meşguldür.', 'Tuvalet kapalıdır.'],
                'Tuvalet sağ taraftadır.',
                '"on the right" = sağ tarafta demektir.'
            ),
            (
                'word_order',
                'Dinle ve cümleyi kur:',
                '',
                'I am hungry let us eat',
                ['I', 'am', 'hungry', 'let', 'us', 'eat', 'have', 'food'],
                ['I', 'am', 'hungry', 'let', 'us', 'eat'],
                '"I am hungry, let us eat" (I\'m hungry, let\'s eat) = Acıktım, hadi yemek yiyelim.'
            ),
            (
                'multiple_choice',
                'Söylenen bir şeyi anlamadığınızda tekrar rica etmek için hangisi en uygundur?',
                'Anlamadım, tekrar edebilir misiniz?',
                '',
                ['I do not understand, can you repeat please?', 'What are you doing now?', 'Speak no English please.', 'I am not listening to you.'],
                'I do not understand, can you repeat please?',
                '"I do not understand, can you repeat please?" = Anlamadım, lütfen tekrar edebilir misiniz?'
            ),
            (
                'word_order',
                'Dinle ve cümleyi kur:',
                '',
                'This coffee is very hot',
                ['This', 'coffee', 'is', 'very', 'hot', 'are', 'cold'],
                ['This', 'coffee', 'is', 'very', 'hot'],
                '"This coffee is very hot" = Bu kahve çok sıcak.'
            ),
        ]
    },
    {
        'title': 'Konu 4: Sayılar, Saatler & Zaman',
        'description': 'Saati sor, zamanı söyle, randevu planla ve günleri öğren.',
        'is_exam': 0, 'difficulty': 2, 'icon': '⏰', 'xp': 15, 'order': 5,
        'questions': [
            (
                'multiple_choice',
                '"What time is it now?" sorusuna en uygun cevap hangisidir?',
                'What time is it now?',
                'What time is it now?',
                ['It is half past two.', 'Today is Monday.', 'I am fine, thanks.', 'At the station.'],
                'It is half past two.',
                '"What time is it?" saat kaç sorusudur; "It is half past two" (Saat iki buçuk) buna karşılık gelir.'
            ),
            (
                'word_order',
                'Dinle ve cümleyi kur:',
                '',
                'What time is it now',
                ['What', 'time', 'is', 'it', 'now', 'are', 'hour'],
                ['What', 'time', 'is', 'it', 'now'],
                '"What time is it now?" = Şu an saat kaç?'
            ),
            (
                'multiple_choice',
                '"It is ten o\'clock in the morning." saat kaçı belirtir?',
                "It is ten o'clock in the morning.",
                "It is ten o'clock in the morning.",
                ['Sabah saat 10:00', 'Gece saat 22:00', 'Öğleden sonra 14:00', 'Sabah saat 08:30'],
                'Sabah saat 10:00',
                '"ten o\'clock in the morning" = sabah saat tam 10 demektir.'
            ),
            (
                'word_order',
                'Dinle ve cümleyi kur:',
                '',
                'The train leaves at five',
                ['The', 'train', 'leaves', 'at', 'five', 'in', 'on'],
                ['The', 'train', 'leaves', 'at', 'five'],
                '"The train leaves at five" = Tren saat beşte kalkıyor. Saatlerden önce "at" edatı kullanılır.'
            ),
            (
                'multiple_choice',
                'Boşluğa hangisi gelmelidir? "The meeting is ___ Friday afternoon."',
                'The meeting is ___ Friday afternoon.',
                '',
                ['on', 'at', 'in', 'to'],
                'on',
                'Günlerle ve belirli gün zamanlarıyla (Friday afternoon) daima "on" edatı kullanılır.'
            ),
            (
                'word_order',
                'Dinle ve cümleyi kur:',
                '',
                'I have thirty minutes left',
                ['I', 'have', 'thirty', 'minutes', 'left', 'am', 'time'],
                ['I', 'have', 'thirty', 'minutes', 'left'],
                '"I have thirty minutes left" = Otuz dakikam kaldı.'
            ),
            (
                'multiple_choice',
                '"There are sixty seconds in a minute." cümlesinin anlamı nedir?',
                'There are sixty seconds in a minute.',
                'There are sixty seconds in a minute.',
                ['Bir dakikada altmış saniye vardır.', 'Bir saatte altmış dakika vardır.', 'Günde yirmi dört saat vardır.', 'Haftada yedi gün vardır.'],
                'Bir dakikada altmış saniye vardır.',
                '"sixty seconds" = altmış saniye, "in a minute" = bir dakikada.'
            ),
            (
                'word_order',
                'Dinle ve cümleyi kur:',
                '',
                'See you on Friday afternoon',
                ['See', 'you', 'on', 'Friday', 'afternoon', 'at', 'in'],
                ['See', 'you', 'on', 'Friday', 'afternoon'],
                '"See you on Friday afternoon" = Cuma öğleden sonra görüşürüz.'
            ),
            (
                'multiple_choice',
                'Boşluğa hangisi gelmelidir? "I work from nine ___ five every day."',
                'I work from nine ___ five every day.',
                '',
                ['to', 'until', 'at', 'for'],
                'to',
                '"from ... to ..." bir başlangıç ve bitiş aralığını (dokuzdan beşe kadar) ifade eden standart kalıptır.'
            ),
            (
                'word_order',
                'Dinle ve cümleyi kur:',
                '',
                'I work from nine to five',
                ['I', 'work', 'from', 'nine', 'to', 'five', 'at', 'on'],
                ['I', 'work', 'from', 'nine', 'to', 'five'],
                '"I work from nine to five" = Dokuzdan beşe kadar çalışıyorum.'
            ),
        ]
    },
    {
        'title': '🏆 Test 2: Ara Değerlendirme 2',
        'description': 'Alışveriş, sipariş verme, saatler ve zaman edatları sınavı.',
        'is_exam': 1, 'difficulty': 2, 'icon': '🏆', 'xp': 25, 'order': 6,
        'questions': [
            (
                'multiple_choice',
                'Boşluğa hangisi gelmelidir? "Excuse me, how ___ are these apples?"',
                'Excuse me, how ___ are these apples?',
                '',
                ['much', 'many', 'price', 'cost'],
                'much',
                'Fiyat sorarken nesne çoğul da olsa kalıp "How much"tır: "How much are these apples?"'
            ),
            (
                'word_order',
                'Dinle ve cümleyi kur:',
                '',
                'Can I have the bill please',
                ['Can', 'I', 'have', 'the', 'bill', 'please', 'give', 'me'],
                ['Can', 'I', 'have', 'the', 'bill', 'please'],
                '"Can I have the bill, please?" = Hesabı alabilir miyim, lütfen?'
            ),
            (
                'multiple_choice',
                'Zaman edatlarını doğru eşleştir: "___ 8:00 AM", "___ Monday", "___ the morning"',
                'Zaman edatları',
                '',
                ['at / on / in', 'in / at / on', 'on / in / at', 'at / in / on'],
                'at / on / in',
                'Saatlerle "at" (at 8:00), günlerle "on" (on Monday), günün bölümleriyle "in" (in the morning) kullanılır.'
            ),
            (
                'word_order',
                'Dinle ve cümleyi kur:',
                '',
                'I would like a cup of coffee',
                ['I', 'would', 'like', 'a', 'cup', 'of', 'coffee', 'want'],
                ['I', 'would', 'like', 'a', 'cup', 'of', 'coffee'],
                '"I would like a cup of coffee" = Bir fincan kahve rica ediyorum.'
            ),
            (
                'multiple_choice',
                '"It is half past two." dijital saat olarak kaçı gösterir?',
                'It is half past two.',
                'It is half past two.',
                ['02:30', '02:15', '01:30', '02:45'],
                '02:30',
                '"half past" buçuk demektir; "half past two" = 02:30.'
            ),
            (
                'word_order',
                'Dinle ve cümleyi kur:',
                '',
                'The bathroom is on the right',
                ['The', 'bathroom', 'is', 'on', 'the', 'right', 'in', 'left'],
                ['The', 'bathroom', 'is', 'on', 'the', 'right'],
                '"The bathroom is on the right" = Tuvalet sağ taraftadır.'
            ),
            (
                'multiple_choice',
                '"Do you accept credit cards?" sorusuna verilebilecek en doğal olumlu cevap hangisidir?',
                'Do you accept credit cards?',
                'Do you accept credit cards?',
                ['Yes, we accept all major cards.', 'No, thank you so much.', 'I am a student.', 'It is on the right.'],
                'Yes, we accept all major cards.',
                '"Kredi kartı kabul ediyor musunuz?" sorusuna "Evet, tüm kartları kabul ediyoruz" en doğal cevaptır.'
            ),
            (
                'word_order',
                'Dinle ve cümleyi kur:',
                '',
                'Do you accept credit cards',
                ['Do', 'you', 'accept', 'credit', 'cards', 'have', 'cash'],
                ['Do', 'you', 'accept', 'credit', 'cards'],
                '"Do you accept credit cards?" = Kredi kartı kabul ediyor musunuz?'
            ),
            (
                'multiple_choice',
                '"The train leaves at five." cümlesinde hangi eylem bildirilmektedir?',
                'The train leaves at five.',
                'The train leaves at five.',
                ['Trenin saat beşte hareket edeceği', 'Trenin saat beşte varacağı', 'Trenin iptal olduğu', 'Trenin beş vagonlu olduğu'],
                'Trenin saat beşte hareket edeceği',
                '"leave" ayrılmak, hareket etmek demektir; tren saat 5\'te kalkıyor.'
            ),
            (
                'word_order',
                'Dinle ve cümleyi kur:',
                '',
                'There are sixty seconds in a minute',
                ['There', 'are', 'sixty', 'seconds', 'in', 'a', 'minute', 'is'],
                ['There', 'are', 'sixty', 'seconds', 'in', 'a', 'minute'],
                '"There are sixty seconds in a minute" = Bir dakikada altmış saniye vardır.'
            ),
        ]
    },
    {
        'title': 'Konu 5: Aile, İnsanlar & Tanımlamalar',
        'description': 'Aileni tanıt, insanları dış görünüş ve kişilik özellikleriyle tarif et.',
        'is_exam': 0, 'difficulty': 2, 'icon': '👨\u200d👩\u200d👦', 'xp': 15, 'order': 7,
        'questions': [
            (
                'multiple_choice',
                '"This is my older brother." cümlesi ne anlama gelir?',
                'This is my older brother.',
                'This is my older brother.',
                ['Bu benim ağabeyim (büyük erkek kardeşim).', 'Bu benim babam.', 'Bu benim amcam.', 'Bu benim en yakın arkadaşım.'],
                'Bu benim ağabeyim (büyük erkek kardeşim).',
                '"older brother" ağabey (yaşça büyük erkek kardeş) demektir.'
            ),
            (
                'word_order',
                'Dinle ve cümleyi kur:',
                '',
                'This is my older brother',
                ['This', 'is', 'my', 'older', 'brother', 'are', 'sister'],
                ['This', 'is', 'my', 'older', 'brother'],
                '"This is my older brother" = Bu benim ağabeyim.'
            ),
            (
                'multiple_choice',
                'Boşluğa hangisi gelmelidir? "I have two sisters, but I ___ have any brothers."',
                'I have two sisters, but I ___ have any brothers.',
                '',
                ["don't", 'am not', 'not', 'no'],
                "don't",
                'Geniş zamanda (Simple Present) olumsuzluk için "don\'t" (do not) kullanılır: "I don\'t have".'
            ),
            (
                'word_order',
                'Dinle ve cümleyi kur:',
                '',
                'I have two sisters',
                ['I', 'have', 'two', 'sisters', 'has', 'sister'],
                ['I', 'have', 'two', 'sisters'],
                '"I have two sisters" = İki kız kardeşim var.'
            ),
            (
                'multiple_choice',
                '"She has blue eyes and brown hair." cümlesi hangi özellikleri belirtir?',
                'She has blue eyes and brown hair.',
                'She has blue eyes and brown hair.',
                ['Mavi gözler ve kahverengi saçlar', 'Yeşil gözler ve sarı saçlar', 'Kahverengi gözler ve siyah saçlar', 'Mavi elbise ve kahverengi çanta'],
                'Mavi gözler ve kahverengi saçlar',
                '"blue eyes" = mavi gözler, "brown hair" = kahverengi saçlar.'
            ),
            (
                'word_order',
                'Dinle ve cümleyi kur:',
                '',
                'She has blue eyes and brown hair',
                ['She', 'has', 'blue', 'eyes', 'and', 'brown', 'hair', 'have'],
                ['She', 'has', 'blue', 'eyes', 'and', 'brown', 'hair'],
                '"She has blue eyes and brown hair" = Onun mavi gözleri ve kahverengi saçları var.'
            ),
            (
                'multiple_choice',
                'Kişilik tanımlarken "O çok cana yakın ve yardımseverdir." demek için hangisi kullanılır?',
                'O çok cana yakın ve yardımseverdir.',
                '',
                ['He is very friendly and helpful.', 'He is very angry and slow.', 'He has a friendly house.', 'He works very hard today.'],
                'He is very friendly and helpful.',
                '"friendly" cana yakın/arkadaş canlısı, "helpful" ise yardımsever demektir.'
            ),
            (
                'word_order',
                'Dinle ve cümleyi kur:',
                '',
                'He is very friendly and helpful',
                ['He', 'is', 'very', 'friendly', 'and', 'helpful', 'are', 'help'],
                ['He', 'is', 'very', 'friendly', 'and', 'helpful'],
                '"He is very friendly and helpful" = O çok cana yakın ve yardımseverdir.'
            ),
            (
                'multiple_choice',
                'Boşluğa hangisi gelmelidir? "My parents ___ in a quiet town."',
                'My parents ___ in a quiet town.',
                '',
                ['live', 'lives', 'living', 'is live'],
                'live',
                '"My parents" (annem ve babam) çoğul bir özne (they) olduğu için fiil yalın halde "live" olarak gelir.'
            ),
            (
                'word_order',
                'Dinle ve cümleyi kur:',
                '',
                'My parents live in a small town',
                ['My', 'parents', 'live', 'in', 'a', 'small', 'town', 'lives'],
                ['My', 'parents', 'live', 'in', 'a', 'small', 'town'],
                '"My parents live in a small town" = Anne ve babam küçük bir kasabada yaşıyor.'
            ),
        ]
    },
    {
        'title': 'Konu 6: Günlük Rutinler & Alışkanlıklar',
        'description': 'Sabah uyanışından akşam yatışına kadar günlük rutinlerini İngilizce anlat.',
        'is_exam': 0, 'difficulty': 2, 'icon': '🌅', 'xp': 15, 'order': 8,
        'questions': [
            (
                'multiple_choice',
                '"I wake up at seven every morning." cümlesinde hangi alışkanlık anlatılmaktadır?',
                'I wake up at seven every morning.',
                'I wake up at seven every morning.',
                ['Her sabah saat yedide uyanmak', 'Her sabah saat yedide evden çıkmak', 'Her akşam yedide uyumak', 'Her sabah yedi kilometre koşmak'],
                'Her sabah saat yedide uyanmak',
                '"wake up" uyanmak demektir; "at seven every morning" her sabah saat yedide.'
            ),
            (
                'word_order',
                'Dinle ve cümleyi kur:',
                '',
                'I wake up at seven every morning',
                ['I', 'wake', 'up', 'at', 'seven', 'every', 'morning', 'wakes'],
                ['I', 'wake', 'up', 'at', 'seven', 'every', 'morning'],
                '"I wake up at seven every morning" = Her sabah saat yedide uyanırım.'
            ),
            (
                'multiple_choice',
                'Boşluğa hangisi gelmelidir? "She usually ___ tea with her breakfast."',
                'She usually ___ tea with her breakfast.',
                '',
                ['drinks', 'drink', 'drinking', 'is drink'],
                'drinks',
                'Geniş zamanda (Simple Present) "she" öznesiyle fiile "-s" takısı gelir: "drinks".'
            ),
            (
                'word_order',
                'Dinle ve cümleyi kur:',
                '',
                'She usually drinks tea with breakfast',
                ['She', 'usually', 'drinks', 'tea', 'with', 'breakfast', 'drink'],
                ['She', 'usually', 'drinks', 'tea', 'with', 'breakfast'],
                '"She usually drinks tea with breakfast" = O kahvaltıda genellikle çay içer.'
            ),
            (
                'multiple_choice',
                'Ulaşım aracıyla işe gitmeyi belirtirken hangisi doğrudur?',
                'İşe otobüsle gidiyorum.',
                '',
                ['I go to work by bus.', 'I go to work with bus.', 'I go to work on bus.', 'I go to work bus.'],
                'I go to work by bus.',
                'Toplu taşıma ve ulaşım araçlarında "vasıtasıyla / ile" demek için "by" kullanılır: "by bus", "by train", "by car".'
            ),
            (
                'word_order',
                'Dinle ve cümleyi kur:',
                '',
                'I go to work by bus',
                ['I', 'go', 'to', 'work', 'by', 'bus', 'with', 'on'],
                ['I', 'go', 'to', 'work', 'by', 'bus'],
                '"I go to work by bus" = İşe otobüsle giderim.'
            ),
            (
                'multiple_choice',
                '"I brush my teeth before going to bed." cümlesinin anlamı nedir?',
                'I brush my teeth before going to bed.',
                'I brush my teeth before going to bed.',
                ['Yatmadan önce dişlerimi fırçalarım.', 'Yataktan kalkınca elimi yüzümü yıkarım.', 'Yemekten sonra dişlerimi fırçalarım.', 'Gece geç saatte uyurum.'],
                'Yatmadan önce dişlerimi fırçalarım.',
                '"brush my teeth" = dişlerimi fırçalamak; "before going to bed" = yatmadan önce.'
            ),
            (
                'word_order',
                'Dinle ve cümleyi kur:',
                '',
                'He reads a book every night',
                ['He', 'reads', 'a', 'book', 'every', 'night', 'read'],
                ['He', 'reads', 'a', 'book', 'every', 'night'],
                '"He reads a book every night" = O her gece bir kitap okur.'
            ),
            (
                'multiple_choice',
                'Boşluğa hangisi gelmelidir? "___ you exercise on weekends?"',
                '___ you exercise on weekends?',
                '',
                ['Do', 'Are', 'Is', 'Does'],
                'Do',
                'Geniş zamanda "you" öznesiyle yapılan fiil sorularında yardımcı fiil "Do" olur: "Do you exercise...?"'
            ),
            (
                'word_order',
                'Dinle ve cümleyi kur:',
                '',
                'We have dinner together at seven',
                ['We', 'have', 'dinner', 'together', 'at', 'seven', 'has'],
                ['We', 'have', 'dinner', 'together', 'at', 'seven'],
                '"We have dinner together at seven" = Saat yedide birlikte akşam yemeği yeriz.'
            ),
        ]
    },
    {
        'title': '🏆 Test 3: Ara Değerlendirme 3',
        'description': 'Aile tanımlamaları, 3. tekil şahıs fiil çekimi (-s) ve günlük rutinler sınavı.',
        'is_exam': 1, 'difficulty': 2, 'icon': '🏆', 'xp': 25, 'order': 9,
        'questions': [
            (
                'multiple_choice',
                'Gramer kuralına göre hangi cümle DOĞRUDUR?',
                'Gramer kontrolü',
                '',
                ['He plays football every Saturday.', 'He play football every Saturday.', 'He is play football every Saturday.', 'He playing football every Saturday.'],
                'He plays football every Saturday.',
                'Geniş zamanda özne "he" olduğunda fiil "-s" takısı alır: "He plays".'
            ),
            (
                'word_order',
                'Dinle ve cümleyi kur:',
                '',
                'She has blue eyes',
                ['She', 'has', 'blue', 'eyes', 'have', 'is'],
                ['She', 'has', 'blue', 'eyes'],
                '"She has blue eyes" = Onun mavi gözleri var.'
            ),
            (
                'multiple_choice',
                'Boşluğa hangisi gelmelidir? "My brother ___ drink coffee; he prefers tea."',
                'My brother ___ drink coffee; he prefers tea.',
                '',
                ["doesn't", "don't", "isn't", 'not'],
                "doesn't",
                '"My brother" (he) tekil olduğu için olumsuzluk eki "doesn\'t" (does not) olur.'
            ),
            (
                'word_order',
                'Dinle ve cümleyi kur:',
                '',
                'I brush my teeth before bed',
                ['I', 'brush', 'my', 'teeth', 'before', 'bed', 'brushes'],
                ['I', 'brush', 'my', 'teeth', 'before', 'bed'],
                '"I brush my teeth before bed" = Yatmadan önce dişlerimi fırçalarım.'
            ),
            (
                'multiple_choice',
                '"He looks like his father." ifadesi ne anlama gelir?',
                'He looks like his father.',
                'He looks like his father.',
                ['O babasına benziyor.', 'O babasını arıyor.', 'O babasını seviyor.', 'O babası gibi çalışıyor.'],
                'O babasına benziyor.',
                '"look like" birine görünüş veya tavır olarak benzemek demektir.'
            ),
            (
                'word_order',
                'Dinle ve cümleyi kur:',
                '',
                'My best friend is very tall',
                ['My', 'best', 'friend', 'is', 'very', 'tall', 'are'],
                ['My', 'best', 'friend', 'is', 'very', 'tall'],
                '"My best friend is very tall" = En yakın arkadaşım çok uzundur.'
            ),
            (
                'multiple_choice',
                'Sıklık zarflarının cümledeki yeri neresidir? "I ___ listen to podcasts."',
                'I ___ listen to podcasts.',
                '',
                ['always', 'every day', 'at the moment', 'now'],
                'always',
                '"always", "usually", "often" gibi sıklık zarfları özne ile ana fiil arasına gelir: "I always listen".'
            ),
            (
                'word_order',
                'Dinle ve cümleyi kur:',
                '',
                'They go for a walk in the evening',
                ['They', 'go', 'for', 'a', 'walk', 'in', 'the', 'evening', 'goes'],
                ['They', 'go', 'for', 'a', 'walk', 'in', 'the', 'evening'],
                '"They go for a walk in the evening" = Akşamları yürüyüşe çıkarlar.'
            ),
            (
                'multiple_choice',
                '"She never eats fast food." cümlesi ne bildirir?',
                'She never eats fast food.',
                'She never eats fast food.',
                ['O asla hazır (fast food) yemek yemez.', 'O bazen hazır yemek yer.', 'O her gün hazır yemek yer.', 'O hazır yemekleri çok sever.'],
                'O asla hazır (fast food) yemek yemez.',
                '"never" yüzde sıfır sıklık bildirir; "asla/hiçbir zaman" anlamına gelir.'
            ),
            (
                'word_order',
                'Dinle ve cümleyi kur:',
                '',
                'I go to work by bus',
                ['I', 'go', 'to', 'work', 'by', 'bus', 'on', 'with'],
                ['I', 'go', 'to', 'work', 'by', 'bus'],
                '"I go to work by bus" = İşe otobüsle giderim.'
            ),
        ]
    },
    {
        'title': 'Konu 7: Şimdiki Zaman & Anlık Aktiviteler',
        'description': 'Şu anda yaptığın eylemleri anlatmayı ve şimdiki zamanı (V-ing) öğren.',
        'is_exam': 0, 'difficulty': 2, 'icon': '⚡', 'xp': 15, 'order': 10,
        'questions': [
            (
                'multiple_choice',
                '"I am studying English right now." cümlesi ne anlama gelir?',
                'I am studying English right now.',
                'I am studying English right now.',
                ['Şu anda İngilizce çalışıyorum.', 'Her gün İngilizce çalışırım.', 'İngilizce çalışmayı severim.', 'Dün İngilizce çalıştım.'],
                'Şu anda İngilizce çalışıyorum.',
                '"am studying" ve "right now" şu anda gerçekleşen bir eylemi bildirir.'
            ),
            (
                'word_order',
                'Dinle ve cümleyi kur:',
                '',
                'I am studying English right now',
                ['I', 'am', 'studying', 'English', 'right', 'now', 'study'],
                ['I', 'am', 'studying', 'English', 'right', 'now'],
                '"I am studying English right now" = Şu anda İngilizce çalışıyorum.'
            ),
            (
                'multiple_choice',
                'Boşluğa hangisi gelmelidir? "What ___ you doing at the moment?"',
                'What ___ you doing at the moment?',
                '',
                ['are', 'do', 'is', 'have'],
                'are',
                'Şimdiki zamanda (Present Continuous) "you" öznesi ile "are + V-ing" kullanılır: "What are you doing?".'
            ),
            (
                'word_order',
                'Dinle ve cümleyi kur:',
                '',
                'What are you doing at the moment',
                ['What', 'are', 'you', 'doing', 'at', 'the', 'moment', 'do'],
                ['What', 'are', 'you', 'doing', 'at', 'the', 'moment'],
                '"What are you doing at the moment?" = Şu anda ne yapıyorsun?'
            ),
            (
                'multiple_choice',
                'Hava durumunu anlık olarak anlatırken "Dışarıda yağmur yağıyor." nasıl söylenir?',
                'Dışarıda yağmur yağıyor.',
                '',
                ['It is raining outside today.', 'It rains outside today.', 'It has rain outside.', 'The rain is go outside.'],
                'It is raining outside today.',
                'Hava olayları anlık olarak şimdiki zamanla anlatılır: "It is raining" (Yağmur yağıyor).'
            ),
            (
                'word_order',
                'Dinle ve cümleyi kur:',
                '',
                'It is raining outside today',
                ['It', 'is', 'raining', 'outside', 'today', 'rains', 'are'],
                ['It', 'is', 'raining', 'outside', 'today'],
                '"It is raining outside today" = Bugün dışarıda yağmur yağıyor.'
            ),
            (
                'multiple_choice',
                'Boşluğa hangisi gelmelidir? "Look! The children ___ football in the garden."',
                'Look! The children ___ football in the garden.',
                '',
                ['are playing', 'is playing', 'plays', 'play'],
                'are playing',
                '"Look!" (Bak!) anlık dikkat çeker ve şimdiki zaman gerektirir. "children" çoğul olduğu için "are playing" doğrudur.'
            ),
            (
                'word_order',
                'Dinle ve cümleyi kur:',
                '',
                'They are playing football in the garden',
                ['They', 'are', 'playing', 'football', 'in', 'the', 'garden', 'is'],
                ['They', 'are', 'playing', 'football', 'in', 'the', 'garden'],
                '"They are playing football in the garden" = Bahçede futbol oynuyorlar.'
            ),
            (
                'multiple_choice',
                '"The baby is sleeping peacefully." cümlesi ne bildirir?',
                'The baby is sleeping peacefully.',
                'The baby is sleeping peacefully.',
                ['Bebek huzur içinde uyuyor.', 'Bebek yatağında ağlıyor.', 'Bebek henüz uyumadı.', 'Bebek sessizce oynuyor.'],
                'Bebek huzur içinde uyuyor.',
                '"is sleeping" = uyuyor; "peacefully" = huzurla, sakince.'
            ),
            (
                'word_order',
                'Dinle ve cümleyi kur:',
                '',
                'We are waiting for the bus',
                ['We', 'are', 'waiting', 'for', 'the', 'bus', 'wait', 'to'],
                ['We', 'are', 'waiting', 'for', 'the', 'bus'],
                '"We are waiting for the bus" = Otobüsü bekliyoruz. "wait for" bir şeyi beklemek anlamına gelir.'
            ),
        ]
    },
    {
        'title': '🏆 Test 4: Konu 7 Pekiştirme Testi',
        'description': 'Geniş Zaman (Simple Present) ile Şimdiki Zaman (Continuous) farkını test et.',
        'is_exam': 1, 'difficulty': 3, 'icon': '🏆', 'xp': 25, 'order': 11,
        'questions': [
            (
                'multiple_choice',
                'Zaman farkı: "I usually drink coffee, but right now I ___ tea."',
                'I usually drink coffee, but right now I ___ tea.',
                '',
                ['am drinking', 'drink', 'drinks', 'drank'],
                'am drinking',
                '"right now" (şu anda) geçici anlık eylemi belirttiği için şimdiki zaman "am drinking" kullanılır.'
            ),
            (
                'word_order',
                'Dinle ve cümleyi kur:',
                '',
                'She is cooking dinner in the kitchen',
                ['She', 'is', 'cooking', 'dinner', 'in', 'the', 'kitchen', 'cooks'],
                ['She', 'is', 'cooking', 'dinner', 'in', 'the', 'kitchen'],
                '"She is cooking dinner in the kitchen" = O mutfakta akşam yemeği pişiriyor.'
            ),
            (
                'multiple_choice',
                'Boşluğa hangisi gelmelidir? "Listen! Somebody ___ at the door."',
                'Listen! Somebody ___ at the door.',
                '',
                ['is knocking', 'knocks', 'knock', 'are knocking'],
                'is knocking',
                '"Listen!" (Dinle!) o anda gerçekleşen eyleme işaret eder; "somebody" tekil kabul edildiği için "is knocking" gelir.'
            ),
            (
                'word_order',
                'Dinle ve cümleyi kur:',
                '',
                'He is listening to music right now',
                ['He', 'is', 'listening', 'to', 'music', 'right', 'now', 'listen'],
                ['He', 'is', 'listening', 'to', 'music', 'right', 'now'],
                '"He is listening to music right now" = O şu an müzik dinliyor.'
            ),
            (
                'multiple_choice',
                'Olumsuz şimdiki zaman: "Bugün çalışmıyorum, dinleniyorum." nasıl söylenir?',
                'Bugün çalışmıyorum, dinleniyorum.',
                '',
                ['I am not working today, I am resting.', "I don't work today, I rest.", 'I not working today.', 'I no work today.'],
                'I am not working today, I am resting.',
                'Günün anlık durumunu anlatırken "I am not working today, I am resting" en doğal kalıptır.'
            ),
            (
                'word_order',
                'Dinle ve cümleyi kur:',
                '',
                'Are you watching television right now',
                ['Are', 'you', 'watching', 'television', 'right', 'now', 'do'],
                ['Are', 'you', 'watching', 'television', 'right', 'now'],
                '"Are you watching television right now?" = Şu anda televizyon mu izliyorsun?'
            ),
            (
                'multiple_choice',
                'Boşluğa hangisi gelmelidir? "Why ___ you laughing?"',
                'Why ___ you laughing?',
                '',
                ['are', 'do', 'is', 'have'],
                'are',
                '"laughing" (-ing) olduğu için soru şimdiki zamandır ve "you" ile "are" kullanılır: "Why are you laughing?".'
            ),
            (
                'word_order',
                'Dinle ve cümleyi kur:',
                '',
                'The baby is sleeping peacefully',
                ['The', 'baby', 'is', 'sleeping', 'peacefully', 'are', 'sleep'],
                ['The', 'baby', 'is', 'sleeping', 'peacefully'],
                '"The baby is sleeping peacefully" = Bebek huzur içinde uyuyor.'
            ),
            (
                'multiple_choice',
                '"He is running in the park." cümlesi ne bildirir?',
                'He is running in the park.',
                'He is running in the park.',
                ['O şu an parkta koşuyor.', 'O her sabah parkta koşar.', 'O parkta yürüyüş yapar.', 'O parka doğru gidiyor.'],
                'O şu an parkta koşuyor.',
                '"is running" anlık olarak şu anda koştuğunu belirtir.'
            ),
            (
                'word_order',
                'Dinle ve cümleyi kur:',
                '',
                'I am studying English right now',
                ['I', 'am', 'studying', 'English', 'right', 'now', 'studies'],
                ['I', 'am', 'studying', 'English', 'right', 'now'],
                '"I am studying English right now" = Şu anda İngilizce çalışıyorum.'
            ),
        ]
    },
    {
        'title': '🏆 Test 5: Ünite 1 Genel Deneme Sınavı',
        'description': '1. Ünitenin tüm konularını (Selamlaşma, Alışveriş, Zaman, Aile, Rutinler) kapsayan deneme.',
        'is_exam': 1, 'difficulty': 3, 'icon': '📝', 'xp': 30, 'order': 12,
        'questions': [
            (
                'multiple_choice',
                'Diyalog tamamlama: "Excuse me, where is the nearest supermarket?" - "___"',
                'Excuse me, where is the nearest supermarket?',
                'Excuse me, where is the nearest supermarket?',
                ['It is on the right, next to the bank.', 'I am fine, thank you.', "It is five o'clock.", 'Yes, I speak English.'],
                'It is on the right, next to the bank.',
                'Adres sorulduğunda yön belirten "It is on the right, next to the bank" (Sağda, bankanın yanında) en mantıklı cevaptır.'
            ),
            (
                'word_order',
                'Dinle ve cümleyi kur:',
                '',
                'How are you doing today',
                ['How', 'are', 'you', 'doing', 'today', 'do', 'is'],
                ['How', 'are', 'you', 'doing', 'today'],
                '"How are you doing today?" = Bugün nasılsın, nasıl gidiyor?'
            ),
            (
                'multiple_choice',
                'Boşluğa hangisi gelmelidir? "My father is a doctor. He ___ at a hospital."',
                'My father is a doctor. He ___ at a hospital.',
                '',
                ['works', 'work', 'is working', 'working'],
                'works',
                'Genel durumlar ve meslek icraları geniş zamanla anlatılır; "he" ile "works" gelir.'
            ),
            (
                'word_order',
                'Dinle ve cümleyi kur:',
                '',
                'Can I have the bill please',
                ['Can', 'I', 'have', 'the', 'bill', 'please', 'take', 'pay'],
                ['Can', 'I', 'have', 'the', 'bill', 'please'],
                '"Can I have the bill, please?" = Hesabı alabilir miyim, lütfen?'
            ),
            (
                'multiple_choice',
                '"What time does the train leave?" sorusuna en uygun cevap hangisidir?',
                'What time does the train leave?',
                'What time does the train leave?',
                ['It leaves at half past four.', 'It is on the platform.', 'Yes, it is very fast.', 'I like traveling by train.'],
                'It leaves at half past four.',
                'Saat sorulduğu için "Saat dört buçukta kalkıyor" (It leaves at half past four) doğru cevaptır.'
            ),
            (
                'word_order',
                'Dinle ve cümleyi kur:',
                '',
                'I wake up at seven every morning',
                ['I', 'wake', 'up', 'at', 'seven', 'every', 'morning', 'wakes'],
                ['I', 'wake', 'up', 'at', 'seven', 'every', 'morning'],
                '"I wake up at seven every morning" = Her sabah saat yedide uyanırım.'
            ),
            (
                'multiple_choice',
                'Boşluğa hangisi gelmelidir? "Look at Sarah! She ___ a beautiful book right now."',
                'Look at Sarah! She ___ a beautiful book right now.',
                '',
                ['is reading', 'reads', 'read', 'are reading'],
                'is reading',
                '"Look at Sarah!" ve "right now" anlık eylemi gösterir; "she" ile "is reading" kullanılır.'
            ),
            (
                'word_order',
                'Dinle ve cümleyi kur:',
                '',
                'I would like a cup of coffee please',
                ['I', 'would', 'like', 'a', 'cup', 'of', 'coffee', 'please', 'want'],
                ['I', 'would', 'like', 'a', 'cup', 'of', 'coffee', 'please'],
                '"I would like a cup of coffee, please" = Bir fincan kahve rica ediyorum, lütfen.'
            ),
            (
                'multiple_choice',
                'Hangisi "Kendine iyi bak, sonra görüşürüz!" anlamındadır?',
                'Kendine iyi bak, sonra görüşürüz!',
                '',
                ['Take care, see you later!', 'Nice to meet you, goodbye!', 'Excuse me, can you help me?', 'You are very welcome!'],
                'Take care, see you later!',
                '"Take care" (Kendine iyi bak) ve "see you later" (sonra görüşürüz) samimi ve doğal vedalaşmadır.'
            ),
            (
                'word_order',
                'Dinle ve cümleyi kur:',
                '',
                'She usually drinks tea with breakfast',
                ['She', 'usually', 'drinks', 'tea', 'with', 'breakfast', 'drink'],
                ['She', 'usually', 'drinks', 'tea', 'with', 'breakfast'],
                '"She usually drinks tea with breakfast" = O kahvaltıda genellikle çay içer.'
            ),
        ]
    },
    {
        'title': '👑 Test 6: Ünite 1 Seviye Atlama Boss Sınavı',
        'description': 'A1 Seviye Atlama Kupası! 1. Ünitenin tüm dilbilgisi ve dinleme kalıplarını ustalıkla tamamla.',
        'is_exam': 1, 'difficulty': 3, 'icon': '👑', 'xp': 50, 'order': 13,
        'questions': [
            (
                'multiple_choice',
                'Doğallık ve gramer kontrolü: Aşağıdaki cümlelerden hangisi hem doğal hem de gramer olarak KUSURSUZDUR?',
                'Kusursuz cümleyi seç:',
                '',
                ['I usually walk to work, but today I am taking the bus.', 'I am usually walk to work, but today I take the bus.', 'I usually walking to work, but today I am take the bus.', 'I usually walk to work, but today I takes the bus.'],
                'I usually walk to work, but today I am taking the bus.',
                'Rutinler için "I usually walk", anlık/özel bugünkü durum için "today I am taking the bus" birlikte kusursuz bir zıtlık oluşturur.'
            ),
            (
                'word_order',
                'Dinle ve cümleyi kur:',
                '',
                'Where are you from',
                ['Where', 'are', 'you', 'from', 'do', 'is'],
                ['Where', 'are', 'you', 'from'],
                '"Where are you from?" = Nerelisin?'
            ),
            (
                'multiple_choice',
                'Boşluğa doğru zamanı seç: "Shh! Be quiet, the baby ___ right now."',
                'Shh! Be quiet, the baby ___ right now.',
                '',
                ['is sleeping', 'sleeps', 'sleeping', 'are sleeping'],
                'is sleeping',
                '"Shh! Be quiet" (Sessiz ol!) ve "right now" şu anda uyuduğunu belirtir; "the baby" tekildir: "is sleeping".'
            ),
            (
                'word_order',
                'Dinle ve cümleyi kur:',
                '',
                'Do you speak English',
                ['Do', 'you', 'speak', 'English', 'are', 'speaks'],
                ['Do', 'you', 'speak', 'English'],
                '"Do you speak English?" = İngilizce biliyor musun?'
            ),
            (
                'multiple_choice',
                '"Can I have the bill, please?" ifadesinin kullanım bağlamı nedir?',
                'Can I have the bill, please?',
                'Can I have the bill, please?',
                ['Restoran veya kafede hesabı nezaketle talep etmek', 'Bir mağazada kıyafet denemek istemek', 'Havalimanında bilet kontrolü yaptırmak', 'Otele giriş yapmak'],
                'Restoran veya kafede hesabı nezaketle talep etmek',
                '"Can I have the bill, please?" hesap ödemek istediğinizde garsona söylenen en kibar kalıptır.'
            ),
            (
                'word_order',
                'Dinle ve cümleyi kur:',
                '',
                'There are sixty seconds in a minute',
                ['There', 'are', 'sixty', 'seconds', 'in', 'a', 'minute', 'is'],
                ['There', 'are', 'sixty', 'seconds', 'in', 'a', 'minute'],
                '"There are sixty seconds in a minute" = Bir dakikada altmış saniye vardır.'
            ),
            (
                'multiple_choice',
                'Boşluğa hangisi gelmelidir? "My brother ___ early on weekdays, but on weekends he ___ until ten."',
                'Geniş zaman çekimi',
                '',
                ['wakes up / sleeps', 'wake up / sleep', 'is waking up / is sleeping', 'wakes up / sleep'],
                'wakes up / sleeps',
                '"My brother" (he) öznesi için geniş zamanda her iki fiile de "-s" takısı gelir: "wakes up" ve "sleeps".'
            ),
            (
                'word_order',
                'Dinle ve cümleyi kur:',
                '',
                'He is very friendly and helpful',
                ['He', 'is', 'very', 'friendly', 'and', 'helpful', 'are', 'help'],
                ['He', 'is', 'very', 'friendly', 'and', 'helpful'],
                '"He is very friendly and helpful" = O çok cana yakın ve yardımseverdir.'
            ),
            (
                'multiple_choice',
                'Diyalog tamamlama: "Have a nice day and take care!" - "___"',
                'Have a nice day and take care!',
                'Have a nice day and take care!',
                ['Thank you, you too! See you later.', "No, I don't understand.", 'Where is the supermarket?', 'I am twenty years old.'],
                'Thank you, you too! See you later.',
                'İyi günler ve kendine iyi bak dileğine "Teşekkürler, sana da! Sonra görüşürüz" en doğal cevaptır.'
            ),
            (
                'word_order',
                'Dinle ve cümleyi kur:',
                '',
                'See you on Friday afternoon',
                ['See', 'you', 'on', 'Friday', 'afternoon', 'at', 'in'],
                ['See', 'you', 'on', 'Friday', 'afternoon'],
                '"See you on Friday afternoon" = Cuma öğleden sonra görüşürüz.'
            ),
        ]
    },
]
