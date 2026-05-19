// ── Language state ────────────────────────────────────────────────────────────
let currentLang = 'tr';

const TRANSLATIONS = {
    tr: {
        appTitle:        'Hava Durumu Agent',
        subtitle:        'Yapay zeka destekli akıllı hava durumu asistanınız',
        sectionTitle:    '📍 Şehir Seçin',
        placeholder:     'Şehir adı girin...',
        searchBtn:       'Kontrol Et',
        loading:         'Hava durumu kontrol ediliyor...',
        loadingBtn:      'Yükleniyor...',
        recTitle:        '🤖 Agent Önerileri',
        labelHumidity:   '💧 Nem',
        labelWind:       '💨 Rüzgar',
        labelFeelsLike:  '🌡️ Hissedilen',
        labelPressure:   '📊 Basınç',
        langBtn:         '🌍 EN',
        srcLLM:          '✨ Yapay zeka',
        srcRule:         '📋 Kural tabanlı',
        footer:          'Powered by OpenWeatherMap API & Claude AI 🚀',
        cities:          ['Istanbul', 'Ankara', 'Izmir', 'Bursa', 'Antalya', 'Adana', 'Trabzon', 'Konya'],
        defaultCity:     'Istanbul',
    },
    en: {
        appTitle:        'Weather Agent',
        subtitle:        'Your AI-powered smart weather assistant',
        sectionTitle:    '📍 Choose a City',
        placeholder:     'Enter city name...',
        searchBtn:       'Check',
        loading:         'Checking weather conditions...',
        loadingBtn:      'Loading...',
        recTitle:        '🤖 Agent Recommendations',
        labelHumidity:   '💧 Humidity',
        labelWind:       '💨 Wind',
        labelFeelsLike:  '🌡️ Feels Like',
        labelPressure:   '📊 Pressure',
        langBtn:         '🇹🇷 TR',
        srcLLM:          '✨ AI powered',
        srcRule:         '📋 Rule based',
        footer:          'Powered by OpenWeatherMap API & Claude AI 🚀',
        cities:          ['London', 'Paris', 'New York', 'Tokyo', 'Dubai', 'Sydney', 'Berlin', 'Barcelona'],
        defaultCity:     'London',
    },
};

function toggleLanguage() {
    currentLang = currentLang === 'tr' ? 'en' : 'tr';
    applyLanguage();
}

function applyLanguage() {
    const L = TRANSLATIONS[currentLang];
    document.documentElement.lang = currentLang;
    document.getElementById('app-title').textContent        = L.appTitle;
    document.getElementById('app-subtitle').textContent     = L.subtitle;
    document.getElementById('section-title').textContent    = L.sectionTitle;
    document.getElementById('city-input').placeholder       = L.placeholder;
    document.getElementById('search-btn-text').textContent  = L.searchBtn;
    document.getElementById('loading-text').textContent     = L.loading;
    document.getElementById('rec-title').textContent        = L.recTitle;
    document.getElementById('label-humidity').textContent   = L.labelHumidity;
    document.getElementById('label-wind').textContent       = L.labelWind;
    document.getElementById('label-feels-like').textContent = L.labelFeelsLike;
    document.getElementById('label-pressure').textContent   = L.labelPressure;
    document.getElementById('lang-toggle').textContent      = L.langBtn;
    document.getElementById('footer-text').textContent      = L.footer;
    renderCities(L.cities);
}

function renderCities(cities) {
    const container = document.getElementById('popular-cities');
    container.innerHTML = '';
    cities.forEach(city => {
        const btn = document.createElement('button');
        btn.className = 'city-tag';
        btn.textContent = city;
        btn.addEventListener('click', () => {
            document.getElementById('city-input').value = city;
            fetchWeather(city);
        });
        container.appendChild(btn);
    });
}

// ── DOM refs ──────────────────────────────────────────────────────────────────
const cityInput            = document.getElementById('city-input');
const searchBtn            = document.getElementById('search-btn');
const loading              = document.getElementById('loading');
const errorBox             = document.getElementById('error-box');
const errorMessage         = document.getElementById('error-message');
const weatherResult        = document.getElementById('weather-result');
const rainContainer        = document.getElementById('rain-container');
const cityName             = document.getElementById('city-name');
const weatherDescription   = document.getElementById('weather-description');
const weatherIcon          = document.getElementById('weather-icon');
const tempValue            = document.getElementById('temp-value');
const humidity             = document.getElementById('humidity');
const wind                 = document.getElementById('wind');
const feelsLike            = document.getElementById('feels-like');
const pressure             = document.getElementById('pressure');
const recommendationContent = document.getElementById('recommendation-content');
const recommendationText   = document.getElementById('recommendation-text');

const API_URL = window.location.hostname === 'localhost'
    ? 'http://localhost:5000'
    : '';

// ── Events ────────────────────────────────────────────────────────────────────
searchBtn.addEventListener('click', () => {
    const city = cityInput.value.trim();
    if (city) fetchWeather(city);
});

cityInput.addEventListener('keypress', e => {
    if (e.key === 'Enter') {
        const city = cityInput.value.trim();
        if (city) fetchWeather(city);
    }
});

