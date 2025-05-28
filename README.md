# DetectLanguage MCP

Bu proje, DetectLanguage.com API'sini kullanarak metin dil algılama işlemi yapan bir MCP (Model Context Protocol) servisidir.

## Özellikler

- DetectLanguage.com API entegrasyonu
- Flask web sunucusu
- RESTful API endpoint'leri
- Docker desteği
- Hata yönetimi ve logging
- Sağlık kontrolü endpoint'i

## API Endpoints

### GET /
API bilgileri ve kullanım kılavuzu

### GET /health
Servis sağlık kontrolü

### GET/POST /detect
Metin dil algılama

**GET Kullanımı:**
```
GET /detect?text=Hello world
```

**POST Kullanımı:**
```json
POST /detect
Content-Type: application/json

{
    "text": "Hello world"
}
```

**Yanıt Formatı:**
```json
{
    "success": true,
    "language": "en",
    "confidence": 11.94,
    "is_reliable": true,
    "text": "Hello world",
    "request_method": "GET",
    "timestamp": "2024-01-01T12:00:00.000000"
}
```

## Kurulum ve Çalıştırma

### 1. Gereksinimler
```bash
pip install -r requirements.txt
```

### 2. Doğrudan Çalıştırma
```bash
python server.py
```

### 3. Docker ile Çalıştırma
```bash
# Docker image oluştur
docker build -t detectlanguage-mcp .

# Container çalıştır
docker run -p 5000:5000 detectlanguage-mcp
```

### 4. Environment Variables
- `DETECTLANGUAGE_API_KEY`: DetectLanguage API anahtarı (varsayılan: ba3b71e93a655b554f1df2f4b2b1e82b)
- `PORT`: Sunucu portu (varsayılan: 5000)
- `HOST`: Sunucu host'u (varsayılan: 0.0.0.0)
- `FLASK_DEBUG`: Debug modu (varsayılan: False)

## Test

### Curl ile Test
```bash
# GET request
curl "http://localhost:5000/detect?text=Hello world"

# POST request
curl -X POST http://localhost:5000/detect \
  -H "Content-Type: application/json" \
  -d '{"text": "Bonjour le monde"}'

# Sağlık kontrolü
curl http://localhost:5000/health
```

### Python ile Test
```python
import requests

# Test GET request
response = requests.get("http://localhost:5000/detect?text=Hello world")
print(response.json())

# Test POST request
response = requests.post(
    "http://localhost:5000/detect",
    json={"text": "Hola mundo"}
)
print(response.json())
```

## Dosya Yapısı

```
.
├── app.py              # DetectLanguage API client
├── server.py           # Flask sunucusu
├── requirements.txt    # Python bağımlılıkları
├── Dockerfile         # Docker yapılandırması
├── smithery.yaml      # MCP yapılandırması
└── README.md          # Bu dosya
```

## API Anahtarı

Proje varsayılan olarak `ba3b71e93a655b554f1df2f4b2b1e82b` API anahtarını kullanır. 
Kendi API anahtarınızı kullanmak için `DETECTLANGUAGE_API_KEY` environment variable'ını ayarlayın.

## Desteklenen Diller

DetectLanguage API 164 farklı dili destekler. Tam liste için:
```bash
curl https://ws.detectlanguage.com/0.2/languages
```

## Hata Yönetimi

API aşağıdaki hata durumlarını yönetir:
- Boş metin
- Geçersiz API anahtarı
- Rate limit aşımı
- Ağ bağlantı hataları
- API timeout'ları

## Lisans

MIT License
