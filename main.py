import telebot
import os
import speech_recognition as sr
from pydub import AudioSegment

#Токен
TOKEN = ''
bot = telebot.TeleBot(TOKEN)

#Временное хранение голосовых
TEMP_PATH = "/temp gs"

if not os.path.exists(TEMP_PATH):
    os.makedirs(TEMP_PATH)
#Функция конвертации
def convert_ogg_to_wav(file_path):
    audio = AudioSegment.from_ogg(file_path)
    wav_path = file_path.replace(".ogg", ".wav")
    audio.export(wav_path, format="wav")
    return wav_path

@bot.message_handler(content_types=['voice'])
def handle_voice_message(message):
    #Загрузка голосового
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    
    #Сохранения временного гс
    ogg_path = os.path.join(TEMP_PATH, f"{message.chat.id}.ogg")
    with open(ogg_path, 'wb') as f:
        f.write(downloaded_file)
    
    try:
        #Конвертация
        wav_path = convert_ogg_to_wav(ogg_path)

        #Распознование
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language="ru-RU")  # Укажите нужный язык
        
        #Отправление
        bot.reply_to(message, f"Распознанный текст: {text}")
        
        #Тут можно написать код для сохранения текста в переменную или в базу данных

    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка при обработке сообщения: {str(e)}")
    finally:
        #Удаление временного голосового
        if os.path.exists(ogg_path):
            os.remove(ogg_path)
        if os.path.exists(wav_path):
            os.remove(wav_path)

#Запуск
bot.polling(none_stop=True)
