import os
import threading
import http.server
import socketserver
from pyngrok import ngrok
from pyrogram import Client, filters

# --- تنظیمات از Secrets ---
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# --- راه‌اندازی کلاینت تلگرام ---
app = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# --- راه‌اندازی سرور فایل ---
PORT = int(os.getenv("PORT", "8000"))
handler = http.server.SimpleHTTPRequestHandler
httpd = socketserver.TCPServer(("", PORT), handler)

thread = threading.Thread(target=httpd.serve_forever)
thread.daemon = True
thread.start()

# --- راه‌اندازی ngrok ---
ngrok_token = os.getenv("NGROK_AUTH_TOKEN")
if ngrok_token:
    ngrok.set_auth_token(ngrok_token)

http_tunnel = ngrok.connect(PORT, bind_tls=True)
public_url = http_tunnel.public_url
print(f"🌍 Public URL: {public_url}")

# --- هندل پیام استارت ---
@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("👋 سلام! فایل یا ویدیو رو بفرست تا لینک دانلود عمومی برات بسازم.")

# --- هندل فایل‌ها
