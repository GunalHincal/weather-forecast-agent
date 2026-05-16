# 🤖 Hava Durumu Agent

Yapay zeka destekli akıllı hava durumu asistanı. Python backend + HTML/CSS/JS frontend ile geliştirilmiştir.

## 📸 Önizleme

Canlı demo: [https://weatherforecastagent.onrender.com/](https://weatherforecastagent.onrender.com/)

## ✨ Özellikler

- 🌍 Türkiye şehirleri için hızlı hava durumu sorgulaması
- 🤖 Akıllı AI Agent önerileri
- 🌧️ Yağmur animasyonu (yağmurlu havalarda)
- 🎨 Hava durumuna göre dinamik renk temaları
- 📊 Detaylı hava durumu bilgileri (nem, rüzgar, basınç)
- 📱 Responsive tasarım (mobil uyumlu)

## 🛠️ Teknolojiler

**Backend:**

- Python 3.x
- Flask (Web Framework)
- Requests (HTTP istekleri)
- python-dotenv (Environment variables)

**Frontend:**

- HTML5
- CSS3 (Animations, Flexbox, Grid)
- Vanilla JavaScript (ES6+)

**API:**

- OpenWeatherMap API

## 📋 Gereksinimler

- Python 3.7 veya üzeri
- OpenWeatherMap API Key: [https://openweathermap.org/api](https://openweathermap.org/api)

## 🚀 Kurulum

### 1. Projeyi Klonlayın

```bash
git clone <your-repo-url>
cd hava-durumu-agent
```

### 2. Python Bağımlılıklarını Yükleyin

```bash
cd backend
pip install -r requirements.txt
```

### 3. Environment Variables Ayarlayın

`backend/.env` dosyasını açın ve API key'inizi girin:

```env
OPENWEATHER_API_KEY=your_actual_api_key_here
PORT=5000
```

### 4. Uygulamayı Çalıştırın

```bash
# Backend klasöründeyken
python app.py
```

Uygulama `http://localhost:5000` adresinde çalışmaya başlayacaktır.

## 📦 Render.com'a Deploy Etme

### 1. GitHub'a Push Edin

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-github-repo>
git push -u origin main
```

### 2. Render.com'da Yeni Web Service Oluşturun

1. [Render Dashboard](https://dashboard.render.com/) → "New" → "Web Service"
2. GitHub repository'nizi bağlayın
3. Ayarları yapın:
   - **Name:** hava-durumu-agent (veya istediğiniz isim)
   - **Region:** Frankfurt (EU Central)
   - **Branch:** main
   - **Root Directory:** `backend` (önemli!)
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`

### 3. Environment Variables Ekleyin

Render Dashboard'da:

- "Environment" sekmesine gidin
- "Add Environment Variable" tıklayın
- Key: `OPENWEATHER_API_KEY`
- Value: `your_api_key_here`
- "Save Changes"

### 4. Deploy Edin!

Render otomatik olarak build edip deploy edecektir. Birkaç dakika içinde uygulamanız hazır olacak!

## 📁 Proje Yapısı

```
hava-durumu-agent/
├── frontend/
│   ├── index.html         # Ana HTML
│   ├── style.css          # CSS styling
│   └── script.js          # JavaScript logic
│
├── app.py              # Flask API
├── agent.py            # Hava Durumu Agent sınıfı
├── requirements.txt    # Python bağımlılıkları
├── .env                # Environment variables (git'e eklenmez)
├── .gitignore
└── README.md
```

## 🎯 Kullanım

1. Ana sayfada şehir adı girin veya popüler şehirlerden birini seçin
2. "Kontrol Et" butonuna tıklayın
3. Hava durumu bilgileri ve AI Agent önerileri görüntülenecektir

## 🤖 Agent Nasıl Çalışır?

Agent, `agent.py` dosyasındaki `HavaDurumuAgent` sınıfı ile çalışır:

1. **Veri Toplama:** OpenWeatherMap API'den hava durumu verisi çeker
2. **Analiz:** Sıcaklık, nem, rüzgar gibi verileri analiz eder
3. **Karar Verme:** Yağmur, sıcak veya soğuk hava durumlarını tespit eder
4. **Öneri:** Kullanıcıya akıllı öneriler sunar (şemsiye, kalın giysi, vb.)

## 🔧 Geliştirme

### Local Development

```bash
# Backend'i development mode'da çalıştır
cd backend
python app.py

# Tarayıcıda aç
# http://localhost:5000
```

### Test Etme

```bash
# API health check
curl http://localhost:5000/api/health

# Hava durumu sorgusu
curl -X POST http://localhost:5000/api/hava-durumu \
  -H "Content-Type: application/json" \
  -d '{"sehir": "Istanbul"}'
```

## 📝 API Endpoints

### `GET /`

Ana sayfa (HTML)

### `POST /api/hava-durumu`

Hava durumu sorgulama

**Request:**

```json
{
  "sehir": "Istanbul"
}
```

**Response:**

```json
{
  "sehir": "Istanbul",
  "ulke": "TR",
  "sicaklik": 18,
  "hissedilen": 16,
  "durum": "parçalı bulutlu",
  "nem": 65,
  "ruzgar": 3.5,
  "basinc": 1013,
  "yagmur_var": false,
  "oneri": "✅ GÜZEL BİR GÜN! Hava oldukça ideal...",
  "oneri_tipi": "good",
  "icon": "02d",
  "tarih": "17.05.2026 21:30"
}
```

### `GET /api/health`

Health check endpoint

## 🐛 Sorun Giderme

**"API key tanımlanmamış" hatası:**

- `.env` dosyasında `OPENWEATHER_API_KEY` değişkenini kontrol edin
- API key'in aktif olduğundan emin olun (10-15 dakika sürebilir)

**"Şehir bulunamadı" hatası:**

- Şehir ismini İngilizce veya Türkçe karakterler olmadan yazın
- Örnek: "Izmir" yerine "Izmir" veya "İzmir"

**Port zaten kullanımda:**

- `.env` dosyasında `PORT` değerini değiştirin
- Veya çalışan diğer uygulamaları kapatın

## 📄 Lisans

Bu proje eğitim amaçlıdır ve özgürce kullanılabilir.

## 🙏 Teşekkürler

- [OpenWeatherMap](https://openweathermap.org/) - Hava durumu API'si
- [Render](https://render.com/) - Hosting platformu
- Medium yazısını okuyan tüm öğrenciler 🎓

## 📧 İletişim

Sorularınız için Medium yazısının yorum kısmını kullanabilirsiniz!

---

**Medium Yazısı:** [MCP ve Agent&#39;ları Sıfırdan Öğrenin](#)

**Live Demo:** [https://weatherforecastagent.onrender.com/](https://weatherforecastagent.onrender.com/)

🚀 Başarılar!
