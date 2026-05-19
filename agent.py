import requests
from datetime import datetime

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

# All OpenWeatherMap weather condition IDs
WEATHER_IDS = {
    # Group 2xx: Thunderstorm
    200: 'thunderstorm with light rain', 201: 'thunderstorm with rain',
    202: 'thunderstorm with heavy rain', 210: 'light thunderstorm',
    211: 'thunderstorm', 212: 'heavy thunderstorm', 221: 'ragged thunderstorm',
    230: 'thunderstorm with light drizzle', 231: 'thunderstorm with drizzle',
    232: 'thunderstorm with heavy drizzle',
    # Group 3xx: Drizzle
    300: 'light drizzle', 301: 'drizzle', 302: 'heavy drizzle',
    310: 'light drizzle rain', 311: 'drizzle rain', 312: 'heavy drizzle rain',
    313: 'shower rain and drizzle', 314: 'heavy shower rain and drizzle', 321: 'shower drizzle',
    # Group 5xx: Rain
    500: 'light rain', 501: 'moderate rain', 502: 'heavy rain',
    503: 'very heavy rain', 504: 'extreme rain', 511: 'freezing rain',
    520: 'light shower rain', 521: 'shower rain', 522: 'heavy shower rain',
    531: 'ragged shower rain',
    # Group 6xx: Snow
    600: 'light snow', 601: 'snow', 602: 'heavy snow',
    611: 'sleet', 612: 'light shower sleet', 613: 'shower sleet',
    615: 'light rain and snow', 616: 'rain and snow',
    620: 'light shower snow', 621: 'shower snow', 622: 'heavy shower snow',
    # Group 7xx: Atmosphere
    701: 'mist', 711: 'smoke', 721: 'haze',
    731: 'dust whirls', 741: 'fog', 751: 'sand',
    761: 'dust', 762: 'volcanic ash', 771: 'squalls', 781: 'tornado',
    # Group 800: Clear
    800: 'clear sky',
    # Group 80x: Clouds
    801: 'few clouds (11-25%)', 802: 'scattered clouds (25-50%)',
    803: 'broken clouds (51-84%)', 804: 'overcast clouds (85-100%)',
}

