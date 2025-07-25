import telebot
import socket
import requests
import platform

# === Token del bot ===
TOKEN = '7305607951:AAGARhR5uw2SJKUAvulM-p55Iq_AFAiObZ4'
bot = telebot.TeleBot(TOKEN)

# === /start ===
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "😈 Bienvenido a AnonX_ToolsBot\nUsa /version para ver mis comandos.")

# === /ping sitio.com ===
@bot.message_handler(commands=['ping'])
def ping(message):
    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "❗ Usa: /ping <sitio>")
        return

    sitio = args[1]
    if not sitio.startswith("http"):
        sitio = "http://" + sitio

    try:
        r = requests.get(sitio, timeout=5)
        bot.reply_to(message, f"✅ {sitio} respondió con código {r.status_code} en {r.elapsed.total_seconds()} segundos.")
    except Exception as e:
        bot.reply_to(message, f"❌ Error al hacer ping: {str(e)}")

# === /info sitio.com ===
@bot.message_handler(commands=['info'])
def info(message):
    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "❗ Usa: /info <sitio>")
        return

    sitio = args[1].replace("http://", "").replace("https://", "").split("/")[0]
    try:
        ip = socket.gethostbyname(sitio)
        headers = requests.get("http://" + sitio, timeout=5).headers
        msg = f"🌐 Información de {sitio}:\n\nIP: {ip}\nServer: {headers.get('Server')}\nContent-Type: {headers.get('Content-Type')}"
        bot.reply_to(message, msg)
    except Exception as e:
        bot.reply_to(message, f"❌ No se pudo obtener info: {str(e)}")

# === /version ===
@bot.message_handler(commands=['version'])
def version(message):
    msg = f"""🤖 *AnonX_ToolsBot v1.0*

📌 Comandos disponibles:
  /ping <sitio> – Mide respuesta web
  /info <sitio> – Muestra IP y headers
  /version – Muestra esta info

🧠 Python {platform.python_version()}
🖥️ OS: {platform.system()} {platform.release()}
"""
    bot.reply_to(message, msg, parse_mode="Markdown")

# === Loop infinito del bot ===
print("✅ Bot encendido")
bot.infinity_polling()
