# TitanyumTPSX

**TitanyumTPSX**, Minecraft sunucularının anlık durumunu takip eden ve bu bilgileri sürekli güncelleyerek belirli bir Discord kanalında paylaşan Python tabanlı bir Discord botudur.

## 🔧 Özellikler

- 🎮 Minecraft sunucusunun çevrimiçi/çevrimdışı durumunu, ping'ini ve oyuncu sayısını kontrol eder.
- 🔁 Her **120 saniyede bir** sunucuyu otomatik olarak kontrol eder.
- 📝 Bilgileri bir **Discord mesajı** olarak gönderir ve daha sonra bu mesajı **düzenleyerek günceller**.
- 💬 Bilgiler sabit bir mesajda sürekli güncellenerek paylaşılır (spam yapmaz).
- ⚙️ 24/7 çalışmaya uygundur (örneğin Replit, UptimeRobot, kendi sunucunuzda çalıştırılabilir).

## 🐍 Gereksinimler

- Python 3.8 veya üzeri
- `discord.py` kütüphanesi
- `mcstatus` kütüphanesi

## 💾 Kurulum

### 1. Depoyu Klonlayın

```bash
git clone https://github.com/kullaniciAdi/TitanyumTPSX.git
cd TitanyumTPSX
