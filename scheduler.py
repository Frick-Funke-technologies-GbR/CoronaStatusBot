from datetime import datetime
from telebot.credentials import bot_token
from cache.cache_handler import global_cache
from telebot.api_handler.metadata_api_parser import api_parser
from telebot.rssHANDLER.run import rssParser
import telegram
import time
import json
import os

# TODO: add functionality for different countries 
class scheduler:

    def __init__(self):
        TOKEN = bot_token
        self.bot = telegram.Bot(token=TOKEN)
        self.cache = global_cache()
        self.metadata_api = api_parser()
        self.running = True
        #rssHandler:
        self.rssHANDLER = rssParser()
        self.cacheDirectory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache")
        with open(os.path.join(self.cacheDirectory, "SORTEDtagesschau-articles.json"), 'r') as filedataS:
            dataS = filedataS.read()
            self.SORTEDtagesschau = json.loads(dataS)
        with open(os.path.join(self.cacheDirectory, "tagesschauVideoPodcastLink.json"), 'r') as filedataV:
            dataV = filedataV.read()
            self.tagesschauVideoPodcastLink = json.loads(dataV)
        self.tag100sekLink = self.tagesschauVideoPodcastLink["https://www.tagesschau.de/export/video-podcast/webxl/tagesschau-in-100-sekunden_https/"][0]["enclosure"]["href"]
        self.tag100sekTitel = self.tagesschauVideoPodcastLink["https://www.tagesschau.de/export/video-podcast/webxl/tagesschau-in-100-sekunden_https/"][0]["description"]
    
    def schedule(self):
        print('point1')
        while self.running:
            self.rssHANDLER.go() # download tagesschaudata every 10 minutes
            # check current time TODO: evtl. add time zone ('%z')
            current_time = datetime.now().strftime('%H')
            print(current_time)
            if current_time == '08':
                chat_ids = self.cache.get_chat_ids() # important: don't add a self. to this variable

                # FIXME: put following code for get_country_info in sepperate file (telebot/api_handler/handler.py)
                metadata_total_cases = self.metadata_api.get_by_key_and_date('total_cases')
                metadata_new_cases = self.metadata_api.get_by_key_and_date('new_cases')
                metadata_total_deaths = self.metadata_api.get_by_key_and_date('total_deaths')
                metadata_new_deaths = self.metadata_api.get_by_key_and_date('new_deaths')

                message = 'Guten Morgen!\nHier der aktuelle (gestrige) Corona-Stand in Deutschland:\n\n'
                message += f'Alle infektionsfälle: {metadata_total_cases}\n'
                message += f'Neue infektionsfälle: {metadata_new_cases}\n'
                message += f'Alle todesfälle: {metadata_total_deaths}\n'
                message += f'Neue todesfälle: {metadata_new_deaths}\n\n'
                message += f'{self.tag100sekTitel} gibt es hier:\n'
                message += f'{self.tag100sekLink}'
                message += 'Die letzten 3 Schlagzeilen auf Tagesschau.de über das Corona Virus:'
                i = 0
                while i < 3:
                    message += f'{self.SORTEDtagesschau[i]["title"]}\n'
                    message += f'Zum ganzen Artikel geht es hier: {self.SORTEDtagesschau[i]["link"]}\n\n'
                    i += 1
                message += 'Für weitere Meldungen und die aktuellen Zahlen geben sie bitte "/update" ein.'
                print('[DEBUG scheduler]send scheduled message:' + message)               

                for chat in chat_ids:
                    self.bot.send_message(text=message, chat_id=chat)

            if current_time == '20':
                chat_ids = self.cache.get_chat_ids() # important: don't add a self. to this variable

                message += 'Guten Abend!\nHier der aktuelle Nachrichtenstand:\n\n'
                message += f'{self.tag100sekTitel} gibt es hier:\n'
                message += f'{self.tag100sekLink}'
                message += 'Die letzten 3 Schlagzeilen auf Tagesschau.de über das Corona Virus:'
                i = 0
                while i < 3:
                    message += f'{self.SORTEDtagesschau[i]["title"]}\n'
                    message += f'Zum ganzen Artikel geht es hier: {self.SORTEDtagesschau[i]["link"]}\n\n'
                    i += 1
                message += 'Für weitere Meldungen und die aktuellen Zahlen geben sie bitte "update" ein.'
                print('[DEBUG scheduler]send scheduled message:' + message)               

                for chat in chat_ids:
                    self.bot.send_message(text=message, chat_id=chat)

            # sleep for 10 minutes
            time.sleep(600)

