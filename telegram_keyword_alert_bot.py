from telethon.sync import TelegramClient, events
import re
from datetime import datetime
import asyncio

# === AYARLAR ===
api_id = 29120660
api_hash = 'a22e6c2850bc998882238f58bcfae60d'
session_name = 'promo_session'

# === ANAHTAR KELİMELER ===
KEYWORDS = ["KOD", "PROMO"]

# === EMOJI ID KOMBINASYONLARI ===
EMOJI_COMBOS = [
    ["5305615921572757257", "5305579156652700515", "5305631211656328976"],  # KOD
    ["5305628505826933043", "5305579156652700515", "5305631211656328976", "5305598595674684337"]  # CODE
]

# === TAKİP EDİLECEK KANALLAR ===
ALLOWED_CHANNELS = [
    "@zbahis_com", "@zbahiscom", "@otobetcom", "@betkomtelegram", "@resmibetine",
    "@grandpashagir", "@TarafbetDuyuru", "@casinoroyalcom", "@asyaresmi", "@maltresmi",
    "@bahiscomtg", "@dumanresmi", "@fixofficial", "@matadorbetresmi",
    "@betpublicofficial", "@supertotobet_official", "@padisah_sosyal"
]

client = TelegramClient(session_name, api_id, api_hash)

def contains_keyword(text):
    return any(re.search(rf"\b{kw}\b", text, re.IGNORECASE) for kw in KEYWORDS)

def contains_combo_entities(entities):
    entity_ids = [getattr(e, 'document_id', None) for e in entities if getattr(e, 'document_id', None)]
    for combo in EMOJI_COMBOS:
        if all(cid in entity_ids for cid in combo):
            return True
    return False

@client.on(events.NewMessage)
async def handler(event):
    chat = await event.get_chat()
    chat_username = f"@{chat.username}" if chat.username else None
    if chat_username not in ALLOWED_CHANNELS:
        return

    text = event.raw_text
    entities = event.message.entities or []

    if contains_keyword(text) or contains_combo_entities(entities):
        msg = (
            "📣 [ANAHTAR KELİME / EMOJİ TETİKLENDİ]\n\n"
            f"📌 Kanal: {chat_username}\n"
            f"🕒 Tarih: {datetime.now().strftime('%d.%m.%Y - %H:%M')}\n"
            f"💬 Mesaj:\n{text}"
        )
        await client.send_message("me", msg)

print("✨ Bot başlatılıyor...")
client.start()
client.run_until_disconnected()
