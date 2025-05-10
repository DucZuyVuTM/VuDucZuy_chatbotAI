import os
import time
import telebot
from flask import Flask, request

from chatbotAI import chatbotAI

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
API_URL = os.getenv("API_URL")
API_KEY = os.getenv("API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "Bot is running!", 200

@app.route('/webhook', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '', 200

@bot.message_handler(commands=['start'])
@bot.message_handler(commands=['help'])
def start(message):
    try:
        bot.send_message(message.chat.id, "Hello! This is VuDucZuy_chatbotAI" +
                        "\nYou can write the prompt you want to generate text for right in this chat.")
    except Exception as e:
        bot.send_message(6180286860, e)
        bot.send_message(6180286860, "Error from user:" +
                        "\nID: " + str(message.from_user.id) +
                        "\nUsername: @" + str(message.from_user.username), parse_mode='MarkdownV2')
        
@bot.message_handler(func=lambda message: True)
def generate_answer(message):
    try:
        bot.send_message(message.chat.id, "Started generating text:"
                        + "\nYou can wait for at least 1 minute, but you can have a cup of coffee and take a nap while you wait! ☕"
                        + "\nGenerating answer...")
        start = time.time()
        result, status = chatbotAI(API_KEY, API_URL, message.text)
        end = time.time()
        t = end - start
        if t < 60:
            time.sleep(60 - t)
        
        if status == "OK":
            print(result)
            clean_message = result.replace("### ", "➡️ ").strip()
            clean_message = clean_message.replace("**", "*").strip()
            # Thoát các ký tự đặc biệt, nhưng không thoát ký tự định dạng
            for char in ["-", ".", "+", "=", "~", "|", "!", "#", "(", ")", "<", ">", "{", "}", "]", "["]:
                if char in clean_message:
                    clean_message = clean_message.replace(char, f"\\{char}")
            bot.send_message(message.chat.id, clean_message, parse_mode="MarkdownV2")
        elif status == "ERROR":
            bot.send_message(6180286860, result)
            bot.send_message(6180286860, "Error from user:" +
                            "\nID: `" + str(message.from_user.id) +
                            "`\nUsername: @" + str(message.from_user.username), parse_mode='MarkdownV2')
    except Exception as e:
        bot.send_message(6180286860, e)
        bot.send_message(6180286860, "Error from user:" +
                        "\nID: `" + str(message.from_user.id) +
                        "`\nUsername: @" + str(message.from_user.username), parse_mode='MarkdownV2')

@app.route('/set_webhook', methods=['GET'])
def set_webhook():
    webhook_url = "https://vuduczuy-chatbotai.onrender.com/webhook"
    bot.remove_webhook()
    bot.set_webhook(url=webhook_url)
    return "Webhook set", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)