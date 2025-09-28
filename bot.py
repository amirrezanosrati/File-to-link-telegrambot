import os
import threading
import http.server
import socketserver
from pyngrok import ngrok
from pyrogram import Client, filters

# مقداردهی اولیه بات
API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')
BOT_TOKEN = os.getenv('BOT_TOKEN')
app = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# راه‌اندازی سرور فایل ساده
PORT = int(os.getenv('PORT', '8000'))
handler = http.server.SimpleHTTPRequestHandler
httpd = socketserver.TCPServer(("", PORT), handler)
thread = threading.Thread(target=httpd.serve_forever)
thread.daemon = True
thread.start()

# ngrok
http_tunnel = ngrok.connect(PORT, bind_tls=True)
public_url = http_tunnel.public_url
print(f"🌍 Public URL: {public_url}")

# هندلر فایل
@app.on_message(filters.document | filters.video | filters.audio)
async def handle_file(client, message):
    file_path = await client.download_media(message)
    filename = os.path.basename(file_path)
    download_link = f"{public_url}/{filename}"
    await message.reply_text(f"🔗 لینک دانلود فایل شما:\n{download_link}")

app.run()
