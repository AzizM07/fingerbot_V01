
import os
from telethon import TelegramClient
from flask import Flask, request, jsonify
from flask_cors import CORS
import asyncio
import threading


SESSION_BASE64 = os.environ.get('SESSION_BASE64')

if SESSION_BASE64:
    import base64
    session_bytes = base64.b64decode(SESSION_BASE64)
    with open('fingerbot_session.session', 'wb') as f:
        f.write(session_bytes)
    print("✅ Session chargée depuis variable d'environnement")


API_ID = 31068656
API_HASH = '75a1c488c72c717615f5ea978d62f436'
BOT_USERNAME = 'AzizFingerbot_bot'


client = TelegramClient('fingerbot_session', API_ID, API_HASH)

async def send_telegram_message(message):
    """Fonction async pour envoyer le message"""
    await client.send_message(BOT_USERNAME, message)
    print(f"✅ Message envoyé: {message}")


app = Flask(__name__)
CORS(app)

loop = None

def run_async(coro):
    """Exécute une coroutine dans la boucle du thread Telegram"""
    future = asyncio.run_coroutine_threadsafe(coro, loop)
    return future.result(timeout=10)

@app.route('/command', methods=['POST'])
def handle_command():
    try:
        data = request.get_json()
        command = data.get('command')
        
        if not command:
            return jsonify({'status': 'error'}), 400
        
        # Envoyer via la boucle asyncio
        run_async(send_telegram_message(command))
        
        return jsonify({'status': 'ok', 'command': command})
    
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/status', methods=['GET'])
def status():
    return jsonify({'status': 'ok', 'bot': BOT_USERNAME})


def telegram_loop_thread():
    """Thread dédié pour la boucle asyncio de Telegram"""
    global loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    async def main():
        await client.start()
        print("✅ Connecté à Telegram")
        await client.run_until_disconnected()
    
    loop.run_until_complete(main())


if __name__ == '__main__':
    print("=== FINGERBOT USERBOT API ===")
    print(f"Bot: @{BOT_USERNAME}\n")
    
    print("Démarrage Telegram...")
    t = threading.Thread(target=telegram_loop_thread, daemon=True)
    t.start()
    
    import time
    time.sleep(3)
    
    print("\nServeur Flask sur http://0.0.0.0:5000\n")
    
    
    port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)