# 📚 Python 202 Bootcamp - Kütüphane Uygulaması

Bu proje, **Global AI Hub Python 202 Bootcamp** kapsamında geliştirilmiş basit bir **Kütüphane Yönetim Sistemi**dir.  
Kitap ekleme, listeleme, silme ve arama gibi işlemler yapılabilir. Ayrıca **FastAPI** tabanlı bir REST API de içerir.  

---

## 🚀 Özellikler

- ISBN numarasıyla kitap ekleme (OpenLibrary API kullanarak)
- Kitapları listeleme
- Kitap silme
- Kitap arama
- Hem **komut satırı (CLI)** hem de **REST API** üzerinden kullanım
- JSON dosyasında kalıcı veri saklama
- Birim testleri (pytest)

---

## 🛠️ Kurulum

Öncelikle gerekli paketleri yükleyin:

```bash

pip install -r requirements.txt

requirements.txt içinde şunlar bulunur:
httpx
fastapi
uvicorn
pytest

📌 Kullanım
1️⃣ CLI (Komut Satırı)
python main.py
Menü üzerinden şu işlemleri yapabilirsiniz:

-Kitap ekle (ISBN ile)

-Kitap sil

-Kitapları listele

-Kitap ara

-Çıkış

2️⃣ API (FastAPI)

API'yi başlatmak için:

uvicorn api:app --reload
Varsayılan olarak http://127.0.0.1:8000
adresinde çalışır.

📖 API Dokümantasyonu:

Swagger UI → http://127.0.0.1:8000/docs

Redoc → http://127.0.0.1:8000/redoc
Kitap ekle (POST)
POST /books
{
  "isbn": "9780140328721"
}

✅ Testler

Pytest ile testleri çalıştırabilirsiniz:
pytest
