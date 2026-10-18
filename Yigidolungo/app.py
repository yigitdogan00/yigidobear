import os
import json
import sqlite3
import datetime
import secrets
from functools import wraps
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, g
from authlib.integrations.flask_client import OAuth

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'yigidobear-gizli-anahtar-12345')

DB_PATH = os.path.join(os.path.dirname(__file__), 'database.db')
if not os.path.exists(DB_PATH):
    from init_db import init_db
    init_db()

# Setup Authlib Google OAuth 2.0
oauth = OAuth(app)
google_client_id = os.environ.get('GOOGLE_CLIENT_ID', '').strip()
google_client_secret = os.environ.get('GOOGLE_CLIENT_SECRET', '').strip()

oauth.register(
    name='google',
    client_id=google_client_id,
    client_secret=google_client_secret,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

HEART_REFILL_INTERVAL = 900 # 15 minutes (in seconds)

STORIES_DATA = [
    # ==========================================
    # LEVEL A1: BAŞLANGIÇ (5 Stories)
    # ==========================================
    {
        'level': 'A1',
        'order_in_level': 1,
        'unit_id': 1,
        'title': 'Yiğido Kafede',
        'description': 'Yiğido şirin bir kafede sıcak çikolata ve kek siparişi veriyor.',
        'icon': '☕',
        'xp_reward': 20,
        'pages': {
            1: [
                ('Garson', '☕', 'Hello! Welcome to the cafe. What would you like to drink?', 'Merhaba! Kafeye hoş geldiniz. Ne içmek istersiniz?', 1, 1),
                ('Yiğido', '/static/images/mascot_happy.svg', 'Hello! I would like a hot chocolate, please.', 'Merhaba! Bir sıcak çikolata istiyorum, lütfen.', 2, 0)
            ],
            2: [
                ('Garson', '☕', 'Of course! Would you like a piece of cake with it?', 'Tabii ki! Yanında bir dilim kek ister misiniz?', 1, 1),
                ('Yiğido', '/static/images/mascot_happy.svg', 'Yes, chocolate cake please. Thank you very much!', 'Evet, çikolatalı kek lütfen. Çok teşekkür ederim!', 2, 0)
            ],
            3: [
                ('Garson', '☕', 'Here is your hot chocolate and chocolate cake. Enjoy!', 'İşte sıcak çikolatanız ve çikolatalı kekiniz. Afiyet olsun!', 1, 1),
                ('Yiğido', '/static/images/mascot_happy.svg', 'It looks delicious! How much is it?', 'Çok lezzetli görünüyor! Ne kadar?', 2, 0),
                ('Garson', '☕', 'It is five dollars. Have a wonderful day!', 'Beş dolar tuttu. Harika bir gün dilerim!', 3, 1)
            ]
        },
        'question': {
            'question_text': 'What drink did Yiğido order at the cafe?',
            'options': ['Hot chocolate', 'Black coffee', 'Cold apple juice'],
            'correct_answer': 'Hot chocolate',
            'explanation': 'Yiğido garsona sıcak çikolata istediğini ("hot chocolate") söyledi.'
        }
    },
    {
        'level': 'A1',
        'order_in_level': 2,
        'unit_id': 1,
        'title': 'Yeni Bir Arkadaş',
        'description': 'Yiğido parkta yeni bir arkadaşla tanışıyor.',
        'icon': '👋',
        'xp_reward': 20,
        'pages': {
            1: [
                ('Yiğido', '/static/images/mascot_happy.svg', 'Hi! My name is Yiğido. What is your name?', 'Selam! Benim adım Yiğido. Senin adın ne?', 1, 0),
                ('Mia', '🐱', 'Hello Yiğido! I am Mia. Nice to meet you.', 'Merhaba Yiğido! Ben Mia. Tanıştığımıza memnun oldum.', 2, 1)
            ],
            2: [
                ('Yiğido', '/static/images/mascot_happy.svg', 'Where are you from, Mia?', 'Nerelisin, Mia?', 1, 0),
                ('Mia', '🐱', 'I am from Canada. Are you from Turkey?', 'Kanada\'danım. Sen Türkiye\'den misin?', 2, 1)
            ],
            3: [
                ('Yiğido', '/static/images/mascot_happy.svg', 'Yes, I am from Turkey! Let\'s play together.', 'Evet, Türkiye\'denim! Haydi birlikte oynayalım.', 1, 0),
                ('Mia', '🐱', 'Great idea! Let\'s go to the swing.', 'Harika fikir! Salıncağa gidelim.', 2, 1)
            ]
        },
        'question': {
            'question_text': 'Where is Mia from?',
            'options': ['Canada', 'Turkey', 'Germany'],
            'correct_answer': 'Canada',
            'explanation': 'Mia kendisinin Kanada\'dan ("I am from Canada") olduğunu belirtti.'
        }
    },
    {
        'level': 'A1',
        'order_in_level': 3,
        'unit_id': 1,
        'title': 'Manavda Alışveriş',
        'description': 'Yiğido taze ve lezzetli meyveler seçiyor.',
        'icon': '🍎',
        'xp_reward': 20,
        'pages': {
            1: [
                ('Manav', '👨‍🌾', 'Good morning! Can I help you today?', 'Günaydın! Bugün yardımcı olabilir miyim?', 1, 1),
                ('Yiğido', '/static/images/mascot_happy.svg', 'Good morning! Are these red apples sweet?', 'Günaydın! Bu kırmızı elmalar tatlı mı?', 2, 0)
            ],
            2: [
                ('Manav', '👨‍🌾', 'Yes, they are very sweet and fresh!', 'Evet, çok tatlı ve tazeler!', 1, 1),
                ('Yiğido', '/static/images/mascot_happy.svg', 'Can I have four red apples and two bananas?', 'Dört kırmızı elma ve iki muz alabilir miyim?', 2, 0)
            ],
            3: [
                ('Manav', '👨‍🌾', 'Here is your fruit bag. That is three dollars.', 'İşte meyve çantanız. Üç dolar tuttu.', 1, 1),
                ('Yiğido', '/static/images/mascot_happy.svg', 'Here is the money. Thank you, have a good day!', 'Buyrun para. Teşekkürler, iyi günler!', 2, 0)
            ]
        },
        'question': {
            'question_text': 'How many apples did Yiğido buy?',
            'options': ['Four', 'Two', 'Six'],
            'correct_answer': 'Four',
            'explanation': 'Yiğido dört adet kırmızı elma ("four red apples") istedi.'
        }
    },
    {
        'level': 'A1',
        'order_in_level': 4,
        'unit_id': 1,
        'title': 'Kayıp Kedi',
        'description': 'Parkta ağacın altında kaybolan sevimli beyaz bir kedi.',
        'icon': '🐈',
        'xp_reward': 20,
        'pages': {
            1: [
                ('Yiğido', '/static/images/mascot_happy.svg', 'Look! There is a little white cat under the big tree.', 'Bak! Büyük ağacın altında küçük beyaz bir kedi var.', 1, 0),
                ('Leo', '🐶', 'Oh, it looks scared. Does it have a collar?', 'Ah, korkmuş görünüyor. Tasması var mı?', 2, 1)
            ],
            2: [
                ('Yiğido', '/static/images/mascot_happy.svg', 'Yes, it has a blue collar with a name: Snowy.', 'Evet, üzerinde Snowy yazan mavi bir tasması var.', 1, 0),
                ('Leo', '🐶', 'There is a phone number too! Let\'s call the owner.', 'Bir telefon numarası da var! Sahibini arayalım.', 2, 1)
            ],
            3: [
                ('Sahip', '👩', 'Thank you so much for finding Snowy!', 'Snowy\'yi bulduğunuz için çok teşekkür ederim!', 1, 1),
                ('Yiğido', '/static/images/mascot_happy.svg', 'You are welcome! Snowy is very safe and friendly.', 'Rica ederiz! Snowy çok güvende ve dost canlısı.', 2, 0)
            ]
        },
        'question': {
            'question_text': 'What color is the cat\'s collar?',
            'options': ['Blue', 'Red', 'Yellow'],
            'correct_answer': 'Blue',
            'explanation': 'Kedinin mavi bir tasması ("blue collar") olduğu belirtildi.'
        }
    },
    {
        'level': 'A1',
        'order_in_level': 5,
        'unit_id': 1,
        'title': 'Otobüs Durağında',
        'description': 'Şehir merkezine giden otobüsü bekleme.',
        'icon': '🚌',
        'xp_reward': 20,
        'pages': {
            1: [
                ('Yiğido', '/static/images/mascot_happy.svg', 'Excuse me, does this bus go to the city center?', 'Affedersiniz, bu otobüs şehir merkezine gider mi?', 1, 0),
                ('Yolcu', '🎒', 'Yes, bus number 12 goes directly to the center.', 'Evet, 12 numaralı otobüs doğrudan merkeze gider.', 2, 1)
            ],
            2: [
                ('Yiğido', '/static/images/mascot_happy.svg', 'What time does it usually arrive?', 'Genellikle saat kaçta gelir?', 1, 0),
                ('Yolcu', '🎒', 'It usually arrives in ten minutes.', 'Genellikle on dakika içinde gelir.', 2, 1)
            ],
            3: [
                ('Yiğido', '/static/images/mascot_happy.svg', 'The bus is coming now! Thank you for your help.', 'Otobüs şimdi geliyor! Yardımın için teşekkürler.', 1, 0),
                ('Yolcu', '🎒', 'You are welcome! Have a safe and nice trip!', 'Rica ederim! Güvenli ve güzel bir yolculuk dilerim!', 2, 1)
            ]
        },
        'question': {
            'question_text': 'Which bus goes to the city center?',
            'options': ['Bus number 12', 'Bus number 5', 'Bus number 24'],
            'correct_answer': 'Bus number 12',
            'explanation': 'Yolcu 12 numaralı otobüsün ("bus number 12") merkeze gittiğini söyledi.'
        }
    },

    # ==========================================
    # LEVEL A2: TEMEL (5 Stories)
    # ==========================================
    {
        'level': 'A2',
        'order_in_level': 1,
        'unit_id': 1,
        'title': 'Kütüphanede Kitap Arayışı',
        'description': 'Yiğido macera ve bilim kurgu kitapları arıyor.',
        'icon': '📖',
        'xp_reward': 20,
        'pages': {
            1: [
                ('Kütüphaneci', '👓', 'Welcome to the town library! Are you searching for a specific book?', 'Şehir kütüphanesine hoş geldiniz! Belirli bir kitap mı arıyorsunuz?', 1, 1),
                ('Yiğido', '/static/images/mascot_happy.svg', 'Yes, I am looking for adventure books for young learners.', 'Evet, genç öğrenciler için macera kitapları arıyorum.', 2, 0)
            ],
            2: [
                ('Kütüphaneci', '👓', 'They are on the second floor in section B.', 'İkinci katta B bölümündeler.', 1, 1),
                ('Yiğido', '/static/images/mascot_happy.svg', 'How many books can I borrow at a time?', 'Bir seferde kaç kitap ödünç alabilirim?', 2, 0)
            ],
            3: [
                ('Kütüphaneci', '👓', 'You can borrow up to three books for two weeks.', 'İki haftalığına en fazla üç kitap ödünç alabilirsin.', 1, 1),
                ('Yiğido', '/static/images/mascot_happy.svg', 'Awesome! I found two fascinating books already.', 'Harika! Şimdiden iki büyüleyici kitap buldum.', 2, 0)
            ]
        },
        'question': {
            'question_text': 'Where are the adventure books located?',
            'options': ['On the second floor', 'In the basement', 'At the entrance'],
            'correct_answer': 'On the second floor',
            'explanation': 'Kütüphaneci kitapların ikinci katta ("on the second floor") olduğunu söyledi.'
        }
    },
    {
        'level': 'A2',
        'order_in_level': 2,
        'unit_id': 1,
        'title': 'Hafta Sonu Kamp Planı',
        'description': 'Göl kenarında çadır kurma ve barbekü planı.',
        'icon': '🏕️',
        'xp_reward': 20,
        'pages': {
            1: [
                ('Sam', '🏕️', 'Hey Yiğido, what are your plans for this Saturday?', 'Hey Yiğido, bu cumartesi için planların neler?', 1, 1),
                ('Yiğido', '/static/images/mascot_happy.svg', 'I am planning to go camping near Blue Lake with my friends.', 'Arkadaşlarımla Mavi Göl yakınında kamp yapmayı planlıyorum.', 2, 0)
            ],
            2: [
                ('Sam', '🏕️', 'The weather forecast says it will be sunny and warm all weekend.', 'Hava durumu tüm hafta sonunun güneşli ve ılık olacağını söylüyor.', 1, 1),
                ('Yiğido', '/static/images/mascot_happy.svg', 'That is perfect! We will bring tents and roast marshmallows.', 'Bu mükemmel! Çadır getireceğiz ve marshmallow kızartacağız.', 2, 0)
            ],
            3: [
                ('Sam', '🏕️', 'Do you have room for one more camper in your tent?', 'Çadırınızda bir kampçı için daha yer var mı?', 1, 1),
                ('Yiğido', '/static/images/mascot_happy.svg', 'Yes, of course! You should definitely come with us.', 'Evet, tabii ki! Kesinlikle bizimle gelmelisin.', 2, 0)
            ]
        },
        'question': {
            'question_text': 'What will the weather be like according to the forecast?',
            'options': ['Sunny and warm', 'Rainy and windy', 'Cold and snowy'],
            'correct_answer': 'Sunny and warm',
            'explanation': 'Hava durumunun güneşli ve ılık ("sunny and warm") olacağı belirtildi.'
        }
    },
    {
        'level': 'A2',
        'order_in_level': 3,
        'unit_id': 1,
        'title': 'Doktorda Sağlık Kontrolü',
        'description': 'Boğaz ağrısı ve soğuk algınlığı şikayeti.',
        'icon': '🩺',
        'xp_reward': 20,
        'pages': {
            1: [
                ('Doktor', '🩺', 'Hello Yiğido! What seems to be the trouble today?', 'Merhaba Yiğido! Bugün şikayetin nedir?', 1, 1),
                ('Yiğido', '/static/images/mascot_happy.svg', 'I have a sore throat and a slight fever since yesterday evening.', 'Dün akşamdan beri boğaz ağrım ve hafif ateşim var.', 2, 0)
            ],
            2: [
                ('Doktor', '🩺', 'Let me listen to your breathing. Your lungs sound clear.', 'Nefesini dinleyeyim. Ciğerlerin temiz duyuluyor.', 1, 1),
                ('Yiğido', '/static/images/mascot_happy.svg', 'Should I stay in bed and take some medicine?', 'Yatakta dinlenip ilaç almalı mıyım?', 2, 0)
            ],
            3: [
                ('Doktor', '🩺', 'Drink warm mint tea with lemon, rest for two days and take this syrup.', 'Limonlu ılık nane çayı iç, iki gün dinlen ve bu şurubu kullan.', 1, 1),
                ('Yiğido', '/static/images/mascot_happy.svg', 'Thank you doctor, I will follow your advice carefully.', 'Teşekkürler doktor, tavsiyelerinize dikkatle uyacağım.', 2, 0)
            ]
        },
        'question': {
            'question_text': 'What health issue does Yiğido describe?',
            'options': ['A sore throat and slight fever', 'A broken leg', 'A stomach ache'],
            'correct_answer': 'A sore throat and slight fever',
            'explanation': 'Yiğido boğaz ağrısı ve hafif ateş ("sore throat and a slight fever") tarif etti.'
        }
    },
    {
        'level': 'A2',
        'order_in_level': 4,
        'unit_id': 1,
        'title': 'Kıyafet Mağazasında',
        'description': 'Kış mevsimi için sıcak ve rahat bir kazak seçimi.',
        'icon': '👕',
        'xp_reward': 20,
        'pages': {
            1: [
                ('Satıcı', '🛍️', 'Good afternoon! Are you looking for anything special?', 'İyi günler! Özel bir şey mi arıyorsunuz?', 1, 1),
                ('Yiğido', '/static/images/mascot_happy.svg', 'Yes, I am looking for a warm blue wool sweater in medium size.', 'Evet, orta boy sıcak mavi bir yün kazak arıyorum.', 2, 0)
            ],
            2: [
                ('Satıcı', '🛍️', 'We have this soft knit sweater. The changing room is to your left.', 'Bu yumuşak triko kazağımız var. Deneme kabini solunuzda.', 1, 1),
                ('Yiğido', '/static/images/mascot_happy.svg', 'I tried it on. It feels very comfortable and cozy!', 'Denedim. Çok rahat ve sıcacık hissettiriyor!', 2, 0)
            ],
            3: [
                ('Satıcı', '🛍️', 'There is a twenty percent discount on all knitwear today.', 'Bugün tüm trikolarda yüzde yirmi indirim var.', 1, 1),
                ('Yiğido', '/static/images/mascot_happy.svg', 'That is a wonderful bargain! I will buy it.', 'Bu harika bir kelepir! Satın alıyorum.', 2, 0)
            ]
        },
        'question': {
            'question_text': 'What color and size sweater did Yiğido want?',
            'options': ['Blue in medium', 'Red in small', 'Black in large'],
            'correct_answer': 'Blue in medium',
            'explanation': 'Yiğido orta beden mavi kazak ("blue wool sweater in medium size") istedi.'
        }
    },
    {
        'level': 'A2',
        'order_in_level': 5,
        'unit_id': 1,
        'title': 'Tren İstasyonunda Bilet',
        'description': 'Sahil kentine ekspres tren bileti satın alma.',
        'icon': '🚆',
        'xp_reward': 20,
        'pages': {
            1: [
                ('Biletçi', '🎫', 'Hello! Where would you like to travel today?', 'Merhaba! Bugün nereye seyahat etmek istersiniz?', 1, 1),
                ('Yiğido', '/static/images/mascot_happy.svg', 'I would like a return ticket to the seaside city of Brighton, please.', 'Sahil kenti Brighton\'a bir gidiş-dönüş bileti istiyorum, lütfen.', 2, 0)
            ],
            2: [
                ('Biletçi', '🎫', 'Would you prefer a window seat or an aisle seat?', 'Cam kenarı mı yoksa koridor kenarı mı tercih edersiniz?', 1, 1),
                ('Yiğido', '/static/images/mascot_happy.svg', 'A window seat please, so I can enjoy the sea view.', 'Cam kenarı lütfen, böylece deniz manzarasının tadını çıkarabilirim.', 2, 0)
            ],
            3: [
                ('Biletçi', '🎫', 'Your train departs from platform 3 at ten o\'clock sharp.', 'Treniniz tam saat onda peron 3\'ten kalkıyor.', 1, 1),
                ('Yiğido', '/static/images/mascot_happy.svg', 'Thank you! I will board the train right now.', 'Teşekkürler! Hemen şimdi trene biniyorum.', 2, 0)
            ]
        },
        'question': {
            'question_text': 'Which seat preference did Yiğido choose?',
            'options': ['A window seat', 'An aisle seat', 'A back seat'],
            'correct_answer': 'A window seat',
            'explanation': 'Yiğido deniz manzarasını görmek için cam kenarı ("a window seat") seçti.'
        }
    },

    # ==========================================
    # LEVEL B1: ORTA (5 Stories)
    # ==========================================
    {
        'level': 'B1',
        'order_in_level': 1,
        'unit_id': 1,
        'title': 'İş Mülakatı Hazırlığı',
        'description': 'Yazılım stajı mülakatı öncesi koçluk ve taktikler.',
        'icon': '💼',
        'xp_reward': 20,
        'pages': {
            1: [
                ('Kariyer Koçu', '👔', 'Confidence and clear communication are crucial for your upcoming interview.', 'Yaklaşan mülakatın için özgüven ve net iletişim çok önemlidir.', 1, 1),
                ('Yiğido', '/static/images/mascot_happy.svg', 'I have practiced answers about my collaborative projects and coding skills.', 'Ortak projelerim ve kodlama becerilerim hakkındaki yanıtları pratik yaptım.', 2, 0)
            ],
            2: [
                ('Kariyer Koçu', '👔', 'How do you handle unexpected setbacks during a sprint deadline?', 'Teslim tarihi yaklaşırken beklenmeyen aksilikleri nasıl yönetirsin?', 1, 1),
                ('Yiğido', '/static/images/mascot_happy.svg', 'I prioritize urgent tasks and communicate transparently with my team through daily syncs.', 'Acil görevleri önceliklendirir ve günlük toplantılarla ekibimle şeffaf iletişim kurarım.', 2, 0)
            ],
            3: [
                ('Kariyer Koçu', '👔', 'That demonstrates maturity and problem-solving capability. You will do great!', 'Bu olgunluk ve problem çözme yeteneği sergiliyor. Harika iş çıkaracaksın!', 1, 1),
                ('Yiğido', '/static/images/mascot_happy.svg', 'Thank you for your valuable feedback! I feel well-prepared now.', 'Değerli geri bildiriminiz için teşekkürler! Şimdi kendimi gayet hazır hissediyorum.', 2, 0)
            ]
        },
        'question': {
            'question_text': 'How does Yiğido manage unexpected setbacks according to his response?',
            'options': ['Prioritizing tasks and daily team syncs', 'Ignoring the deadline', 'Working alone in secret'],
            'correct_answer': 'Prioritizing tasks and daily team syncs',
            'explanation': 'Yiğido görevleri önceliklendirip ekiple günlük toplantılarla iletişim kurduğunu belirtti.'
        }
    },
    {
        'level': 'B1',
        'order_in_level': 2,
        'unit_id': 1,
        'title': 'Otel Rezervasyon Sorunu',
        'description': 'Otel odasındaki gürültü sorununu profesyonelce çözme.',
        'icon': '🏨',
        'xp_reward': 20,
        'pages': {
            1: [
                ('Resepsiyon', '🛎️', 'Good evening sir, welcome to Blue Bay Resort.', 'İyi akşamlar efendim, Blue Bay Resort\'a hoş geldiniz.', 1, 1),
                ('Yiğido', '/static/images/mascot_happy.svg', 'Good evening. I booked a quiet ocean-view room, but this room is right above the noisy street.', 'İyi akşamlar. Sessiz bir okyanus manzaralı oda ayırtmıştım, ancak bu oda gürültülü caddenin tam üstünde.', 2, 0)
            ],
            2: [
                ('Resepsiyon', '🛎️', 'I sincerely apologize for the inconvenience. Let me check our vacant rooms immediately.', 'Aksaklık için içtenlikle özür dilerim. Hemen boş odalarımızı kontrol edeyim.', 1, 1),
                ('Yiğido', '/static/images/mascot_happy.svg', 'I have my booking confirmation number right here on my phone.', 'Telefonumda rezervasyon onay numaram burada hazır.', 2, 0)
            ],
            3: [
                ('Resepsiyon', '🛎️', 'We have upgraded you to a deluxe balcony suite on the top floor free of charge.', 'Sizi en üst kattaki delüks balkonlu süite ücretsiz olarak yükselttik.', 1, 1),
                ('Yiğido', '/static/images/mascot_happy.svg', 'That is very generous and professional. Thank you for resolving it so quickly!', 'Bu çok cömert ve profesyonelce. Bu kadar çabuk çözdüğünüz için teşekkür ederim!', 2, 0)
            ]
        },
        'question': {
            'question_text': 'What solution did the receptionist offer to Yiğido?',
            'options': ['A free upgrade to a deluxe top-floor suite', 'A refund and cancellation', 'Earplugs for the night'],
            'correct_answer': 'A free upgrade to a deluxe top-floor suite',
            'explanation': 'Resepsiyon görevlisi Yiğido\'ya en üst katta ücretsiz delüks süit yükseltmesi teklif etti.'
        }
    },
    {
        'level': 'B1',
        'order_in_level': 3,
        'unit_id': 1,
        'title': 'Çevre ve Geri Dönüşüm',
        'description': 'Mahallede sıfır atık ve sürdürülebilirlik hareketi.',
        'icon': '♻️',
        'xp_reward': 20,
        'pages': {
            1: [
                ('Çevre Uzmanı', '🌿', 'Recycling plastic and aluminum conserves a massive amount of natural resources.', 'Plastik ve alüminyumu geri dönüştürmek çok büyük miktarda doğal kaynak tasarrufu sağlar.', 1, 1),
                ('Yiğido', '/static/images/mascot_happy.svg', 'How can we encourage our neighborhood community to participate actively?', 'Mahalle topluluğumuzu aktif olarak katılmaya nasıl teşvik edebiliriz?', 2, 0)
            ],
            2: [
                ('Çevre Uzmanı', '🌿', 'We could install labeled recycling bins and organize a weekend cleanup event.', 'Etiketli geri dönüşüm kutuları yerleştirebilir ve hafta sonu çevre temizliği etkinliği düzenleyebiliriz.', 1, 1),
                ('Yiğido', '/static/images/mascot_happy.svg', 'I can create colorful digital flyers and share them on social media.', 'Renkli dijital el ilanları hazırlayıp sosyal medyada paylaşabilirim.', 2, 0)
            ],
            3: [
                ('Çevre Uzmanı', '🌿', 'That would be effective! Small collective actions make a tremendous difference.', 'Bu çok etkili olur! Küçük toplu eylemler muazzam bir fark yaratır.', 1, 1),
                ('Yiğido', '/static/images/mascot_happy.svg', 'Let\'s collaborate and build a greener future together!', 'Birlikte iş birliği yapalım ve daha yeşil bir gelecek inşa edelim!', 2, 0)
            ]
        },
        'question': {
            'question_text': 'What will Yiğido do to raise awareness for the recycling project?',
            'options': ['Create colorful digital flyers for social media', 'Sell plastic bottles', 'Stay at home'],
            'correct_answer': 'Create colorful digital flyers for social media',
            'explanation': 'Yiğido sosyal medyada paylaşmak üzere renkli dijital el ilanları hazırlayacağını belirtti.'
        }
    },
    {
        'level': 'B1',
        'order_in_level': 4,
        'unit_id': 1,
        'title': 'Kültürlerarası Akşam Yemeği',
        'description': 'Dünya mutfakları ve geleneksel lezzetler sohbeti.',
        'icon': '🍲',
        'xp_reward': 20,
        'pages': {
            1: [
                ('Elena', '🥘', 'Welcome to our international food exchange dinner! I cooked Spanish seafood paella.', 'Uluslararası yemek değişimi akşamımıza hoş geldiniz! İspanyol deniz ürünlü paella pişirdim.', 1, 1),
                ('Yiğido', '/static/images/mascot_happy.svg', 'It smells delicious! I brought freshly baked Turkish baklava with pistachios.', 'Çok lezzetli kokuyor! Ben de taze fıstıklı Türk baklavası getirdim.', 2, 0)
            ],
            2: [
                ('Elena', '🥘', 'Baklava is famous around the world for its delicate flaky pastry layers.', 'Baklava narin ve çıtır hamur katmanlarıyla tüm dünyada meşhurdur.', 1, 1),
                ('Yiğido', '/static/images/mascot_happy.svg', 'Sharing traditional cuisine brings people from different backgrounds closer.', 'Geleneksel mutfakları paylaşmak farklı kültürlerden insanları birbirine yakınlaştırır.', 2, 0)
            ],
            3: [
                ('Elena', '🥘', 'I completely agree. Good food is the universal language of friendship!', 'Kesinlikle katılıyorum. Güzel yemek, dostluğun evrensel dilidir!', 1, 1),
                ('Yiğido', '/static/images/mascot_happy.svg', 'Enjoy your meal everyone! Let\'s toast to new friendships.', 'Herkese afiyet olsun! Yeni dostluklarımıza kadeh kaldıralım.', 2, 0)
            ]
        },
        'question': {
            'question_text': 'What traditional dessert did Yiğido bring to the dinner?',
            'options': ['Turkish baklava with pistachios', 'French apple pie', 'Italian gelato'],
            'correct_answer': 'Turkish baklava with pistachios',
            'explanation': 'Yiğido akşam yemeğine fıstıklı Türk baklavası getirdiğini söyledi.'
        }
    },
    {
        'level': 'B1',
        'order_in_level': 5,
        'unit_id': 1,
        'title': 'Müze Rehberi Eşliğinde',
        'description': 'Antik uygarlıklar galerisinde tarihi keşif.',
        'icon': '🏛️',
        'xp_reward': 20,
        'pages': {
            1: [
                ('Müze Rehberi', '🏛️', 'This gallery displays ancient marble statues discovered in underwater ruins.', 'Bu galeri su altı harabelerinde keşfedilen antik mermer heykelleri sergilemektedir.', 1, 1),
                ('Yiğido', '/static/images/mascot_happy.svg', 'The intricate craftsmanship on the drapery and faces is astonishing.', 'Kıyafet kıvrımları ve yüzlerdeki ince işçilik gerçekten şaşırtıcı.', 2, 0)
            ],
            2: [
                ('Müze Rehberi', '🏛️', 'They were submerged in saltwater for two millennia before modern restoration.', 'Modern restorasyondan önce iki bin yıl boyunca tuzlu suyun altında kaldılar.', 1, 1),
                ('Yiğido', '/static/images/mascot_happy.svg', 'How do conservators protect them from deterioration in the open air?', 'Konservatörler onları açık havada bozulmaktan nasıl koruyorlar?', 2, 0)
            ],
            3: [
                ('Müze Rehberi', '🏛️', 'Advanced humidity sensors and custom climate chambers preserve their mineral integrity.', 'Gelişmiş nem sensörleri ve özel iklim odaları mineral bütünlüklerini korur.', 1, 1),
                ('Yiğido', '/static/images/mascot_happy.svg', 'Preserving cultural heritage for future generations is an admirable mission.', 'Kültürel mirası gelecek nesiller için korumak takdire şayan bir görev.', 2, 0)
            ]
        },
        'question': {
            'question_text': 'Where were the ancient marble statues discovered?',
            'options': ['In underwater ruins', 'In a desert cave', 'On top of a volcano'],
            'correct_answer': 'In underwater ruins',
            'explanation': 'Heykellerin su altı harabelerinde ("in underwater ruins") keşfedildiği söylendi.'
        }
    },

    # ==========================================
    # LEVEL B2: İLERİ (5 Stories)
    # ==========================================
    {
        'level': 'B2',
        'order_in_level': 1,
        'unit_id': 1,
        'title': 'Yapay Zeka ve Gelecek',
        'description': 'Yapay zekanın iş gücüne etkisi ve etik sorumluluklar.',
        'icon': '🤖',
        'xp_reward': 20,
        'pages': {
            1: [
                ('Prof. Davis', '🧠', 'Generative models are reshaping workflow productivity across almost every industry.', 'Üretken modeller hemen her sektörde iş akışı verimliliğini yeniden şekillendiriyor.', 1, 1),
                ('Yiğido', '/static/images/mascot_happy.svg', 'Yet critical thinking, empathy and human creativity remain fundamentally irreplaceable.', 'Yine de eleştirel düşünme, empati ve insan yaratıcılığı temelde yeri doldurulamaz kalıyor.', 2, 0)
            ],
            2: [
                ('Prof. Davis', '🧠', 'Do you foresee regulatory frameworks balancing technological innovation with safety?', 'Düzenleyici çerçevenin teknolojik inovasyon ile güvenliği dengeleyeceğini öngörüyor musunuz?', 1, 1),
                ('Yiğido', '/static/images/mascot_happy.svg', 'Transparent algorithms and strict data governance should be non-negotiable standards.', 'Şeffaf algoritmalar ve sıkı veri yönetişimi taviz verilemez standartlar olmalıdır.', 2, 0)
            ],
            3: [
                ('Prof. Davis', '🧠', 'Well stated. Technology must continuously augment human agency rather than displace it.', 'Çok iyi ifade ettin. Teknoloji insan iradesini devre dışı bırakmak yerine daima güçlendirmelidir.', 1, 1),
                ('Yiğido', '/static/images/mascot_happy.svg', 'Responsible innovation is indeed our shared global obligation.', 'Sorumlu inovasyon gerçekten de ortak küresel sorumluluğumuzdur.', 2, 0)
            ]
        },
        'question': {
            'question_text': 'What human qualities does Yiğido emphasize as irreplaceable by AI?',
            'options': ['Critical thinking, empathy and human creativity', 'Speed of data calculation', 'Repetitive typing tasks'],
            'correct_answer': 'Critical thinking, empathy and human creativity',
            'explanation': 'Yiğido eleştirel düşünme, empati ve yaratıcılığın yeri doldurulamaz olduğunu vurguladı.'
        }
    },
    {
        'level': 'B2',
        'order_in_level': 2,
        'unit_id': 1,
        'title': 'Finansal Yatırım ve Girişimcilik',
        'description': 'Bir edtech girişimi için tohum yatırım sunumu değerlendirmesi.',
        'icon': '📈',
        'xp_reward': 20,
        'pages': {
            1: [
                ('Risk Sermayesi', '💼', 'Your pitch demonstrates solid organic growth, but how resilient is your retention model?', 'Sunumunuz güçlü organik büyüme gösteriyor, peki kullanıcı tutundurma modeliniz ne kadar dirençli?', 1, 1),
                ('Yiğido', '/static/images/mascot_happy.svg', 'Our ninety-day retention exceeds benchmark rates because interactive gamification builds daily learning habits.', 'Etkileşimli oyunlaştırma günlük öğrenme alışkanlığı oluşturduğu için 90 günlük tutundurmamız sektör ortalamasının üzerinde.', 2, 0)
            ],
            2: [
                ('Risk Sermayesi', '💼', 'That is compelling evidence. What are your customer acquisition cost projections for Europe?', 'Bu ikna edici bir kanıt. Avrupa için müşteri edinme maliyeti projeksiyonlarınız neler?', 1, 1),
                ('Yiğido', '/static/images/mascot_happy.svg', 'By leveraging organic student referrals and localized micro-influencers, we will maintain low CAC.', 'Öğrenci davetlerini ve yerel mikro-etkileyicileri kullanarak düşük müşteri edinme maliyetini koruyacağız.', 2, 0)
            ],
            3: [
                ('Risk Sermayesi', '💼', 'The financial model looks scalable and viable. Let\'s draft a preliminary term sheet.', 'Finansal model ölçeklenebilir ve uygulanabilir görünüyor. Ön sözleşme taslağı hazırlayalım.', 1, 1),
                ('Yiğido', '/static/images/mascot_happy.svg', 'Thank you! We are thrilled to partner and expand our educational mission.', 'Teşekkür ederim! Eğitim misyonumuzu ortaklıkla büyütmekten büyük heyecan duyuyoruz.', 2, 0)
            ]
        },
        'question': {
            'question_text': 'Why does Yiğido\'s platform maintain strong user retention?',
            'options': ['Interactive gamification builds daily learning habits', 'By giving away free devices', 'By eliminating all practice tests'],
            'correct_answer': 'Interactive gamification builds daily learning habits',
            'explanation': 'Oyunlaştırmanın günlük öğrenme alışkanlığı yaratarak kullanıcıları tuttuğu açıklandı.'
        }
    },
    {
        'level': 'B2',
        'order_in_level': 3,
        'unit_id': 1,
        'title': 'İklim Zirvesi ve Yenilenebilir Enerji',
        'description': 'Net sıfır karbon hedefleri ve sürdürülebilir altyapı.',
        'icon': '🌍',
        'xp_reward': 20,
        'pages': {
            1: [
                ('Panelist', '🌱', 'Phasing out fossil fuel subsidies requires concerted international political resolve.', 'Fosil yakıt sübvansiyonlarını kademeli bitirmek ortak uluslararası siyasi kararlılık gerektirir.', 1, 1),
                ('Yiğido', '/static/images/mascot_happy.svg', 'Reallocating capital towards offshore wind and solar storage will catalyze green modernization.', 'Sermayeyi açık deniz rüzgarı ve güneş depolamasına yönlendirmek yeşil modernleşmeyi hızlandıracaktır.', 2, 0)
            ],
            2: [
                ('Panelist', '🌱', 'How can developing economies ensure energy affordability while pursuing decarbonization?', 'Gelişmekte olan ekonomiler karbonsuzlaşırken enerji erişilebilirliğini nasıl sağlayabilir?', 1, 1),
                ('Yiğido', '/static/images/mascot_happy.svg', 'Concessional green bonds and technology transfer treaties offer an equitable transitional pathway.', 'Düşük faizli yeşil tahviller ve teknoloji transferi anlaşmaları adil bir geçiş yolu sunar.', 2, 0)
            ],
            3: [
                ('Panelist', '🌱', 'Exactly. Multilateral cooperation is indispensable in mitigating planetary risk.', 'Kesinlikle. Gezegensel riski azaltmada çok taraflı iş birliği vazgeçilmezdir.', 1, 1),
                ('Yiğido', '/static/images/mascot_happy.svg', 'Bold climate investments today will ensure prosperity and biodiversity for future generations.', 'Bugünkü cesur iklim yatırımları, gelecek nesiller için refah ve biyoçeşitlilik sağlayacaktır.', 2, 0)
            ]
        },
        'question': {
            'question_text': 'What financing mechanism does Yiğido suggest for developing economies?',
            'options': ['Concessional green bonds and technology transfer treaties', 'Increasing tariffs on clean energy', 'Cutting all renewable funding'],
            'correct_answer': 'Concessional green bonds and technology transfer treaties',
            'explanation': 'Yiğido düşük faizli yeşil tahviller ve teknoloji transferi anlaşmalarını önerdi.'
        }
    },
    {
        'level': 'B2',
        'order_in_level': 4,
        'unit_id': 1,
        'title': 'Kriz Yönetimi ve Halkla İlişkiler',
        'description': 'Hizmet kesintisi sonrası şeffaf ve güven veren kriz iletişimi.',
        'icon': '📢',
        'xp_reward': 20,
        'pages': {
            1: [
                ('İletişim Direktörü', '🎙️', 'Our cloud hosting infrastructure experienced an unprecedented service disruption this morning.', 'Bulut altyapımız bu sabah benzeri görülmemiş bir hizmet kesintisi yaşadı.', 1, 1),
                ('Yiğido', '/static/images/mascot_happy.svg', 'We should promptly release an open incident report detailing the root cause and mitigation steps.', 'Kök nedeni ve çözüm adımlarını detaylandıran açık bir olay raporunu ivedilikle yayınlamalıyız.', 2, 0)
            ],
            2: [
                ('İletişim Direktörü', '🎙️', 'Should we issue automatic service credits to all affected premium subscribers?', 'Etkilenen tüm premium abonelere otomatik hizmet kredisi tanımlamalı mıyız?', 1, 1),
                ('Yiğido', '/static/images/mascot_happy.svg', 'Proactive restitution reinforces transparency and cements long-term customer loyalty.', 'Proaktif telafi şeffaflığı pekiştirir ve uzun vadeli müşteri sadakatini perçinler.', 2, 0)
            ],
            3: [
                ('İletişim Direktörü', '🎙️', 'Agreed. Sincerity and prompt restitution turn crises into trust-building opportunities.', 'Katılıyorum. Samimiyet ve hızlı telafi, krizleri güven inşa etme fırsatlarına dönüştürür.', 1, 1),
                ('Yiğido', '/static/images/mascot_happy.svg', 'Excellence in customer care is tested precisely under such challenging circumstances.', 'Müşteri memnuniyetinde mükemmellik tam da bu tür zorlu koşullarda sınanır.', 2, 0)
            ]
        },
        'question': {
            'question_text': 'Why does Yiğido advocate for proactive customer restitution?',
            'options': ['It reinforces transparency and cements long-term customer loyalty', 'It saves money in the short term', 'It hides the incident from the public'],
            'correct_answer': 'It reinforces transparency and cements long-term customer loyalty',
            'explanation': 'Yiğido proaktif telafinin şeffaflığı pekiştirdiğini ve sadakati güçlendirdiğini belirtti.'
        }
    },
    {
        'level': 'B2',
        'order_in_level': 5,
        'unit_id': 1,
        'title': 'Uzay Keşfi ve Derin Evren',
        'description': 'Uzay teleskobu verileriyle erken kozmik evrenin sırları.',
        'icon': '🚀',
        'xp_reward': 20,
        'pages': {
            1: [
                ('Astrofizikçi', '🔭', 'Spectroscopic observations have revealed primordial galaxies formed shortly after the Big Bang.', 'Spektroskopik gözlemler Büyük Patlama\'dan hemen sonra oluşan ilkel galaksileri ortaya çıkardı.', 1, 1),
                ('Yiğido', '/static/images/mascot_happy.svg', 'Those ancient photons travel across billions of light years to unravel cosmological evolution.', 'O kadim fotonlar kozmolojik evrimi aydınlatmak için milyarlarca ışık yılı yol kat ediyor.', 2, 0)
            ],
            2: [
                ('Astrofizikçi', '🔭', 'Do you think extraterrestrial biosignatures might be detected within our lifetime?', 'Sizce dünya dışı biyo-imzalar bizim ömrümüz içerisinde tespit edilebilir mi?', 1, 1),
                ('Yiğido', '/static/images/mascot_happy.svg', 'Given the myriad exoplanets in habitable zones, statistical probability strongly supports that possibility.', 'Yaşanabilir bölgelerdeki sayısız ötegezegen düşünüldüğünde istatistiksel olasılık bu ihtimali güçlü biçimde destekliyor.', 2, 0)
            ],
            3: [
                ('Astrofizikçi', '🔭', 'It is an exhilarating era to decipher the deep mysteries of our universe.', 'Evrenimizin derin gizemlerini çözmek için heyecan verici bir dönemdeyiz.', 1, 1),
                ('Yiğido', '/static/images/mascot_happy.svg', 'Humanity\'s relentless curiosity will perpetually explore beyond known frontiers.', 'İnsanlığın dinmek bilmeyen merakı bilinen sınırların ötesini daima keşfedecektir.', 2, 0)
            ]
        },
        'question': {
            'question_text': 'Why does Yiğido consider detecting extraterrestrial biosignatures probable?',
            'options': ['Because of the myriad exoplanets located in habitable zones', 'Because space is completely empty', 'Because aliens have already sent emails'],
            'correct_answer': 'Because of the myriad exoplanets located in habitable zones',
            'explanation': 'Yaşanabilir kuşaktaki sayısız ötegezegenin istatistiksel olasılığı artırdığı vurgulandı.'
        }
    }
]

def ensure_schema_migrated():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(users)")
        cols = [c[1] for c in cursor.fetchall()]
        if 'last_heart_loss_time' not in cols:
            cursor.execute("ALTER TABLE users ADD COLUMN last_heart_loss_time TIMESTAMP DEFAULT NULL")
        if 'is_premium' not in cols:
            cursor.execute("ALTER TABLE users ADD COLUMN is_premium INTEGER DEFAULT 0")
        if 'streak_count' not in cols:
            cursor.execute("ALTER TABLE users ADD COLUMN streak_count INTEGER DEFAULT 0")
            cursor.execute("UPDATE users SET streak_count = COALESCE(streak, 0)")
        if 'last_study_date' not in cols:
            cursor.execute("ALTER TABLE users ADD COLUMN last_study_date TEXT DEFAULT NULL")
        if 'referral_code' not in cols:
            cursor.execute("ALTER TABLE users ADD COLUMN referral_code TEXT DEFAULT NULL")
        if 'invited_count' not in cols:
            cursor.execute("ALTER TABLE users ADD COLUMN invited_count INTEGER DEFAULT 0")

        # Migrate referral codes for existing users
        cursor.execute("SELECT id FROM users WHERE referral_code IS NULL OR referral_code = ''")
        for (u_id,) in cursor.fetchall():
            code = f"YGD{u_id:02d}{secrets.token_hex(2).upper()}"
            cursor.execute("UPDATE users SET referral_code = ? WHERE id = ?", (code, u_id))
        cursor.execute("UPDATE users SET invited_count = 0 WHERE invited_count IS NULL")

        # Migrate units table
        cursor.execute("PRAGMA table_info(units)")
        unit_cols = [c[1] for c in cursor.fetchall()]
        if 'order_index' not in unit_cols:
            cursor.execute("ALTER TABLE units ADD COLUMN order_index INTEGER DEFAULT 1")
            cursor.execute("UPDATE units SET order_index = order_num WHERE order_index IS NULL OR order_index = 1")
        if 'is_unlocked' not in unit_cols:
            cursor.execute("ALTER TABLE units ADD COLUMN is_unlocked INTEGER DEFAULT 0")

        # Ensure Unit 1 is unlocked
        cursor.execute("UPDATE units SET is_unlocked = 1, order_index = 1 WHERE order_num = 1 OR order_index = 1")

        # Ensure all 4 units exist
        unit_definitions = [
            (1, 'Ünite 1: İngilizceye Başlangıç (7 Konu + 6 Sınav)', 'Temel Selamlaşma, Tanışma ve Günlük Kalıplar (13 Adım)', '#0284c7', 1),
            (2, 'Ünite 2: Günlük Yaşam & Zaman (A1.2)', 'Saatler, planlar, alışkanlıklar ve temel zaman kalıpları.', '#059669', 0),
            (3, 'Ünite 3: Çevre & İnsanlar (A2.1)', 'Kişi ve mekan tasvirleri, sıfatlar ve temel diyaloglar.', '#d97706', 0),
            (4, 'Ünite 4: Seyahat & Alışveriş (A2.2)', 'Yol tarifleri, sipariş verme, alışveriş ve seyahat kalıpları.', '#7c3aed', 0)
        ]

        for order_idx, title, desc, color, unlocked in unit_definitions:
            cursor.execute("SELECT id FROM units WHERE order_index = ? OR order_num = ?", (order_idx, order_idx))
            row = cursor.fetchone()
            if not row:
                cursor.execute("""
                INSERT INTO units (title, description, color, order_num, order_index, is_unlocked)
                VALUES (?, ?, ?, ?, ?, ?)
                """, (title, desc, color, order_idx, order_idx, unlocked))
            elif order_idx == 1:
                cursor.execute("UPDATE units SET is_unlocked = 1, order_index = 1 WHERE id = ?", (row[0],))

        # Create stories and story_lines tables
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS stories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            unit_id INTEGER NOT NULL,
            level TEXT DEFAULT 'A1',
            order_in_level INTEGER DEFAULT 1,
            title TEXT NOT NULL,
            description TEXT,
            icon TEXT DEFAULT '☕',
            xp_reward INTEGER DEFAULT 20,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (unit_id) REFERENCES units(id)
        )
        ''')

        # Check and migrate columns on stories
        cursor.execute("PRAGMA table_info(stories)")
        stories_cols = [c[1] for c in cursor.fetchall()]
        if 'level' not in stories_cols:
            cursor.execute("ALTER TABLE stories ADD COLUMN level TEXT DEFAULT 'A1'")
        if 'order_in_level' not in stories_cols:
            cursor.execute("ALTER TABLE stories ADD COLUMN order_in_level INTEGER DEFAULT 1")

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS story_lines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            story_id INTEGER NOT NULL,
            page_num INTEGER DEFAULT 1,
            character_name TEXT NOT NULL,
            character_avatar TEXT,
            english_text TEXT NOT NULL,
            turkish_text TEXT NOT NULL,
            order_num INTEGER NOT NULL,
            is_left INTEGER DEFAULT 1,
            FOREIGN KEY (story_id) REFERENCES stories(id)
        )
        ''')

        # Check and migrate columns on story_lines
        cursor.execute("PRAGMA table_info(story_lines)")
        lines_cols = [c[1] for c in cursor.fetchall()]
        if 'page_num' not in lines_cols:
            cursor.execute("ALTER TABLE story_lines ADD COLUMN page_num INTEGER DEFAULT 1")

        # Create story_questions table for Page 2 mini comprehension test
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS story_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            story_id INTEGER NOT NULL,
            question_text TEXT NOT NULL,
            options TEXT NOT NULL,
            correct_answer TEXT NOT NULL,
            explanation TEXT,
            FOREIGN KEY (story_id) REFERENCES stories(id)
        )
        ''')

        # Create user_story_progress table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_story_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            story_id INTEGER NOT NULL,
            completed INTEGER DEFAULT 1,
            completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, story_id),
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (story_id) REFERENCES stories(id)
        )
        ''')

        # Fix legacy row for 'Yiğido Kafede'
        cursor.execute("UPDATE stories SET level = 'A1', order_in_level = 1 WHERE title = 'Yiğido Kafede' AND (level IS NULL OR level = '')")

        # Seed all 20 Stories across A1, A2, B1, B2 (5 stories each)
        for s_data in STORIES_DATA:
            cursor.execute("SELECT id FROM stories WHERE level = ? AND order_in_level = ?", (s_data['level'], s_data['order_in_level']))
            s_row = cursor.fetchone()
            if s_row:
                story_id = s_row[0]
                cursor.execute('''
                UPDATE stories 
                SET title = ?, description = ?, icon = ?, xp_reward = ?, unit_id = ?
                WHERE id = ?
                ''', (s_data['title'], s_data['description'], s_data['icon'], s_data['xp_reward'], s_data.get('unit_id', 1), story_id))
            else:
                cursor.execute('''
                INSERT INTO stories (unit_id, level, order_in_level, title, description, icon, xp_reward)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (s_data.get('unit_id', 1), s_data['level'], s_data['order_in_level'], s_data['title'], s_data['description'], s_data['icon'], s_data['xp_reward']))
                story_id = cursor.lastrowid

            # Sync dialogue lines for 3 pages
            cursor.execute("DELETE FROM story_lines WHERE story_id = ?", (story_id,))
            for p_num in (1, 2, 3):
                for c_name, c_avatar, en, tr, o_num, is_l in s_data['pages'].get(p_num, []):
                    cursor.execute('''
                    INSERT INTO story_lines (story_id, page_num, character_name, character_avatar, english_text, turkish_text, order_num, is_left)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (story_id, p_num, c_name, c_avatar, en, tr, o_num, is_l))

            # Sync question for Page 2
            q = s_data['question']
            cursor.execute("DELETE FROM story_questions WHERE story_id = ?", (story_id,))
            cursor.execute('''
            INSERT INTO story_questions (story_id, question_text, options, correct_answer, explanation)
            VALUES (?, ?, ?, ?, ?)
            ''', (story_id, q['question_text'], json.dumps(q['options'], ensure_ascii=False), q['correct_answer'], q['explanation']))

        conn.commit()
        conn.close()
    except Exception as e:
        print("Schema migration error:", e)