RULE_RECOMMENDATIONS = {
    'tr': {
        'Thunderstorm': (
            "⛈️ FIRTINA ALARMI! Dışarı çıkmak zorunda değilsen evde kal — "
            "yıldırım şaka değil! Çıkacaksan su geçirmez mont + şemsiye şart, "
            "ama açık alanda sakın durma!", 'thunderstorm'
        ),
        'Drizzle': (
            "🌦️ Hafif çiseleyen bir yağmur var. Şemsiye alsam mı almasam mı dersin ama "
            "biraz ıslanırsan kuruması kolay 😄 Yine de çantana at!", 'drizzle'
        ),
        'Rain': (
            "☔ YAĞMUR YAĞIYOR! Şemsiyesiz çıkarsan pişman olursun, sözüm ona. "
            "Su geçirmez ayakkabı da giysen büyük artı!", 'rain'
        ),
        'Snow': (
            "❄️ KAR YAĞIYOR! Bot giy, kalın kaban al, eldiven ve bere şart. "
            "Yollar kaygan olabilir — sür dikkatli, acele etme!", 'snow'
        ),
        'Mist': (
            "🌫️ Sisli hava var. Araç kullanacaksan yavaş git ve sisli far yak — "
            "görüş mesafesi düşük!", 'fog'
        ),
        'Smoke': (
            "🌫️ Havada duman var. Mümkünse dışarı çıkma, çıkacaksan N95 maske tak!", 'fog'
        ),
        'Haze': (
            "🌫️ Pus var. Solunum sorunu olanlar dikkat! "
            "Lens yerine gözlük daha iyi olur bugün.", 'fog'
        ),
        'Dust': (
            "🌪️ Tozlu/kumlu hava! Gözlerini koru, maske tak. "
            "Pencereni de kapat yoksa evin altüst olur!", 'fog'
        ),
        'Fog': (
            "🌁 YOĞUN SİS! Araba kullanmak zorundaysan çok dikkat et — "
            "görüş mesafesi ciddi şekilde düşük!", 'fog'
        ),
        'Sand': (
            "🏜️ Kum fırtınası! Mümkünse dışarı çıkma. Gözlerini ve ağzını koru.", 'fog'
        ),
        'Ash': (
            "🌋 Havada volkanik kül var! Kesinlikle maske tak, "
            "zorunlu değilse dışarı adım atma!", 'fog'
        ),
        'Squall': (
            "💨 Ani fırtına/bora var! Dışardaysan güvenli bir yere geç. "
            "Şapkan uçar gider 😄", 'thunderstorm'
        ),
        'Tornado': (
            "🌪️ TORNADO ALARMI! HEMEN GÜVENLİ YERE GEÇ! BU ŞAKA DEĞİL!", 'thunderstorm'
        ),
    },
    'en': {
        'Thunderstorm': (
            "⛈️ STORM ALERT! Stay home if you don't have to go out — "
            "lightning is no joke! If you must, waterproof jacket + umbrella, "
            "and avoid open areas at all costs!", 'thunderstorm'
        ),
        'Drizzle': (
            "🌦️ Light drizzle out there. Umbrella or not, it's your call — "
            "a little water never hurt anyone 😄 Still, toss one in your bag!", 'drizzle'
        ),
        'Rain': (
            "☔ IT'S RAINING! Step out without an umbrella and you'll regret it, trust me. "
            "Waterproof shoes are a huge bonus!", 'rain'
        ),
        'Snow': (
            "❄️ IT'S SNOWING! Boots, thick coat, gloves, and beanie are a must. "
            "Roads might be slippery — drive slowly and carefully!", 'snow'
        ),
        'Mist': (
            "🌫️ Misty out there. If you're driving, slow down and use fog lights — "
            "visibility is reduced!", 'fog'
        ),
        'Smoke': (
            "🌫️ Smoke in the air. Stay indoors if possible, wear an N95 mask if you go out!", 'fog'
        ),
        'Haze': (
            "🌫️ Hazy conditions. Take extra care if you have respiratory issues. "
            "Glasses beat contacts today.", 'fog'
        ),
        'Dust': (
            "🌪️ Dusty/sandy conditions! Protect your eyes, wear a mask. "
            "Close your windows or everything will be covered in dust!", 'fog'
        ),
        'Fog': (
            "🌁 HEAVY FOG! Drive with extreme caution if you must — "
            "visibility is seriously impaired!", 'fog'
        ),
        'Sand': (
            "🏜️ Sandstorm! Stay inside if you can. Protect your eyes and mouth.", 'fog'
        ),
        'Ash': (
            "🌋 Volcanic ash in the air! Wear a mask — "
            "stay indoors unless absolutely necessary!", 'fog'
        ),
        'Squall': (
            "💨 Sudden squalls! Find shelter if you're outside. "
            "Your hat might fly to another country 😄", 'thunderstorm'
        ),
        'Tornado': (
            "🌪️ TORNADO WARNING! TAKE COVER IMMEDIATELY! THIS IS NOT A DRILL!", 'thunderstorm'
        ),
    }
}


