from telethon.sync import TelegramClient, events
import re
from datetime import datetime
import requests
from keep_alive import keep_alive

keep_alive()

# === AYARLAR ===
api_id = 29120660
api_hash = 'a22e6c2850bc998882238f58bcfae60d'
session_name = 'promo_session'

# === TELEGRAM BOT BİLGİLERİ ===
bot_token = '7956014813:AAGfr-0JJtBW9wrF6NpAAXH2ECh0y9EF8oU'
chat_id = 5739354880

# === ANAHTAR KELİMELER ===
KEYWORDS = ["KOD", "PROMO"]

# === TAKİP EDİLECEK KANALLAR ===
ALLOWED_CHANNELS = [
    "@zbahis_com", "@zbahiscom", "@otobetcom", "@betkomtelegram",
    "@resmibetine", "@grandpashagir", "@TarafbetDuyuru", "@casinoroyalcom",
    "@asyaresmi", "@maltresmi", "@bahiscomtg", "@dumanresmi", "@fixofficial",
    "@matadorbetresmi", "@betpublicofficial", "@supertotobet_official",
    "@padisah_sosyal", "@dezodeneme"
]

# === BOT BAŞLIYOR ===
client = TelegramClient(session_name, api_id, api_hash)


@client.on(events.NewMessage)
async def handler(event):
    chat = await event.get_chat()
    try:
        chat_username = f"@{chat.username}" if chat.username else None
        if chat_username not in ALLOWED_CHANNELS:
            return

        text = event.raw_text
        for keyword in KEYWORDS:
            if re.search(rf"\b{keyword}\b", text, re.IGNORECASE):
                msg = f"📣 [ANAHTAR KELİME BULUNDU]\n\n" \
                      f"📌 Kanal: {chat_username}\n" \
                      f"🕐 Tarih: {datetime.now().strftime('%d.%m.%Y - %H:%M')}\n" \
                      f"📨 Mesaj:\n{text}"
                requests.post(
                    f"https://api.telegram.org/bot{bot_token}/sendMessage",
                    data={
                        "chat_id": chat_id,
                        "text": msg
                    })
                break
    except Exception as e:
        print(f"Hata: {e}")


async def on_start():
    requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage",
                  data={
                      "chat_id": chat_id,
                      "text": "🚀 Bot başlatıldı. Kanal dinlemesi aktif."
                  })


async def on_stop():
    requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage",
                  data={
                      "chat_id": chat_id,
                      "text": "⛔️ Bot durduruluyor. Kanal dinlemesi sona erdi."
                  })


print("✨ Bot başlatılıyor...")

with client:
    client.loop.run_until_complete(on_start())
    try:
        client.run_until_disconnected()
    finally:
        client.loop.run_until_complete(on_stop())
