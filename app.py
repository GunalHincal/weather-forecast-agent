
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from agent import HavaDurumuAgent
import os
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

app = Flask(__name__, static_folder='frontend', static_url_path='')
CORS(app)  # CORS'u etkinleştir

# API key'i environment variable'dan al

API_KEY = os.getenv('OPENWEATHER_API_KEY')

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
        
        if not API_KEY:
            return jsonify({
                "error": "API key tanımlanmamış. Lütfen .env dosyasını kontrol edin."
            }), 500
        
        # Agent'ı oluştur ve çalıştır
        agent = HavaDurumuAgent(sehir, API_KEY)
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
    """Health check endpoint"""
    return jsonify({
        "status": "ok",
        "api_key_configured": bool(API_KEY)
    }), 200

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
