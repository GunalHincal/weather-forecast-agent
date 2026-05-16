// DOM Elements
const cityInput = document.getElementById('city-input');
const searchBtn = document.getElementById('search-btn');
const popularCities = document.querySelectorAll('.city-tag');
const loading = document.getElementById('loading');
const errorBox = document.getElementById('error-box');
const errorMessage = document.getElementById('error-message');
const weatherResult = document.getElementById('weather-result');
const rainContainer = document.getElementById('rain-container');

// Weather data elements
const cityName = document.getElementById('city-name');
const weatherDescription = document.getElementById('weather-description');
const weatherIcon = document.getElementById('weather-icon');
const tempValue = document.getElementById('temp-value');
const humidity = document.getElementById('humidity');
const wind = document.getElementById('wind');
const feelsLike = document.getElementById('feels-like');
const pressure = document.getElementById('pressure');
const recommendationContent = document.getElementById('recommendation-content');
const recommendationText = document.getElementById('recommendation-text');

// API endpoint (production'da boş string, development'ta localhost)
const API_URL = window.location.hostname === 'localhost' 
    ? 'http://localhost:5000'
    : '';

// Event Listeners
searchBtn.addEventListener('click', () => {
    const city = cityInput.value.trim();
    if (city) {
        fetchWeather(city);
    }
});

cityInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        const city = cityInput.value.trim();
        if (city) {
            fetchWeather(city);
        }
    }
});

popularCities.forEach(cityTag => {
    cityTag.addEventListener('click', () => {
        const city = cityTag.textContent;
        cityInput.value = city;
        fetchWeather(city);
    });
});

// Hava durumu verisi çekme
async function fetchWeather(city) {
    // UI'ı hazırla
    showLoading();
    hideError();
    hideWeatherResult();
    stopRainAnimation();

    try {
        const response = await fetch(`${API_URL}/api/hava-durumu`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ sehir: city })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Hava durumu bilgisi alınamadı!');
        }

        // Başarılı - verileri göster
        displayWeather(data);
        
    } catch (error) {
        showError(error.message);
    } finally {
        hideLoading();
    }
}

// Hava durumu verisini göster
function displayWeather(data) {
    // Şehir bilgileri
    cityName.textContent = `${data.sehir}, ${data.ulke}`;
    weatherDescription.textContent = data.durum;
    
    // Hava durumu ikonu
    weatherIcon.src = `https://openweathermap.org/img/wn/${data.icon}@2x.png`;
    weatherIcon.alt = data.durum;
    
    // Sıcaklık ve detaylar
    tempValue.textContent = data.sicaklik;
    humidity.textContent = `${data.nem}%`;
    wind.textContent = `${data.ruzgar} m/s`;
    feelsLike.textContent = `${data.hissedilen}°C`;
    pressure.textContent = `${data.basinc} hPa`;
    
    // Agent önerisi
    recommendationText.textContent = data.oneri;
    recommendationContent.className = `recommendation-content ${data.oneri_tipi}`;
    
    // Arka plan rengini güncelle
    updateBackground(data.oneri_tipi);
    
    // Yağmur animasyonu
    if (data.yagmur_var) {
        startRainAnimation();
    }
    
    // Sonuç kartını göster
    showWeatherResult();
}

// Arka plan rengini güncelle
function updateBackground(type) {
    const body = document.body;
    
    const gradients = {
        rain: 'linear-gradient(135deg, #4a5568 0%, #2d3748 100%)',
        hot: 'linear-gradient(135deg, #f6ad55 0%, #ed8936 100%)',
        cold: 'linear-gradient(135deg, #90cdf4 0%, #4299e1 100%)',
        good: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
    };
    
    body.style.background = gradients[type] || gradients.good;
}

// Yağmur animasyonu başlat
function startRainAnimation() {
    rainContainer.innerHTML = '';
    
    for (let i = 0; i < 50; i++) {
        const drop = document.createElement('div');
        drop.className = 'rain-drop';
        drop.style.left = `${Math.random() * 100}%`;
        drop.style.animationDelay = `${Math.random() * 2}s`;
        drop.style.animationDuration = `${0.5 + Math.random()}s`;
        rainContainer.appendChild(drop);
    }
}

// Yağmur animasyonu durdur
function stopRainAnimation() {
    rainContainer.innerHTML = '';
}

// Loading göster
function showLoading() {
    loading.classList.remove('hidden');
    searchBtn.disabled = true;
    searchBtn.textContent = 'Yükleniyor...';
}

// Loading gizle
function hideLoading() {
    loading.classList.add('hidden');
    searchBtn.disabled = false;
    searchBtn.textContent = '🔍 Kontrol Et';
}

// Hata göster
function showError(message) {
    errorMessage.textContent = message;
    errorBox.classList.remove('hidden');
}

// Hata gizle
function hideError() {
    errorBox.classList.add('hidden');
}

// Hava durumu sonucunu göster
function showWeatherResult() {
    weatherResult.classList.remove('hidden');
}

// Hava durumu sonucunu gizle
function hideWeatherResult() {
    weatherResult.classList.add('hidden');
}

// Sayfa yüklendiğinde varsayılan şehir için veri çek
window.addEventListener('load', () => {
    fetchWeather('Istanbul');
});
