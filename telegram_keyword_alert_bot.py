from telethon.sync import TelegramClient, events
from telethon.tl.types import MessageEntityCustomEmoji
import re
from datetime import datetime
import requests

# === AYARLAR ===
api_id = 29120660
api_hash = 'a22e6c2850bc998882238f58bcfae60d'
session_name = 'promo_session'
bot_token = '7956014813:AAGfr-0JJtBW9wrF6NpAAXH2ECh0y9EF8oU'
chat_id = 5739354880

# === ANAHTAR KELİMELER ===
KEYWORDS = ["KOD", "PROMO"]

# === TAKİP EDİLECEK KANALLAR ===
ALLOWED_CHANNELS = [
    "@zbahis_com", "@zbahiscom", "@otobetcom", "@betkomtelegram",
    "@resmibetine", "@grandpashagir", "@TarafbetDuyuru", "@casinoroyalcom",
    "@asyaresmi", "@maltresmi", "@bahiscomtg", "@dumanresmi", "@fixofficial",
    "@matadorbetresmi", "@betpublicofficial", "@supertotobet_official", "@padisah_sosyal"
]

# === EMOJI KOMBINASYONLARI ===
KOD_COMBO = [
    5305615921572757257,  # K
    5305579156652700515,  # O
    5305631211656328976   # D
]

CODE_COMBO = [
    5305628505826933043,  # C
    5305579156652700515,  # O
    5305631211656328976,  # D
    5305598595674684337   # E
]

client = TelegramClient(session_name, api_id, api_hash)

def contains_sequence(full_list, sub_list):
    for i in range(len(full_list) - len(sub_list) + 1):
        if full_list[i:i + len(sub_list)] == sub_list:
            return True
    return False

@client.on(events.NewMessage)
async def handler(event):
    sender = await event.get_sender()
    chat = await event.get_chat()

    try:
        chat_username = f"@{chat.username}" if chat.username else None
        if chat_username not in ALLOWED_CHANNELS:
            return

        text = event.raw_text
        for keyword in KEYWORDS:
            if re.search(rf"\b{keyword}\b", text, re.IGNORECASE):
                msg = f"📣 [ANAHTAR KELİME BULUNDU]\n\n"                       f"📍 Kanal: {chat_username}\n"                       f"🕒 Tarih: {datetime.now().strftime('%d.%m.%Y - %H:%M')}\n"                       f"💬 Mesaj:\n{text}"
                await client.send_message("me", msg)
                requests.get(f"https://api.telegram.org/bot{bot_token}/sendMessage",
                             params={"chat_id": chat_id, "text": msg})
                break

        # Emoji kombinasyon kontrolü
        emoji_sequence = []
        if event.message.entities:
            for entity in event.message.entities:
                if isinstance(entity, MessageEntityCustomEmoji):
                    emoji_sequence.append(entity.document_id)

        if contains_sequence(emoji_sequence, KOD_COMBO):
            await client.send_message("me", "🔑 KOD emoji kombinasyonu tespit edildi!")

        elif contains_sequence(emoji_sequence, CODE_COMBO):
            await client.send_message("me", "🆔 CODE emoji kombinasyonu tespit edildi!")

    except Exception as e:
        print(f"Hata: {e}")

print("✨ Bot başlatılıyor...")
client.start()
client.run_until_disconnected()
