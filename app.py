
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from agent import HavaDurumuAgent
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder='frontend', static_url_path='')
CORS(app)

API_KEY = os.getenv('OPENWEATHER_API_KEY')
ANTHROPIC_KEY = os.getenv('ANTHROPIC_API_KEY')

if not API_KEY:
    print("⚠️  UYARI: OPENWEATHER_API_KEY bulunamadı! .env dosyasını kontrol edin.")

@app.route('/')
def index():
    """Ana sayfa"""
    return send_from_directory('frontend', 'index.html')

@app.route('/api/hava-durumu', methods=['POST'])
def hava_durumu():
    """Hava durumu sorgulama endpoint'i"""
    try:
        data = request.get_json()
        sehir = data.get('sehir', 'Istanbul')
        lang = data.get('lang', 'tr')

        if not API_KEY:
            return jsonify({
                "error": "API key tanımlanmamış. Lütfen .env dosyasını kontrol edin."
            }), 500

        agent = HavaDurumuAgent(sehir, API_KEY, lang=lang, anthropic_key=ANTHROPIC_KEY)
        sonuc = agent.calistir()
        
        # Hata kontrolü
        if 'error' in sonuc:
            return jsonify(sonuc), 400
        
        return jsonify(sonuc), 200
        
    except Exception as e:
        return jsonify({
            "error": f"Beklenmeyen hata: {str(e)}"
        }), 500

@app.route('/api/health', methods=['GET'])
def health():
    if not API_KEY:
        return jsonify({
            "status": "unhealthy",
            "service": "weather-forecast-agent"
        }), 500

    return jsonify({
        "status": "healthy",
        "service": "weather-forecast-agent"
    }), 200

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