// ── Fetch ─────────────────────────────────────────────────────────────────────
async function fetchWeather(city) {
    showLoading();
    hideError();
    hideWeatherResult();
    clearAnimations();

    try {
        const response = await fetch(`${API_URL}/api/hava-durumu`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ sehir: city, lang: currentLang }),
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || (currentLang === 'tr'
                ? 'Hava durumu bilgisi alınamadı!'
                : 'Could not fetch weather data!'));
        }

        displayWeather(data);
    } catch (error) {
        showError(error.message);
    } finally {
        hideLoading();
    }
}

// ── Display ───────────────────────────────────────────────────────────────────
function displayWeather(data) {
    cityName.textContent          = `${data.sehir}, ${data.ulke}`;
    weatherDescription.textContent = data.durum;
    weatherIcon.src               = `https://openweathermap.org/img/wn/${data.icon}@2x.png`;
    weatherIcon.alt               = data.durum;
    tempValue.textContent         = data.sicaklik;
    humidity.textContent          = `${data.nem}%`;
    wind.textContent              = `${data.ruzgar} m/s`;
    feelsLike.textContent         = `${data.hissedilen}°C`;
    pressure.textContent          = `${data.basinc} hPa`;
    recommendationText.textContent = data.oneri;
    recommendationContent.className = `recommendation-content ${data.oneri_tipi}`;

    const recSource = document.getElementById('rec-source');
    const L = TRANSLATIONS[currentLang];
    if (data.oneri_kaynagi === 'llm') {
        recSource.textContent = L.srcLLM;
        recSource.className   = 'rec-source rec-llm';
    } else {
        recSource.textContent = L.srcRule;
        recSource.className   = 'rec-source rec-rule';
    }
    recSource.classList.remove('hidden');

    updateBackground(data.oneri_tipi);

    const type = data.oneri_tipi;
    if (type === 'rain' || type === 'drizzle' || type === 'thunderstorm') {
        startRain(type === 'thunderstorm' ? 80 : 50);
    } else if (type === 'snow') {
        startSnow();
    }

    showWeatherResult();
}

// ── Background gradient ───────────────────────────────────────────────────────
function updateBackground(type) {
    const gradients = {
        thunderstorm: 'linear-gradient(135deg, #2d1b69 0%, #1a0a3d 100%)',
        drizzle:      'linear-gradient(135deg, #5c7a9e 0%, #3d5a7a 100%)',
        rain:         'linear-gradient(135deg, #4a5568 0%, #2d3748 100%)',
        snow:         'linear-gradient(135deg, #bee3f8 0%, #90cdf4 100%)',
        fog:          'linear-gradient(135deg, #718096 0%, #4a5568 100%)',
        hot:          'linear-gradient(135deg, #f6ad55 0%, #ed8936 100%)',
        cold:         'linear-gradient(135deg, #90cdf4 0%, #4299e1 100%)',
        cool:         'linear-gradient(135deg, #76e4f7 0%, #4299e1 100%)',
        good:         'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    };
    document.body.style.background = gradients[type] || gradients.good;
}

// ── Animations ────────────────────────────────────────────────────────────────
function startRain(count = 50) {
    rainContainer.innerHTML = '';
    for (let i = 0; i < count; i++) {
        const drop = document.createElement('div');
        drop.className = 'rain-drop';
        drop.style.left              = `${Math.random() * 100}%`;
        drop.style.animationDelay    = `${Math.random() * 2}s`;
        drop.style.animationDuration = `${0.5 + Math.random()}s`;
        rainContainer.appendChild(drop);
    }
}

function startSnow() {
    rainContainer.innerHTML = '';
    const flakes = ['❄', '❅', '❆'];
    for (let i = 0; i < 50; i++) {
        const flake = document.createElement('div');
        flake.className = 'snow-flake';
        flake.textContent            = flakes[Math.floor(Math.random() * flakes.length)];
        flake.style.left             = `${Math.random() * 100}%`;
        flake.style.fontSize         = `${0.8 + Math.random() * 1.4}rem`;
        flake.style.opacity          = `${0.5 + Math.random() * 0.5}`;
        flake.style.animationDelay   = `${Math.random() * 6}s`;
        flake.style.animationDuration = `${4 + Math.random() * 6}s`;
        rainContainer.appendChild(flake);
    }
}

function clearAnimations() {
    rainContainer.innerHTML = '';
}

// ── UI helpers ────────────────────────────────────────────────────────────────
function showLoading() {
    loading.classList.remove('hidden');
    searchBtn.disabled = true;
    document.getElementById('search-btn-text').textContent =
        TRANSLATIONS[currentLang].loadingBtn;
}

function hideLoading() {
    loading.classList.add('hidden');
    searchBtn.disabled = false;
    document.getElementById('search-btn-text').textContent =
        TRANSLATIONS[currentLang].searchBtn;
}

function showError(message) {
    errorMessage.textContent = message;
    errorBox.classList.remove('hidden');
}

function hideError()        { errorBox.classList.add('hidden'); }
function showWeatherResult() { weatherResult.classList.remove('hidden'); }
function hideWeatherResult() { weatherResult.classList.add('hidden'); }

// ── Init ──────────────────────────────────────────────────────────────────────
window.addEventListener('load', () => {
    applyLanguage();
    fetchWeather(TRANSLATIONS[currentLang].defaultCity);
});
