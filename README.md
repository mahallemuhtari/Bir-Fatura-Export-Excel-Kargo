# BirFatura Export Bot

BirFatura sisteminden otomatik olarak rapor indiren bir bot.

## Kurulum

1. Python 3.6 veya üzeri sürümü yükleyin
2. ChromeDriver'ı yükleyin:
   ```bash
   brew install chromedriver
   ```
3. Gerekli Python paketlerini yükleyin:
   ```bash
   pip install -r requirements.txt
   ```

## Yapılandırma

`config/credentials.py` dosyasında BirFatura giriş bilgilerinizi güncelleyin:

```python
EMAIL = "your-email@example.com"
PASSWORD = "your-password"
```

## Kullanım

Botu çalıştırmak için:

```bash
python main.py
```

Bot otomatik olarak:
1. BirFatura sistemine giriş yapar
2. Satış faturaları sayfasına gider
3. Bir önceki günün raporunu indirir

## Proje Yapısı

```
BirFaturaExportBot/
├── src/
│   ├── bot/
│   │   ├── bir_fatura_bot.py  # Ana bot sınıfı
│   │   └── config.py          # Bot yapılandırması
│   └── utils/
│       └── browser.py         # Tarayıcı yardımcı fonksiyonları
├── config/
│   └── credentials.py         # Giriş bilgileri
├── requirements.txt           # Python paket gereksinimleri
├── README.md                  # Bu dosya
└── main.py                    # Ana program
``` 