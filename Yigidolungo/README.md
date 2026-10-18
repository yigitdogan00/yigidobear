# 🐻 YiğidoBear - Okyanus Mavisi & Küçük Ayı Temalı İngilizce Öğrenme Platformu

Python Flask ve SQLite kullanılarak geliştirilmiş, Duolingo'nun 3D buton ve oyunlaştırma (gamification) dinamiklerini **ferah okyanus mavisi** (#0EA5E9 / #0284C7) renk paleti ve **sevimli Küçük Ayı (Teddy Bear)** maskotu ile harmanlayan modern bir İngilizce öğrenme web uygulamasıdır.

---

## 🌟 Öne Çıkan Özellikler

1. **Genişletilmiş Ünite 1 Müfredatı (7 Konu + 6 Sınav/Test = 13 Adım)**:
   - **Sıralı Kilit Mekanizması**: Kullanıcı bir konuyu veya sınavı bitirmeden sonraki adıma geçemez.
   - **Konu 1**: Selamlaşma & Temel Tanışma (Zorluk: 1 - Çoktan seçmeli)
   - **Konu 2**: Kendini Tanıtma & Ülkeler (Zorluk: 2 - Kelime eşleştirme & çoktan seçmeli)
   - **🏆 Test 1**: Ara Değerlendirme 1 (Konu 1 & 2 karması - 7 soru)
   - **Konu 3**: Günlük Nesneler & Renkler (Zorluk: 2 - Kelime sıralama)
   - **Konu 4**: Sayılar & Saatler (Zorluk: 3 - Çoktan seçmeli & dinleme/ses)
   - **🏆 Test 2**: Ara Değerlendirme 2 (Konu 3 & 4 karması - 7 soru)
   - **Konu 5**: Aile Üyeleri & Sıfatlar (Zorluk: 3 - Kelime sıralama & tamamlama)
   - **Konu 6**: Günlük Rutinler & Temel Fiiller (Zorluk: 4 - Cümle kurma & çeviri)
   - **🏆 Test 3**: Ara Değerlendirme 3 (Konu 5 & 6 karması - 7 soru)
   - **Konu 7**: Basit Şimdiki Zaman & Aktiviteler (Zorluk: 4 - Şimdiki zaman & çeviri)
   - **🏆 Test 4**: Konu 7 Pekiştirme Testi (Zorluk: 4 - 7 soru)
   - **🏆 Test 5**: Ünite 1 Genel Deneme Sınavı (Tüm 7 konudan karma - 10 soru)
   - **👑 Test 6**: Ünite 1 Bitirme & Seviye Atlama Sınavı (**Boss Sınavı** - 12 soru, Kupa ödüllü!)

2. **Profil Sekmesi & Düzenleme (`/profile` & `/profile/edit`)**:
   - Google profil fotoğrafı veya Ayıcık avatarı.
   - Görünen ad (display name), günlük hedef (10, 20, 50 XP) ve biyografi/hedef düzenleme.
   - Toplam XP, mevcut can, seri, tamamlanan konu (X / 7) ve başarılan sınav (Y / 6) istatistikleri.
   - Başarı rozetleri (İlk Adım, Sınav Fatihi, Ateş Serisi, Büyük Şampiyon).

3. **Duolingo Tarzı 13 Adımlı Yol Haritası (Dashboard)**:
   - Kıvrımlı basamaklı dikey patika.
   - Normal dersler okyanus mavisi yuvarlak butonlarla, 6 sınav altın taç/kupa parıltısıyla öne çıkar.
   - Tamamlanan adımlar yeşil onaylı (✓), aktif adım zıplayan ("BAŞLA"), kilitli adımlar pasif (🔒).

2. **İnteraktif Soru Ekranı & Ayıcık Tepkileri**:
   - **Çoktan Seçmeli (Multiple Choice)**: 3D kartlar, klavye kısayolları (1, 2, 3, 4) ve seçim animasyonları.
   - **Kelime Sıralama (Word Order)**: Kelime havuzundan tıklayarak cümle kurma ve cümleden geri çıkartma mekaniği.
   - **Küçük Ayı Maskotu Tepkileri**:
     - Doğru cevapta: Küçük Ayı tebessüm ederek başparmak yukarı (👍) kaldırır ve kutlama zıplaması yapar.
     - Yanlış cevapta: Sevimli empati ifadesiyle kullanıcıyı cesaretlendirir (*"Sorun değil, bir dahaki sefere yapacaksın! 🐻"*).
   - **Duolingo Tarzı Alt Çekmece**: Doğru cevapta yeşil deniz esintisi kutlama çekmecesi, yanlış cevapta doğru yanıt ve Türkçe ipucu açıklaması sunan çekmece.

