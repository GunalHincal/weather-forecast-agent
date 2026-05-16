import requests
from datetime import datetime

class HavaDurumuAgent:
    def __init__(self, sehir, api_key):
        self.sehir = sehir
        self.api_key = api_key
        
    def hava_durumunu_kontrol_et(self):
        """Hava durumu verisini API'den çeker"""
        url = f"http://api.openweathermap.org/data/2.5/weather?q={self.sehir}&appid={self.api_key}&units=metric&lang=tr"
        
        try:
            response = requests.get(url)
            data = response.json()
            return data
        except Exception as e:
            return {"error": str(e)}
    
    def yagmur_kontrolu(self, hava_data):
        """Yağmur yağıp yağmayacağını kontrol eder"""
        if hava_data and 'weather' in hava_data:
            weather = hava_data['weather'][0]['main']
            if 'Rain' in weather:
                return True
        return False
    
    def analiz_yap(self, hava_data):
        """Hava durumu analizini JSON formatında döner"""
        if 'error' in hava_data:
            return {"error": hava_data['error']}
        
        sicaklik = hava_data['main']['temp']
        durum = hava_data['weather'][0]['description']
        yagmur_var = self.yagmur_kontrolu(hava_data)
        
        # Akıllı öneri
        if yagmur_var:
            oneri = "⚠️ YAĞMUR UYARISI! Yağmur yağacak! Şemsiyenizi yanınıza almayı unutmayın. ☔"
            oneri_tipi = "rain"
        elif sicaklik > 30:
            oneri = f"🌡️ SICAK HAVA UYARISI! Hava oldukça sıcak ({round(sicaklik)}°C). Bol bol su için!"
            oneri_tipi = "hot"
        elif sicaklik < 10:
            oneri = f"❄️ SOĞUK HAVA UYARISI! Hava soğuk ({round(sicaklik)}°C). Kalın giyinin!"
            oneri_tipi = "cold"
        else:
            oneri = f"✅ GÜZEL BİR GÜN! Hava oldukça ideal ({round(sicaklik)}°C). İyi günler! 😊"
            oneri_tipi = "good"
        
        return {
            "sehir": hava_data['name'],
            "ulke": hava_data['sys']['country'],
            "sicaklik": round(sicaklik),
            "hissedilen": round(hava_data['main']['feels_like']),
            "durum": durum,
            "nem": hava_data['main']['humidity'],
            "ruzgar": hava_data['wind']['speed'],
            "basinc": hava_data['main']['pressure'],
            "yagmur_var": yagmur_var,
            "oneri": oneri,
            "oneri_tipi": oneri_tipi,
            "icon": hava_data['weather'][0]['icon'],
            "tarih": datetime.now().strftime('%d.%m.%Y %H:%M')
        }
    
    def calistir(self):
        """Agent'ı çalıştırır - JSON response döner"""
        hava_data = self.hava_durumunu_kontrol_et()
        return self.analiz_yap(hava_data)
