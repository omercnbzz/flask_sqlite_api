# Simple Book API with Flask & SQLite

Bu proje, Python'da Flask kullanarak oluşturulmuş basit bir REST API örneğidir. Veriler SQLite veritabanında saklanmakta ve `/books` endpoint’i üzerinden sunulmaktadır.

## Bileşenler

- **Flask**: REST API için
- **SQLite**: Hafif veritabanı
- **Python**: 3.x

## Dosyalar

- `create_db.py`: Veritabanını oluşturur ve örnek kitap verilerini ekler.
- `api.py`: Flask sunucusunu başlatır ve `/books` endpoint’ini sağlar.

## Kurulum ve Kullanım

### 1. Ortamı Kurun

```bash
pip install flask
