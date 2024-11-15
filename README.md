# İzin Günü Planlayıcı

Bu Python programı, bulunduğunuz yıl için en verimli izin günlerini planlamanıza yardımcı olur. Resmi tatilleri ve hafta sonlarını dikkate alarak, en uzun tatil dönemlerini oluşturacak şekilde izin günlerinizi optimize eder.

## Özellikler

- Bulunan yılın tüm resmi tatillerini içerir
- Maksimum izin gün sayısını belirleyebilme
- Hafta sonları ve resmi tatillerle birleştirilmiş en verimli izin günlerini önerir
- Oluşan uzun hafta sonu ve tatil dönemlerini listeler
- Yıl boyunca toplam tatil günü sayısını hesaplar

## Nasıl Kullanılır

1. Programı çalıştırın:

```bash
pip install -r requirements.txt
python main.py
```

2. İstediğiniz maksimum izin gün sayısını girin (varsayılan: 14 gün)
3. Cuma günleri 2 iş gün olarak sayılsın mı? (e/h, varsayılan h)
4. Hangi yıl için izinleri hesaplamak istersiniz? (varsayılan: 2025): 
   - Program, 2025 yılı için önerilen izin günlerini ve uzun tatil dönemlerini gösterecektir.
5. Program size:
   - Önerilen izin günlerini
   - Oluşan uzun tatil dönemlerini
   - Toplam tatil günü sayısını gösterecektir

## Çıktı Örneği

```
Maksimum izin günü sayısını girin (varsayılan 14):

2025 için Önerilen İzin Günleri (14 günün 14 günü kullanılıyor):

- 30 Aralık 2024, Pazartesi
- 31 Aralık 2024, Salı
- 02 Ocak 2025, Perşembe
- 03 Ocak 2025, Cuma
- 21 Nisan 2025, Pazartesi
- 22 Nisan 2025, Salı
- 24 Nisan 2025, Perşembe
- 25 Nisan 2025, Cuma
- 02 Mayıs 2025, Cuma
- 14 Temmuz 2025, Pazartesi
- 27 Ekim 2025, Pazartesi
- 28 Ekim 2025, Salı
- 30 Ekim 2025, Perşembe
- 31 Ekim 2025, Cuma

Uzun Hafta Sonu/Tatil Dönemleri:

- 28 Aralık ile 05 Ocak arası: 9 gün
- 29 Mart ile 01 Nisan arası: 4 gün
- 19 Nisan ile 27 Nisan arası: 9 gün
- 01 Mayıs ile 04 Mayıs arası: 4 gün
- 17 Mayıs ile 19 Mayıs arası: 3 gün
- 06 Haziran ile 09 Haziran arası: 4 gün
- 12 Temmuz ile 15 Temmuz arası: 4 gün
- 25 Ekim ile 02 Kasım arası: 9 gün

Toplam ardışık tatil günleri: 46
2025'te toplam tatil günleri (tüm haftasonları + resmi tatiller + izinler): 128
```

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır.