def _temperature_recommendation(temp, lang):
    if lang == 'tr':
        if temp > 35:
            return (
                f"🔥 YANIYORUZ! {round(temp)}°C mi?! Termosu doldur soğuk suyla, "
                f"şapka tak, güneş kremini sür — sıcak çarpması şaka değil!", 'hot'
            )
        elif temp > 30:
            return (
                f"🌡️ SICAK! {round(temp)}°C — bol bol su iç, yanına su şişesi al. "
                f"Güneş kremi de sürsene!", 'hot'
            )
        elif temp < 0:
            return (
                f"🥶 DONACAKSIN! {round(temp)}°C! Bot, bere, atkı, eldiven — "
                f"tam techizat lazım! Dışarısı gerçekten buz gibi!", 'cold'
            )
        elif temp < 10:
            return (
                f"❄️ SOĞUK! {round(temp)}°C — kalın mont şart. "
                f"Şapkanı da tak, soğuk algınlığı kapma!", 'cold'
            )
        elif temp < 18:
            return (
                f"🧥 Serin bir gün ({round(temp)}°C). "
                f"İnce bir mont ya da hırka yeterli olur.", 'cool'
            )
        else:
            return (
                f"✅ MÜKEMMEL HAVA! {round(temp)}°C — ideal sıcaklık. "
                f"Dışarı çık ve keyfini çıkar! 😊", 'good'
            )
    else:
        if temp > 35:
            return (
                f"🔥 SCORCHING! {round(temp)}°C?! Fill that thermos with cold water, "
                f"wear a hat, slap on sunscreen — heatstroke is real!", 'hot'
            )
        elif temp > 30:
            return (
                f"🌡️ HOT! {round(temp)}°C — drink lots of water, carry a bottle. "
                f"Put on some sunscreen while you're at it!", 'hot'
            )
        elif temp < 0:
            return (
                f"🥶 FREEZING! {round(temp)}°C! Boots, beanie, scarf, gloves — "
                f"full gear required! It's literally below zero out there!", 'cold'
            )
        elif temp < 10:
            return (
                f"❄️ COLD! {round(temp)}°C — thick coat is a must. "
                f"Wear your hat, don't catch a cold!", 'cold'
            )
        elif temp < 18:
            return (
                f"🧥 Cool day ({round(temp)}°C). "
                f"A light jacket or sweater should do the trick.", 'cool'
            )
        else:
            return (
                f"✅ PERFECT WEATHER! {round(temp)}°C — ideal conditions. "
                f"Get outside and enjoy it! 😊", 'good'
            )


