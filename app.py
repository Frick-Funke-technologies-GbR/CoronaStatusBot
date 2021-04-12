import os
import re
from flask import Flask, request, render_template, send_file, abort
import telegram
from telebot.credentials import bot_token, bot_user_name, URL
import telebot
import json
import time
from cache.cache_handler import global_cache
from telebot.api_handler.metadata_api_parser import api_parser
from message_parser import message_parser

global bot
global TOKEN
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)
cache = global_cache()
metadata_api = api_parser()
msg_parser = message_parser()


@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
   # retrieve the message in JSON and then transform it to Telegram object
   update = telegram.Update.de_json(request.get_json(force=True), bot)
   print(request.get_json(force=True))

   chat_id = update.message.chat.id

   # store chat_id in cache
   stored = cache.store_chat_id(chat_id)
   print('[DEBUG:app_01] store_chat_id() outputs: ', stored)
  #  if not stored:
  #    bot.send_message(chat_id=chat_id, text='[ERROR_CODE_1] An error occured. For more info, please create an issue at https://github.com/HajFunk/CoronaStatus/issues.')

   if stored:
     print('[DEBUG:app_01.1] stored user_id successfully')
    #  bot.send_message(chat_id=chat_id, text=str(chat_id))

   msg_id = update.message.message_id

   bug = False

   if not update.message.text:
     bot.sendMessage(
         chat_id=chat_id, text='An error occured with this message.', reply_to_message_id=msg_id)
     print(
         f'[DEBUG_ERROR:app_02] An error occured with the sent message being {update.message.text}')
     text = update.message.text
     bug = True

   if not bug:
    # Telegram understands UTF-8, so encode text for unicode compatibility
    text = update.message.text.encode('utf-8').decode().lower()
    # for debugging purposes only

   # caches the message under the chat_id
   if cache.store_chat_messages(chat_id, text):
     print(f'[DEBUG:app_03] recieved and cached message successfully: {text}')
   else:
     print(f'[DEBUG_ERROR_SOFT:app_03] recieved message but didn\'t cached it: {text}')
     
   # the first time you chat with the bot AKA the welcoming message
   if text == "/start":
       # print the welcoming message
       bot_welcome = """
       Welcome to CoronaStatus bot. This bot sends you certified corona status updates as well as news around corona in Germany.
       """
       # send the welcoming message
       bot.sendMessage(chat_id=chat_id, text=bot_welcome, reply_to_message_id=msg_id)

   elif not bug:
     msg_parser.find_task_in_message(chat_id, text, msg_id)

   return 'ok'

@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    # we use the bot object to link the bot to our app which live
    # in the link provided by URL
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
    # something to let us know things work
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"

@app.route('/')
def index():
  return render_template("index.html")

if __name__ == '__main__':
  # note the threaded arg which allow
  # your app to have more than one thread
  app.run(threaded=True)
  # TODO: Add scheduler => in differend thread