3. **Okyanus Mavisi 3D Tasarım Dili**:
   - Ferah okyanus mavisi (`#0284c7`), gök mavisi (`#0ea5e9`), 3D gölgeler (`#0369a1`), açık deniz tonları (`#f0f9ff` ve `#e0f2fe`).
   - Dokunma hissi veren **3D ekstrüzyonlu butonlar** (`box-shadow` ve `translateY` efektleri).
   - Harici resme ihtiyaç duymayan, modern ve vektörel sevimli Küçük Ayı (Little Bear / Teddy) SVG illüstrasyonu.
   - Ders tamamlama konfeti patlaması ve zafer ses efektleri.

4. **Ses & Telaffuz (Web Speech API + Web Audio API)**:
   - **Web Speech API**: İngilizce kelime ve cümleleri hem normal hızda (0.9x) hem de kaplumbağa modunda yavaş (0.6x) dinleme imkanı.
   - **Web Audio API**: Dışarıdan dosya indirmeye gerek kalmadan tarayıcı içinde gerçek zamanlı sentezlenen doğru cevap melodisi, yanlış ses tonu, buton tıklama ve ders bitirme fanfarı.

---

## 📁 Proje Dizin Yapısı

```
YiğidoBear/
├── app.py                # Flask sunucusu ve API rotaları (/api/check-answer, /api/lesson, vb.)
├── init_db.py            # SQLite veritabanı şeması ve başlangıç tohum verileri (Unit, Lesson, Questions)
├── database.db           # SQLite veritabanı dosyası
├── test_app.py           # Backend ve değerlendirme fonksiyonlarını test eden betik
├── static/
│   ├── css/
│   │   └── style.css     # Duolingo renkleri, 3D butonlar ve responsive stil kuralları
│   ├── js/
│   │   ├── audio.js      # Web Audio API (ses efektleri) & Web Speech API (İngilizce telaffuz)
│   │   └── lesson.js     # Çoktan seçmeli ve kelime sıralama soru motoru, can ve ilerleme yönetimi
│   └── images/
│       ├── mascot_happy.svg
│       ├── mascot_sad.svg
│       └── mascot_cheer.svg
└── templates/
    ├── base.html         # Üst menü (Can, XP, Streak, Maskot) ve global modal pencereleri
    ├── dashboard.html    # Ünite listesi ve kıvrımlı ders patikası
    └── lesson.html       # Tam ekran ders çözme arayüzü ve alt çekmece
```

---

## 🔑 Google OAuth 2.0 Kurulumu (.env)

Google ile giriş özelliğini aktif etmek için:

1. [Google Cloud Console](https://console.cloud.google.com/)'a gidin ve yeni bir proje oluşturun.
2. **APIs & Services > Credentials** (Kimlik Bilgileri) bölümünden **Create Credentials > OAuth client ID** seçin.
3. Uygulama türünü **Web Application** (Web Uygulaması) olarak seçin.
4. **Authorized redirect URIs** (Yetkilendirilmiş Yönlendirme URI'leri) alanına şunu ekleyin:
   ```
   http://127.0.0.1:5000/authorize
   ```
5. Oluşturulan **Client ID** ve **Client Secret** değerlerini projenizdeki `.env` dosyasına yazın:
   ```env
   SECRET_KEY=yigidobear-super-secret-key-ocean-blue-2026
   GOOGLE_CLIENT_ID=your_client_id_here.apps.googleusercontent.com
   GOOGLE_CLIENT_SECRET=your_client_secret_here
   ```
6. Bilgileri girdikten sonra kullanıcılar **Google ile Giriş Yap** butonuna tıkladıklarında otomatik olarak profil resmi, adı ve e-postasıyla kayıt olur ve oturum açar.
7. Henüz Google kimlik bilgileriniz yoksa **Hızlı Demo Girişi** butonuyla da sistemi anında test edebilirsiniz!

---

## 🚀 Çalıştırma

1. Gerekli kütüphaneleri yükleyin:
   ```bash
   pip install Flask Authlib python-dotenv requests
   ```

2. Veritabanını başlatın ve güncelleyin:
   ```bash
   python init_db.py
   ```

3. Flask sunucusunu başlatın:
   ```bash
   python app.py
   ```

4. Tarayıcınızda açın:
   👉 **http://127.0.0.1:5000**