class HavaDurumuAgent:
    def __init__(self, sehir, api_key, lang='tr', anthropic_key=None):
        self.sehir = sehir
        self.api_key = api_key
        self.lang = lang
        self.anthropic_key = anthropic_key

    def hava_durumunu_kontrol_et(self):
        lang_param = 'tr' if self.lang == 'tr' else 'en'
        url = (
            f"http://api.openweathermap.org/data/2.5/weather"
            f"?q={self.sehir}&appid={self.api_key}&units=metric&lang={lang_param}"
        )
        try:
            response = requests.get(url, timeout=10)
            data = response.json()
            if response.status_code == 404:
                msg = (
                    f"'{self.sehir}' şehri bulunamadı. Şehir adını kontrol edin."
                    if self.lang == 'tr'
                    else f"City '{self.sehir}' not found. Please check the city name."
                )
                return {"error": msg}
            if response.status_code == 401:
                msg = ("Geçersiz API anahtarı." if self.lang == 'tr' else "Invalid API key.")
                return {"error": msg}
            return data
        except Exception as e:
            return {"error": str(e)}

    def _get_category(self, weather_id, weather_main):
        if 200 <= weather_id <= 232:
            return 'Thunderstorm'
        if 300 <= weather_id <= 321:
            return 'Drizzle'
        if 500 <= weather_id <= 531:
            return 'Rain'
        if 600 <= weather_id <= 622:
            return 'Snow'
        single_map = {
            701: 'Mist', 711: 'Smoke', 721: 'Haze',
            731: 'Dust', 741: 'Fog', 751: 'Sand',
            761: 'Dust', 762: 'Ash', 771: 'Squall', 781: 'Tornado',
            800: 'Clear',
        }
        if weather_id in single_map:
            return single_map[weather_id]
        if 801 <= weather_id <= 804:
            return 'Clouds'
        return weather_main

    def _llm_recommendation(self, weather_info):
        if not ANTHROPIC_AVAILABLE or not self.anthropic_key:
            return None
        try:
            client = anthropic.Anthropic(api_key=self.anthropic_key)
            if self.lang == 'tr':
                system = (
                    "Sen hem hava durumu asistanısın hem de çok esprili, samimi bir arkadaşsın. "
                    "Kullanıcıya hava durumuna göre komik, sıcak ve pratik öneriler ver. "
                    "En yakın arkadaşın gibi konuş — samimi, esprili, ama işe yarar. "
                    "2-3 cümle yeterli. Emoji kullan. Fazla uzatma."
                )
                user_msg = (
                    f"{weather_info['sehir']}, {weather_info['ulke']} — "
                    f"Sıcaklık: {weather_info['sicaklik']}°C (hissedilen {weather_info['hissedilen']}°C), "
                    f"Durum: {weather_info['durum']}, Nem: {weather_info['nem']}%, "
                    f"Rüzgar: {weather_info['ruzgar']} m/s. "
                    f"Bu hava için kısa, esprili ve pratik bir öneri ver."
                )
            else:
                system = (
                    "You are a weather assistant but also a hilarious, warm friend. "
                    "Give funny, friendly and practical recommendations based on the weather. "
                    "Talk like a best friend — casual, witty, but actually useful. "
                    "2-3 sentences max. Use emojis. Keep it short."
                )
                user_msg = (
                    f"{weather_info['sehir']}, {weather_info['ulke']} — "
                    f"Temp: {weather_info['sicaklik']}°C (feels like {weather_info['hissedilen']}°C), "
                    f"Condition: {weather_info['durum']}, Humidity: {weather_info['nem']}%, "
                    f"Wind: {weather_info['ruzgar']} m/s. "
                    f"Give a short, funny and practical recommendation for this weather."
                )
            msg = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=200,
                system=system,
                messages=[{"role": "user", "content": user_msg}]
            )
            return msg.content[0].text
        except Exception:
            return None

    def _rule_recommendation(self, hava_data, weather_id, temp):
        category = self._get_category(weather_id, hava_data['weather'][0]['main'])
        lang_rules = RULE_RECOMMENDATIONS.get(self.lang, RULE_RECOMMENDATIONS['tr'])
        if category in lang_rules:
            return lang_rules[category]
        return _temperature_recommendation(temp, self.lang)

    def analiz_yap(self, hava_data):
        if 'error' in hava_data:
            return {"error": hava_data['error']}

        sicaklik = hava_data['main']['temp']
        weather_id = hava_data['weather'][0]['id']
        durum = hava_data['weather'][0]['description']
        category = self._get_category(weather_id, hava_data['weather'][0]['main'])
        yagmur_var = category in ('Rain', 'Drizzle', 'Thunderstorm')

        weather_info = {
            'sehir': hava_data['name'],
            'ulke': hava_data['sys']['country'],
            'sicaklik': round(sicaklik),
            'hissedilen': round(hava_data['main']['feels_like']),
            'durum': durum,
            'nem': hava_data['main']['humidity'],
            'ruzgar': hava_data['wind']['speed'],
        }

        _, oneri_tipi = self._rule_recommendation(hava_data, weather_id, sicaklik)
        llm_text = self._llm_recommendation(weather_info)

        if llm_text:
            oneri = llm_text
            kaynak = 'llm'
        else:
            oneri, _ = self._rule_recommendation(hava_data, weather_id, sicaklik)
            kaynak = 'rule'

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
            "tarih": datetime.now().strftime('%d.%m.%Y %H:%M'),
            "weather_category": category,
            "oneri_kaynagi": kaynak,
        }

    def calistir(self):
        hava_data = self.hava_durumunu_kontrol_et()
        return self.analiz_yap(hava_data)