ensure_schema_migrated()

def generate_unique_referral_code(conn):
    for _ in range(100):
        code = f"YGD{secrets.token_hex(3).upper()}"
        row = conn.execute("SELECT id FROM users WHERE referral_code = ?", (code,)).fetchone()
        if not row:
            return code
    return f"YGD{int(datetime.datetime.now().timestamp())}"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def sync_user_hearts(conn, user):
    """
    Calculates heart regeneration based on 15-minute intervals (900 seconds).
    For every 15 minutes elapsed since last_heart_loss_time, +1 heart is granted up to max_hearts (5).
    If user is premium (is_premium=1), hearts are infinite and always 5/5.
    Returns (current_hearts, max_hearts, remaining_seconds, is_full)
    """
    if not user:
        return 5, 5, 0, True

    user_keys = user.keys() if hasattr(user, 'keys') else []
    is_premium = bool(user['is_premium']) if 'is_premium' in user_keys else False

    if is_premium:
        if user['hearts'] < 5 or user['last_heart_loss_time'] is not None:
            conn.execute('UPDATE users SET hearts = 5, last_heart_loss_time = NULL WHERE id = ?', (user['id'],))
            conn.commit()
        return 5, 5, 0, True

    hearts = user['hearts']
    max_hearts = user['max_hearts'] if user['max_hearts'] is not None else 5
    last_loss = user['last_heart_loss_time'] if 'last_heart_loss_time' in user_keys else None

    if hearts >= max_hearts:
        if last_loss is not None:
            conn.execute('UPDATE users SET last_heart_loss_time = NULL WHERE id = ?', (user['id'],))
            conn.commit()
        return max_hearts, max_hearts, 0, True

    now = datetime.datetime.now()

    if not last_loss:
        conn.execute('UPDATE users SET last_heart_loss_time = ? WHERE id = ?', (now.isoformat(), user['id']))
        conn.commit()
        return hearts, max_hearts, HEART_REFILL_INTERVAL, False

    try:
        last_time = datetime.datetime.fromisoformat(str(last_loss))
    except Exception:
        last_time = now
        conn.execute('UPDATE users SET last_heart_loss_time = ? WHERE id = ?', (now.isoformat(), user['id']))
        conn.commit()

    elapsed = (now - last_time).total_seconds()
    if elapsed < 0:
        elapsed = 0

    earned_hearts = int(elapsed // HEART_REFILL_INTERVAL)

    if earned_hearts > 0:
        new_hearts = min(max_hearts, hearts + earned_hearts)
        if new_hearts >= max_hearts:
            new_last_loss = None
            remaining_seconds = 0
            is_full = True
        else:
            new_last_time = last_time + datetime.timedelta(seconds=earned_hearts * HEART_REFILL_INTERVAL)
            new_last_loss = new_last_time.isoformat()
            remaining_seconds = max(0, int(HEART_REFILL_INTERVAL - (now - new_last_time).total_seconds()))
            is_full = False

        conn.execute('UPDATE users SET hearts = ?, last_heart_loss_time = ? WHERE id = ?', 
                     (new_hearts, new_last_loss, user['id']))
        conn.commit()
        return new_hearts, max_hearts, remaining_seconds, is_full
    else:
        remaining_seconds = max(0, int(HEART_REFILL_INTERVAL - elapsed))
        return hearts, max_hearts, remaining_seconds, False

def get_or_create_default_user(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = 1')
    user = cursor.fetchone()
    if not user:
        cursor.execute('''
        INSERT INTO users (id, username, name, email, google_id, hearts, max_hearts, xp, streak, daily_goal, bio, referral_code, invited_count)
        VALUES (1, 'misafir', 'Misafir Öğrenci', NULL, NULL, 5, 5, 0, 1, 50, 'İngilizce öğrenmeye yeni başladım! 🐻', 'YGDMISAFIR', 0)
        ''')
        conn.commit()
        cursor.execute('SELECT * FROM users WHERE id = 1')
        user = cursor.fetchone()
    elif not user['referral_code']:
        cursor.execute("UPDATE users SET referral_code = 'YGDMISAFIR' WHERE id = 1")
        conn.commit()
        cursor.execute('SELECT * FROM users WHERE id = 1')
        user = cursor.fetchone()
    return user

def is_guest_user(user):
    if not user:
        return True
    return bool(user['google_id'] is None or user['google_id'] == '')

# @login_required Decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not g.user:
            session['next_url'] = request.url
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.before_request
def load_logged_in_user():
    if request.path.startswith('/static'):
        return

    ref_param = request.args.get('ref')
    if ref_param:
        session['pending_ref'] = ref_param.strip()

    user_id = session.get('user_id')
    conn = get_db_connection()

    if user_id is not None:
        user_row = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    else:
        user_row = None

    # Auto-initialize Guest session for visitors who don't have an active session!
    # (Except when explicitly on login / oauth routes)
    if user_row is None and request.endpoint not in ['login', 'login_google', 'authorize', 'register']:
        guest = get_or_create_default_user(conn)
        session['user_id'] = guest['id']
        session['is_guest'] = True
        user_row = guest

    if user_row:
        if not user_row['referral_code']:
            new_ref = generate_unique_referral_code(conn)
            conn.execute('UPDATE users SET referral_code = ? WHERE id = ?', (new_ref, user_row['id']))
            conn.commit()
            user_row = conn.execute('SELECT * FROM users WHERE id = ?', (user_row['id'],)).fetchone()
        hearts, max_h, remaining_sec, is_full = sync_user_hearts(conn, user_row)
        g.user = conn.execute('SELECT * FROM users WHERE id = ?', (user_row['id'],)).fetchone()
        g.heart_remaining_seconds = remaining_sec
        g.is_hearts_full = is_full
    else:
        g.user = None
        g.heart_remaining_seconds = 0
        g.is_hearts_full = True

    conn.close()

@app.context_processor
def inject_user_and_config():
    is_google_configured = bool(google_client_id and google_client_secret)
    is_guest = is_guest_user(g.user)
    is_user_premium = bool(g.user and ('is_premium' in g.user.keys() and g.user['is_premium']))
    today_str = datetime.date.today().strftime('%Y-%m-%d')
    has_studied_today = False
    user_streak_count = 0
    if g.user:
        user_keys = g.user.keys() if hasattr(g.user, 'keys') else []
        last_date = g.user['last_study_date'] if 'last_study_date' in user_keys else None
        has_studied_today = (last_date == today_str)
        if 'streak_count' in user_keys and g.user['streak_count'] is not None:
            user_streak_count = g.user['streak_count']
        elif 'streak' in user_keys and g.user['streak'] is not None:
            user_streak_count = g.user['streak']

    return {
        'current_user': g.user,
        'google_configured': is_google_configured,
        'is_guest': is_guest,
        'is_premium': is_user_premium,
        'today_str': today_str,
        'has_studied_today': has_studied_today,
        'streak_count': user_streak_count,
        'heart_remaining_seconds': getattr(g, 'heart_remaining_seconds', 0),
        'is_hearts_full': getattr(g, 'is_hearts_full', True)
    }

# ----------------- Authentication Routes -----------------

@app.route('/login')
def login():
    if g.user and not is_guest_user(g.user):
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login/google')
def login_google():
    if not (google_client_id and google_client_secret):
        return redirect(url_for('login', error='not_configured'))
    
    redirect_uri = url_for('authorize', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    if not (google_client_id and google_client_secret):
        return redirect(url_for('login', error='not_configured'))

    try:
        token = oauth.google.authorize_access_token()
        user_info = token.get('userinfo')
        if not user_info:
            try:
                user_info = oauth.google.parse_id_token(token)
            except Exception:
                pass
        if not user_info:
            resp = oauth.google.get('https://openidconnect.googleapis.com/v1/userinfo')
            user_info = resp.json()

        google_id = user_info.get('sub') or user_info.get('id')
        email = user_info.get('email')
        name = user_info.get('name') or (email.split('@')[0] if email else 'Öğrenci')
        avatar = user_info.get('picture', '')

        if not email and not google_id:
            return redirect(url_for('login', error='no_email'))

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check existing user by google_id or email
        cursor.execute('SELECT * FROM users WHERE google_id = ? OR email = ?', (google_id, email))
        user = cursor.fetchone()

        if user:
            cursor.execute('''
            UPDATE users SET name = ?, avatar = ?, google_id = ? WHERE id = ?
            ''', (name, avatar, google_id, user['id']))
            user_id = user['id']
        else:
            # Create new user with 5 hearts and 0 XP
            new_ref_code = generate_unique_referral_code(conn)
            cursor.execute('''
            INSERT INTO users (username, name, email, google_id, avatar, hearts, max_hearts, xp, streak, daily_goal, bio, referral_code, invited_count)
            VALUES (?, ?, ?, ?, ?, 5, 5, 0, 1, 50, 'Her gün yeni bir İngilizce kelime öğreniyorum! 🌊🐻', ?, 0)
            ''', (name, name, email, google_id, avatar, new_ref_code))
            user_id = cursor.lastrowid

            # Apply pending referral if newly registered via Google
            pending_ref = session.pop('pending_ref', None)
            if pending_ref:
                inviter = conn.execute("SELECT id, invited_count, is_premium FROM users WHERE referral_code = ?", (pending_ref,)).fetchone()
                if inviter and inviter['id'] != user_id:
                    new_count = (inviter['invited_count'] or 0) + 1
                    new_premium = 1 if new_count >= 10 else (inviter['is_premium'] or 0)
                    cursor.execute("UPDATE users SET invited_count = ?, is_premium = ? WHERE id = ?",
                                   (new_count, new_premium, inviter['id']))

        conn.commit()
        conn.close()

        session['user_id'] = user_id
        next_url = session.pop('next_url', None)
        return redirect(next_url or url_for('dashboard'))

    except Exception as e:
        print('OAuth Callback Error:', e)
        return redirect(url_for('login', error='oauth_failed'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    conn = get_db_connection()
    ref_code = (request.args.get('ref') or request.form.get('ref') or '').strip()

    if ref_code:
        session['pending_ref'] = ref_code

    req_username = request.form.get('username') or request.args.get('username')
    req_name = request.form.get('name') or request.args.get('name')
    req_email = request.form.get('email') or request.args.get('email')

    # Register new user whenever ref is provided, or method is POST, or registration parameters provided
    if ref_code or request.method == 'POST' or req_username:
        rand_suffix = secrets.token_hex(3)
        username = req_username or f"ogrenci_{rand_suffix}"
        name = req_name or f"Yeni Öğrenci {rand_suffix[:4].upper()}"
        email = req_email or None

        while conn.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone():
            username = f"ogrenci_{secrets.token_hex(4)}"

        new_ref_code = generate_unique_referral_code(conn)
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO users (username, name, email, hearts, max_hearts, xp, streak, daily_goal, bio, referral_code, invited_count)
        VALUES (?, ?, ?, 5, 5, 0, 1, 50, 'YiğidoBear ile İngilizce öğreniyorum! 🐻', ?, 0)
        ''', (username, name, email, new_ref_code))
        new_user_id = cursor.lastrowid
        conn.commit()

        # Davet edenin sayısını artır; 10 olunca is_premium = 1 yap
        if ref_code:
            inviter = conn.execute(
                "SELECT id, invited_count, is_premium FROM users WHERE referral_code = ?",
                (ref_code,)
            ).fetchone()
            if inviter and inviter['id'] != new_user_id:
                new_count = (inviter['invited_count'] or 0) + 1
                new_premium = 1 if new_count >= 10 else (inviter['is_premium'] or 0)
                conn.execute(
                    "UPDATE users SET invited_count = ?, is_premium = ? WHERE id = ?",
                    (new_count, new_premium, inviter['id'])
                )
                conn.commit()

        conn.close()

        session.clear()
        session['user_id'] = new_user_id
        session['is_guest'] = False

        if request.headers.get('Accept') == 'application/json' or request.is_json:
            return jsonify({
                'success': True,
                'user_id': new_user_id,
                'username': username,
                'referral_code': new_ref_code
            })

        return redirect(url_for('dashboard', welcome='referred' if ref_code else 'new'))

    conn.close()
    return redirect(url_for('login'))

@app.route('/login/demo')
def login_demo():
    # Instant authenticated user login for demo / testing
    user_target = request.args.get('user')
    conn = get_db_connection()
    if user_target == 'standard':
        user = conn.execute("SELECT * FROM users WHERE google_id IS NOT NULL AND (is_premium = 0 OR is_premium IS NULL) LIMIT 1").fetchone()
        if not user:
            conn.execute('''
            INSERT INTO users (username, name, email, google_id, hearts, max_hearts, xp, streak, daily_goal, bio, is_premium)
            VALUES ('demo_student', 'Demo Standart Öğrenci', 'student@google.com', 'google-student-12345', 5, 5, 30, 2, 50, 'Standart öğrenci hesabı', 0)
            ''')
            conn.commit()
            user = conn.execute("SELECT * FROM users WHERE google_id = 'google-student-12345' LIMIT 1").fetchone()
    elif user_target in ('premium', 'yigit'):
        user = conn.execute("SELECT * FROM users WHERE is_premium = 1 LIMIT 1").fetchone()
    else:
        user = conn.execute("SELECT * FROM users WHERE google_id IS NOT NULL LIMIT 1").fetchone()
        if not user:
            conn.execute('''
            INSERT INTO users (username, name, email, google_id, hearts, max_hearts, xp, streak, daily_goal, bio)
            VALUES ('demo_user', 'Demo Google Öğrenci', 'demo@google.com', 'google-demo-12345', 5, 5, 50, 3, 50, 'Google ile giriş yaptım!')
            ''')
            conn.commit()
            user = conn.execute("SELECT * FROM users WHERE google_id IS NOT NULL LIMIT 1").fetchone()
    session['user_id'] = user['id']
    session['is_guest'] = False
    conn.close()
    next_url = session.pop('next_url', None)
    return redirect(next_url or url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# ----------------- Profile Routes -----------------

@app.route('/profile')
@login_required
def profile():
    user = g.user
    conn = get_db_connection()

    # Completed topics (regular lessons) count
    comp_topics = conn.execute('''
    SELECT COUNT(*) FROM user_progress up
    JOIN lessons l ON up.lesson_id = l.id
    WHERE up.user_id = ? AND up.completed = 1 AND l.is_exam = 0
    ''', (user['id'],)).fetchone()[0]

    # Completed exams count
    comp_exams = conn.execute('''
    SELECT COUNT(*) FROM user_progress up
    JOIN lessons l ON up.lesson_id = l.id
    WHERE up.user_id = ? AND up.completed = 1 AND l.is_exam = 1
    ''', (user['id'],)).fetchone()[0]

    total_lessons = conn.execute('SELECT COUNT(*) FROM lessons').fetchone()[0]
    total_completed = comp_topics + comp_exams
    completion_rate = round((total_completed / total_lessons * 100)) if total_lessons > 0 else 0

    conn.close()

    stats = {
        'completed_topics': comp_topics,
        'completed_exams': comp_exams,
        'total_completed': total_completed,
        'total_lessons': total_lessons,
        'completion_rate': completion_rate
    }

    return render_template('profile.html', user=user, stats=stats)

@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def profile_edit():
    user = g.user
    conn = get_db_connection()

    if request.method == 'POST':
        name = request.form.get('name', '').strip() or user['name'] or user['username']
        bio = request.form.get('bio', '').strip()
        try:
            daily_goal = int(request.form.get('daily_goal', 50))
            if daily_goal not in [10, 20, 50]:
                daily_goal = 50
        except ValueError:
            daily_goal = 50

        conn.execute('''
        UPDATE users SET name = ?, daily_goal = ?, bio = ? WHERE id = ?
        ''', (name, daily_goal, bio, user['id']))
        conn.commit()
        conn.close()

        return redirect(url_for('profile', updated='1'))

    conn.close()
    return render_template('profile_edit.html', user=user)

# ----------------- Dashboard & Curriculum Roadmap -----------------

@app.route('/')
def index():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
@login_required
def dashboard():
    user = g.user
    conn = get_db_connection()

    # Get completed lessons set for user
    progress_rows = conn.execute(
        'SELECT lesson_id, completed FROM user_progress WHERE user_id = ? AND completed = 1',
        (user['id'],)
    ).fetchall()
    completed_lesson_ids = {row['lesson_id'] for row in progress_rows}

    # Unlock Unit 2 if user completed Boss Exam of Unit 1
    boss_lesson = conn.execute(
        "SELECT id FROM lessons WHERE (order_num = 13 OR title LIKE '%Boss%') LIMIT 1"
    ).fetchone()
    if boss_lesson and boss_lesson['id'] in completed_lesson_ids:
        conn.execute("UPDATE units SET is_unlocked = 1 WHERE order_index = 2 OR order_num = 2")
        conn.commit()

    # Get all units
    units_rows = conn.execute('SELECT * FROM units ORDER BY COALESCE(order_index, order_num) ASC').fetchall()
    units_data = []

    # Strict sequential unlocking:
    # A step is 'completed' if its id is in completed_lesson_ids.
    # The first uncompleted step is 'active'.
    # All subsequent steps are 'locked'.
    active_found = False
    current_unit_identified = False

    for unit in units_rows:
        u_order = unit['order_index'] if 'order_index' in unit.keys() else unit['order_num']
        u_unlocked = bool(unit['is_unlocked']) or (u_order == 1)

        lessons_rows = conn.execute(
            'SELECT * FROM lessons WHERE unit_id = ? ORDER BY order_num ASC',
            (unit['id'],)
        ).fetchall()

        lessons_list = []
        unit_all_completed = len(lessons_rows) > 0 and all(l['id'] in completed_lesson_ids for l in lessons_rows)
        unit_has_active = False

        if u_unlocked and lessons_rows:
            for lesson in lessons_rows:
                l_id = lesson['id']
                if l_id in completed_lesson_ids:
                    status = 'completed'
                elif not active_found:
                    status = 'active'
                    active_found = True
                    unit_has_active = True
                else:
                    status = 'locked'

                lessons_list.append({
                    'id': lesson['id'],
                    'title': lesson['title'],
                    'description': lesson['description'],
                    'is_exam': lesson['is_exam'],
                    'difficulty': lesson['difficulty'],
                    'icon': lesson['icon'],
                    'xp_reward': lesson['xp_reward'],
                    'order_num': lesson['order_num'],
                    'status': status
                })

        is_current = False
        if u_unlocked and not current_unit_identified:
            if unit_has_active or not unit_all_completed or len(lessons_rows) == 0:
                is_current = True
                current_unit_identified = True

        units_data.append({
            'id': unit['id'],
            'title': unit['title'],
            'description': unit['description'],
            'color': unit['color'],
            'order_index': u_order,
            'is_unlocked': u_unlocked,
            'is_current': is_current,
            'is_completed': unit_all_completed,
            'lessons': lessons_list
        })

    # Fallback for current unit
    if not current_unit_identified and units_data:
        for u in units_data:
            if u['is_unlocked']:
                u['is_current'] = True
                break

    # Determine selected unit for main stream view
    requested_unit_id = request.args.get('unit', type=int)
    selected_unit = None
    if requested_unit_id:
        for u in units_data:
            if u['id'] == requested_unit_id and u['is_unlocked']:
                selected_unit = u
                break

    if not selected_unit:
        for u in units_data:
            if u['is_current']:
                selected_unit = u
                break

    if not selected_unit and units_data:
        selected_unit = units_data[0]

    # Stats for dashboard sidebar
    completed_total = len(completed_lesson_ids)
    # Unit 1 has 13 steps; total steps count from unlocked units with lessons
    total_steps = sum(len(u['lessons']) for u in units_data if u['lessons']) or 13

    # Leaderboard: En yüksek XP'ye sahip ilk 5 kullanıcı
    leaderboard = conn.execute('''
        SELECT id, username, name, avatar, xp
        FROM users
        ORDER BY xp DESC, id ASC
        LIMIT 5
    ''').fetchall()

    # Aktif kullanıcının sırası
    user_rank = 1
    if user:
        rank_row = conn.execute('''
            SELECT COUNT(*) + 1 AS rank
            FROM users
            WHERE xp > (SELECT xp FROM users WHERE id = ?)
               OR (xp = (SELECT xp FROM users WHERE id = ?) AND id < ?)
        ''', (user['id'], user['id'], user['id'])).fetchone()
        if rank_row:
            user_rank = rank_row['rank']

    completed_stories_count = 0
    if user:
        c_story_row = conn.execute('SELECT COUNT(DISTINCT story_id) as cnt FROM user_story_progress WHERE user_id = ? AND completed = 1', (user['id'],)).fetchone()
        if c_story_row:
            completed_stories_count = c_story_row['cnt']

    conn.close()
    return render_template('dashboard.html', user=user, units=units_data,
                           selected_unit=selected_unit,
                           completed_total=completed_total, total_steps=total_steps,
                           leaderboard=leaderboard, user_rank=user_rank,
                           completed_stories_count=completed_stories_count)

@app.route('/unit/<int:unit_id>')
@login_required
def unit_view(unit_id):
    conn = get_db_connection()
    unit = conn.execute('SELECT * FROM units WHERE id = ?', (unit_id,)).fetchone()
    if not unit:
        conn.close()
        return redirect(url_for('dashboard', locked='not_found'))

    user = g.user
    unit_order = unit['order_index'] if 'order_index' in unit.keys() else unit['order_num']

    # Unit 1 is always unlocked
    is_unlocked = bool(unit['is_unlocked']) if 'is_unlocked' in unit.keys() else False
    if unit_order == 1:
        is_unlocked = True

    if not is_unlocked:
        # Check if user completed previous unit's boss test
        prev_unit = conn.execute(
            'SELECT id FROM units WHERE order_index = ? OR order_num = ?',
            (unit_order - 1, unit_order - 1)
        ).fetchone()

        if prev_unit:
            boss_lesson = conn.execute(
                'SELECT id FROM lessons WHERE unit_id = ? ORDER BY order_num DESC LIMIT 1',
                (prev_unit['id'],)
            ).fetchone()
            if boss_lesson:
                prog = conn.execute(
                    'SELECT completed FROM user_progress WHERE user_id = ? AND lesson_id = ? AND completed = 1',
                    (user['id'], boss_lesson['id'])
                ).fetchone()
                if prog:
                    is_unlocked = True
                    conn.execute('UPDATE units SET is_unlocked = 1 WHERE id = ?', (unit['id'],))
                    conn.commit()

    conn.close()
    if not is_unlocked:
        return redirect(url_for('dashboard', locked='unit_locked'))

    return redirect(url_for('dashboard', unit=unit_id))

# ----------------- Stories Module (Seviyeli Hikaye Kütüphanesi & Akış) -----------------

@app.route('/stories')
@login_required
def stories_library():
    conn = get_db_connection()
    user = g.user

    # Fetch completed story IDs for the active user
    completed_rows = conn.execute(
        'SELECT story_id FROM user_story_progress WHERE user_id = ? AND completed = 1',
        (user['id'],)
    ).fetchall()
    completed_story_ids = set(r['story_id'] for r in completed_rows)
    total_completed = len(completed_story_ids)

    levels_config = [
        {
            'code': 'A1',
            'title': 'Başlangıç Seviyesi',
            'badge': 'A1 • Beginner',
            'desc': 'Kafede sipariş, parkta tanışma, manav alışverişi ve günlük pratik diyaloglar.',
            'icon': '🌱',
            'prev_level': None,
            'color': '#0284c7'
        },
        {
            'code': 'A2',
            'title': 'Temel Seviye',
            'badge': 'A2 • Elementary',
            'desc': 'Kütüphane, hafta sonu kampı, doktor kontrolü ve seyahat diyalogları.',
            'icon': '🌿',
            'prev_level': 'A1',
            'color': '#059669'
        },
        {
            'code': 'B1',
            'title': 'Orta Seviye',
            'badge': 'B1 • Intermediate',
            'desc': 'İş mülakatı, otel rezervasyonu, sıfır atık projesi ve kültürel etkinlikler.',
            'icon': '🌲',
            'prev_level': 'A2',
            'color': '#d97706'
        },
        {
            'code': 'B2',
            'title': 'İleri Seviye',
            'badge': 'B2 • Upper-Intermediate',
            'desc': 'Yapay zeka etiği, tohum yatırım, iklim paneli ve derin uzay araştırmaları.',
            'icon': '🌟',
            'prev_level': 'B1',
            'color': '#7c3aed'
        }
    ]

    levels_data = []
    default_active_level = 'A1'
    found_active = False

    for lvl in levels_config:
        stories_rows = conn.execute(
            'SELECT * FROM stories WHERE level = ? ORDER BY order_in_level ASC',
            (lvl['code'],)
        ).fetchall()

        # Check if level is unlocked:
        # A1 is always unlocked. A2, B1, B2 require all 5 stories of previous level to be completed.
        if lvl['prev_level'] is None:
            is_unlocked = True
        else:
            prev_stories = conn.execute(
                'SELECT id FROM stories WHERE level = ?',
                (lvl['prev_level'],)
            ).fetchall()
            is_unlocked = (len(prev_stories) >= 5 and all(s['id'] in completed_story_ids for s in prev_stories))

        level_stories = []
        completed_in_level = 0
        level_has_active_story = False

        for idx, s in enumerate(stories_rows):
            is_completed = s['id'] in completed_story_ids
            if is_completed:
                completed_in_level += 1

            # Story status within level:
            # If level is locked -> story is locked (🔒)
            # If level is unlocked:
            # - completed: ✓
            # - first uncompleted: 'active' ("Oku" with pulse)
            # - subsequent: 'locked' (🔒)
            if not is_unlocked:
                story_status = 'locked'
            elif is_completed:
                story_status = 'completed'
            elif idx == 0 or (idx > 0 and stories_rows[idx - 1]['id'] in completed_story_ids):
                if not level_has_active_story:
                    story_status = 'active'
                    level_has_active_story = True
                else:
                    story_status = 'open'
            else:
                story_status = 'locked'

            level_stories.append({
                'id': s['id'],
                'level': s['level'],
                'order_in_level': s['order_in_level'],
                'title': s['title'],
                'description': s['description'],
                'icon': s['icon'],
                'xp_reward': s['xp_reward'],
                'status': story_status
            })

        total_in_level = len(stories_rows)
        percent = int((completed_in_level / total_in_level) * 100) if total_in_level > 0 else 0
        is_all_completed = (total_in_level > 0 and completed_in_level == total_in_level)

        if is_unlocked and not is_all_completed and not found_active:
            default_active_level = lvl['code']
            found_active = True

        levels_data.append({
            'code': lvl['code'],
            'title': lvl['title'],
            'badge': lvl['badge'],
            'desc': lvl['desc'],
            'icon': lvl['icon'],
            'color': lvl['color'],
            'prev_level': lvl['prev_level'],
            'is_unlocked': is_unlocked,
            'is_all_completed': is_all_completed,
            'completed_count': completed_in_level,
            'total_count': total_in_level,
            'percent': percent,
            'stories': level_stories
        })

    conn.close()

    requested_level = request.args.get('level', '').upper()
    active_level = requested_level if requested_level in ['A1', 'A2', 'B1', 'B2'] else default_active_level

    return render_template('stories.html',
                           user=user,
                           levels=levels_data,
                           active_level=active_level,
                           total_completed=total_completed)

@app.route('/story')
@login_required
def story_redirect():
    return redirect(url_for('stories_library'))

@app.route('/story/<int:story_id>')
@login_required
def story_view(story_id):
    conn = get_db_connection()
    user = g.user

    story = conn.execute('SELECT * FROM stories WHERE id = ?', (story_id,)).fetchone()
    if not story:
        conn.close()
        return redirect(url_for('stories_library'))

    # Check lock status
    level = story['level']
    order = story['order_in_level']

    completed_rows = conn.execute(
        'SELECT story_id FROM user_story_progress WHERE user_id = ? AND completed = 1',
        (user['id'],)
    ).fetchall()
    completed_ids = set(r['story_id'] for r in completed_rows)

    # Check level unlock
    prev_map = {'A2': 'A1', 'B1': 'A2', 'B2': 'B1'}
    prev_lvl = prev_map.get(level)
    level_unlocked = True
    if prev_lvl:
        prev_stories = conn.execute('SELECT id FROM stories WHERE level = ?', (prev_lvl,)).fetchall()
        level_unlocked = len(prev_stories) >= 5 and all(s['id'] in completed_ids for s in prev_stories)

    # Check story unlock within level
    story_unlocked = False
    if level_unlocked:
        if order == 1:
            story_unlocked = True
        else:
            prev_in_level = conn.execute('SELECT id FROM stories WHERE level = ? AND order_in_level = ?', (level, order - 1)).fetchone()
            if prev_in_level and prev_in_level['id'] in completed_ids:
                story_unlocked = True
            elif story['id'] in completed_ids:
                story_unlocked = True

    if not story_unlocked:
        conn.close()
        return redirect(url_for('stories_library', level=level, locked=1))

    # Fetch 3-page dialogue lines
    page1_rows = conn.execute('SELECT * FROM story_lines WHERE story_id = ? AND page_num = 1 ORDER BY order_num ASC', (story_id,)).fetchall()
    page2_rows = conn.execute('SELECT * FROM story_lines WHERE story_id = ? AND page_num = 2 ORDER BY order_num ASC', (story_id,)).fetchall()
    page3_rows = conn.execute('SELECT * FROM story_lines WHERE story_id = ? AND page_num = 3 ORDER BY order_num ASC', (story_id,)).fetchall()

    page1_lines = [dict(r) for r in page1_rows]
    page2_lines = [dict(r) for r in page2_rows]
    page3_lines = [dict(r) for r in page3_rows]

    # Fetch Question for Page 2
    q_row = conn.execute('SELECT * FROM story_questions WHERE story_id = ? LIMIT 1', (story_id,)).fetchone()
    question_data = None
    if q_row:
        question_data = dict(q_row)
        try:
            question_data['options'] = json.loads(q_row['options'])
        except Exception:
            question_data['options'] = []

    is_completed = story['id'] in completed_ids

    # Find next story id (same level order+1, or next level order 1)
    next_story = conn.execute(
        'SELECT id, title, level, order_in_level FROM stories WHERE level = ? AND order_in_level = ?',
        (level, order + 1)
    ).fetchone()

    conn.close()

    return render_template('story.html',
                           user=user,
                           story=story,
                           page1_lines=page1_lines,
                           page2_lines=page2_lines,
                           page3_lines=page3_lines,
                           question=question_data,
                           is_completed=is_completed,
                           next_story=next_story)

@app.route('/api/story/<int:story_id>/complete', methods=['POST'])
@login_required
def api_complete_story(story_id):
    conn = get_db_connection()
    user = g.user

    story = conn.execute('SELECT * FROM stories WHERE id = ?', (story_id,)).fetchone()
    if not story:
        conn.close()
        return jsonify({'error': 'Hikaye bulunamadı'}), 404

    xp_reward = story['xp_reward'] if story and 'xp_reward' in story.keys() and story['xp_reward'] is not None else 20

    # Check if previously completed
    existing = conn.execute(
        'SELECT id FROM user_story_progress WHERE user_id = ? AND story_id = ?',
        (user['id'], story_id)
    ).fetchone()

    already_done = bool(existing)
    if not already_done:
        conn.execute(
            'INSERT INTO user_story_progress (user_id, story_id, completed) VALUES (?, ?, 1)',
            (user['id'], story_id)
        )

    # Award XP and update streak
    today_str = datetime.date.today().strftime('%Y-%m-%d')
    yesterday_str = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')

    user_keys = user.keys() if hasattr(user, 'keys') else []
    current_xp = user['xp'] if 'xp' in user_keys and user['xp'] is not None else 0
    xp_to_add = 0 if already_done else xp_reward
    new_xp = current_xp + xp_to_add

    last_study = user['last_study_date'] if 'last_study_date' in user_keys else None
    current_streak = user['streak_count'] if 'streak_count' in user_keys and user['streak_count'] is not None else (user['streak'] if 'streak' in user_keys and user['streak'] is not None else 0)

    if not last_study or last_study < yesterday_str:
        new_streak = 1
    elif last_study == yesterday_str:
        new_streak = current_streak + 1
    else:
        new_streak = max(1, current_streak)

    conn.execute('''
    UPDATE users 
    SET xp = ?, streak = ?, streak_count = ?, last_study_date = ? 
    WHERE id = ?
    ''', (new_xp, new_streak, new_streak, today_str, user['id']))

    # Check if a new level was unlocked by completing this story
    unlocked_new_level = None
    level = story['level']
    comp_count_row = conn.execute(
        'SELECT COUNT(*) as cnt FROM user_story_progress usp JOIN stories s ON usp.story_id = s.id WHERE usp.user_id = ? AND s.level = ?',
        (user['id'], level)
    ).fetchone()
    comp_in_level = comp_count_row['cnt'] if comp_count_row else 0

    if comp_in_level >= 5:
        level_progression = {'A1': 'A2', 'A2': 'B1', 'B1': 'B2'}
        next_lvl = level_progression.get(level)
        if next_lvl:
            unlocked_new_level = next_lvl

    # Find next story ID to offer seamless navigation
    next_story_row = conn.execute(
        'SELECT id FROM stories WHERE level = ? AND order_in_level = ?',
        (level, story['order_in_level'] + 1)
    ).fetchone()
    next_story_id = next_story_row['id'] if next_story_row else None
    if not next_story_id and unlocked_new_level:
        first_of_next = conn.execute(
            'SELECT id FROM stories WHERE level = ? AND order_in_level = 1',
            (unlocked_new_level,)
        ).fetchone()
        if first_of_next:
            next_story_id = first_of_next['id']

    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'already_completed': already_done,
        'xp_gained': xp_to_add,
        'total_xp': new_xp,
        'streak': new_streak,
        'streak_count': new_streak,
        'unlocked_new_level': unlocked_new_level,
        'next_story_id': next_story_id,
        'today_str': today_str
    })

@app.route('/lesson/<int:lesson_id>')
def lesson_view(lesson_id):
    conn = get_db_connection()
    lesson = conn.execute('SELECT * FROM lessons WHERE id = ?', (lesson_id,)).fetchone()
    
    if not lesson:
        conn.close()
        return redirect(url_for('dashboard'))

    user = g.user
    is_guest = is_guest_user(user)

    # If user is a guest:
    if is_guest:
        # A guest can ONLY open Lesson 1 (Demo)
        if lesson['order_num'] == 1:
            unit = conn.execute('SELECT * FROM units WHERE id = ?', (lesson['unit_id'],)).fetchone()
            conn.close()
            return render_template('lesson.html', user=user, lesson=lesson, unit=unit, is_demo=True)
        else:
            conn.close()
            return redirect(url_for('dashboard', locked=lesson['order_num']))

    # Authenticated user flow
    # Verify sequential unlock: check if previous lesson is completed (unless order_num == 1)
    if lesson['order_num'] > 1:
        prev_lesson = conn.execute(
            'SELECT id FROM lessons WHERE unit_id = ? AND order_num = ?',
            (lesson['unit_id'], lesson['order_num'] - 1)
        ).fetchone()

        if prev_lesson:
            is_prev_done = conn.execute(
                'SELECT completed FROM user_progress WHERE user_id = ? AND lesson_id = ? AND completed = 1',
                (user['id'], prev_lesson['id'])
            ).fetchone()

            is_this_done = conn.execute(
                'SELECT completed FROM user_progress WHERE user_id = ? AND lesson_id = ? AND completed = 1',
                (user['id'], lesson['id'])
            ).fetchone()

            if not is_prev_done and not is_this_done:
                conn.close()
                return redirect(url_for('dashboard', locked=lesson['order_num']))

    unit = conn.execute('SELECT * FROM units WHERE id = ?', (lesson['unit_id'],)).fetchone()
    conn.close()

    return render_template('lesson.html', user=user, lesson=lesson, unit=unit, is_demo=False)

@app.route('/api/lesson/<int:lesson_id>/questions')
def get_lesson_questions(lesson_id):
    conn = get_db_connection()
    lesson = conn.execute('SELECT order_num FROM lessons WHERE id = ?', (lesson_id,)).fetchone()
    
    # Guest users can only query questions for lesson 1 (demo)
    if is_guest_user(g.user) and (not lesson or lesson['order_num'] != 1):
        conn.close()
        return jsonify({'error': 'Giriş yapmalısınız'}), 401

    rows = conn.execute(
        'SELECT id, lesson_id, type, instruction, prompt_text, english_speech, options, explanation, order_num FROM questions WHERE lesson_id = ? ORDER BY order_num ASC',
        (lesson_id,)
    ).fetchall()

    questions = []
    for r in rows:
        questions.append({
            'id': r['id'],
            'lesson_id': r['lesson_id'],
            'type': r['type'],
            'instruction': r['instruction'],
            'prompt_text': r['prompt_text'],
            'english_speech': r['english_speech'],
            'options': json.loads(r['options']),
            'explanation': r['explanation'],
            'order_num': r['order_num']
        })

    conn.close()
    return jsonify({'success': True, 'questions': questions})

@app.route('/api/check-answer', methods=['POST'])
def check_answer():
    data = request.get_json() or {}
    question_id = data.get('question_id')
    user_answer = data.get('answer') # Can be string or list of strings

    if not question_id or user_answer is None:
        return jsonify({'error': 'Geçersiz parametre'}), 400

    conn = get_db_connection()
    user = g.user
    q = conn.execute('SELECT * FROM questions WHERE id = ?', (question_id,)).fetchone()

    if not q:
        conn.close()
        return jsonify({'error': 'Soru bulunamadı'}), 404

    correct_answer_raw = q['correct_answer']
    q_type = q['type']

    is_correct = False
    target_answer_display = ""

    if q_type == 'word_order':
        try:
            expected_list = json.loads(correct_answer_raw)
            if isinstance(expected_list, list):
                expected_str = " ".join(expected_list).strip().lower()
            else:
                expected_str = str(expected_list).strip().lower()
        except Exception:
            expected_str = str(correct_answer_raw).strip().lower()

        if isinstance(user_answer, list):
            user_str = " ".join(user_answer).strip().lower()
        else:
            user_str = str(user_answer).strip().lower()

        is_correct = (user_str == expected_str)
        target_answer_display = " ".join(json.loads(correct_answer_raw)) if isinstance(json.loads(correct_answer_raw), list) else correct_answer_raw

    else: # multiple_choice
        user_str = str(user_answer).strip().lower()
        expected_str = str(correct_answer_raw).strip().lower()
        is_correct = (user_str == expected_str)
        target_answer_display = correct_answer_raw

    if user:
        user_keys = user.keys() if hasattr(user, 'keys') else []
        is_user_premium = bool(user['is_premium']) if 'is_premium' in user_keys else False

        if not is_correct and not is_user_premium:
            new_hearts = max(0, user['hearts'] - 1)
            now_iso = datetime.datetime.now().isoformat()
            last_loss = user['last_heart_loss_time'] if 'last_heart_loss_time' in user_keys else None
            
            # Start timer if user was full or timer wasn't active
            if user['hearts'] >= (user['max_hearts'] or 5) or not last_loss:
                conn.execute('UPDATE users SET hearts = ?, last_heart_loss_time = ? WHERE id = ?', 
                             (new_hearts, now_iso, user['id']))
            else:
                conn.execute('UPDATE users SET hearts = ? WHERE id = ?', (new_hearts, user['id']))
            conn.commit()

        synced_user = conn.execute('SELECT * FROM users WHERE id = ?', (user['id'],)).fetchone()
        hearts, max_h, remaining_sec, is_full = sync_user_hearts(conn, synced_user)
        if is_user_premium:
            hearts = 5
            remaining_sec = 0
            is_full = True
    else:
        # Unauthenticated demo guest session
        demo_hearts = session.get('demo_hearts', 5)
        new_hearts = demo_hearts
        if not is_correct:
            new_hearts = max(0, demo_hearts - 1)
            session['demo_hearts'] = new_hearts
            if 'demo_last_heart_loss' not in session or demo_hearts >= 5:
                session['demo_last_heart_loss'] = datetime.datetime.now().isoformat()
        max_h = 5
        hearts = new_hearts
        remaining_sec = HEART_REFILL_INTERVAL if hearts < max_h else 0
        is_full = (hearts >= max_h)

    conn.close()

    return jsonify({
        'is_correct': is_correct,
        'correct_answer': target_answer_display,
        'explanation': q['explanation'],
        'hearts': hearts,
        'max_hearts': max_h,
        'remaining_seconds': remaining_sec,
        'is_hearts_full': is_full
    })

@app.route('/api/heart-status')
def heart_status():
    conn = get_db_connection()
    user = g.user
    if not user:
        conn.close()
        return jsonify({'hearts': 5, 'max_hearts': 5, 'remaining_seconds': 0, 'is_full': True, 'is_premium': False})
    
    hearts, max_h, remaining_sec, is_full = sync_user_hearts(conn, user)
    user_keys = user.keys() if hasattr(user, 'keys') else []
    is_user_premium = bool(user['is_premium']) if 'is_premium' in user_keys else False
    conn.close()
    return jsonify({
        'hearts': 5 if is_user_premium else hearts,
        'max_hearts': max_h,
        'remaining_seconds': 0 if is_user_premium else remaining_sec,
        'is_full': True if is_user_premium else is_full,
        'is_premium': is_user_premium
    })

@app.route('/api/lesson/<int:lesson_id>/complete', methods=['POST'])
@login_required
def complete_lesson(lesson_id):
    conn = get_db_connection()
    user = g.user
    lesson = conn.execute('SELECT * FROM lessons WHERE id = ?', (lesson_id,)).fetchone()

    if not lesson:
        conn.close()
        return jsonify({'error': 'Ders bulunamadı'}), 404

    if is_guest_user(user):
        conn.close()
        return jsonify({'success': False, 'error': 'İlerleyişinizi kaydetmek için Google ile giriş yapmalısınız.'}), 403

    xp_gained = lesson['xp_reward']
    new_xp = user['xp'] + xp_gained

    # Daily Streak (🔥 Ateş) Calculation Logic
    today_dt = datetime.date.today()
    today_str = today_dt.strftime('%Y-%m-%d')
    yesterday_str = (today_dt - datetime.timedelta(days=1)).strftime('%Y-%m-%d')

    user_keys = user.keys() if hasattr(user, 'keys') else []
    last_study = user['last_study_date'] if 'last_study_date' in user_keys else None
    current_streak = user['streak_count'] if 'streak_count' in user_keys and user['streak_count'] is not None else (user['streak'] if 'streak' in user_keys and user['streak'] is not None else 0)

    if not last_study or last_study < yesterday_str:
        # Araya gün girdiyse veya ilk kez ders çözülüyorsa
        new_streak = 1
    elif last_study == yesterday_str:
        # Dün ders tamamlanmış, bugün ardışık seri devam ediyor (+1)
        new_streak = current_streak + 1
    elif last_study == today_str:
        # Bugün zaten ders tamamlanmış, streak değişmez
        new_streak = max(1, current_streak)
    else:
        new_streak = max(1, current_streak)

    # Update progress
    conn.execute('''
    INSERT INTO user_progress (user_id, lesson_id, completed, score)
    VALUES (?, ?, 1, 100)
    ON CONFLICT(user_id, lesson_id) DO UPDATE SET completed = 1, score = 100
    ''', (user['id'], lesson_id))

    conn.execute('''
    UPDATE users 
    SET xp = ?, streak = ?, streak_count = ?, last_study_date = ? 
    WHERE id = ?
    ''', (new_xp, new_streak, new_streak, today_str, user['id']))

    # If Boss Exam of Unit 1 completed, unlock Unit 2
    if lesson['is_exam'] and (lesson['order_num'] == 13 or 'Boss' in lesson['title']):
        conn.execute("UPDATE units SET is_unlocked = 1 WHERE order_index = 2 OR order_num = 2")

    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'xp_gained': xp_gained,
        'total_xp': new_xp,
        'streak': new_streak,
        'streak_count': new_streak,
        'last_study_date': today_str,
        'has_studied_today': True,
        'is_exam': bool(lesson['is_exam'])
    })

@app.route('/api/complete-lesson', methods=['POST'])
@login_required
def api_complete_lesson_generic():
    data = request.get_json() or {}
    lesson_id = data.get('lesson_id')
    if not lesson_id:
        return jsonify({'error': 'lesson_id parametresi gerekli'}), 400
    return complete_lesson(lesson_id)

@app.route('/api/refill-hearts', methods=['POST'])
@login_required
def refill_hearts():
    conn = get_db_connection()
    user = g.user
    conn.execute('UPDATE users SET hearts = max_hearts, last_heart_loss_time = NULL WHERE id = ?', (user['id'],))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'hearts': 5, 'remaining_seconds': 0, 'is_full': True})

@app.route('/api/reset-progress', methods=['POST'])
@login_required
def api_reset_progress():
    conn = get_db_connection()
    user = g.user
    conn.execute('DELETE FROM user_progress WHERE user_id = ?', (user['id'],))
    conn.execute('UPDATE users SET hearts = 5, last_heart_loss_time = NULL, xp = 0 WHERE id = ?', (user['id'],))
    conn.execute('UPDATE units SET is_unlocked = 0 WHERE order_index > 1 OR (order_index IS NULL AND order_num > 1)')
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'İlerleme başarıyla sıfırlandı!'})

@app.route('/reset-progress', methods=['GET', 'POST'])
@login_required
def reset_progress():
    conn = get_db_connection()
    user = g.user
    conn.execute('DELETE FROM user_progress WHERE user_id = ?', (user['id'],))
    conn.execute('UPDATE users SET hearts = 5, last_heart_loss_time = NULL, xp = 0 WHERE id = ?', (user['id'],))
    conn.execute('UPDATE units SET is_unlocked = 0 WHERE order_index > 1 OR (order_index IS NULL AND order_num > 1)')
    conn.commit()
    conn.close()
    if request.is_json:
        return jsonify({'success': True, 'message': 'İlerleme başarıyla sıfırlandı!'})
    return redirect(url_for('dashboard', reset='success'))

if __name__ == '__main__':
    from init_db import init_db
    init_db()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
