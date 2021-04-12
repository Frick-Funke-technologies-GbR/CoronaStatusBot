import re
import telegram
from telebot.credentials import bot_token
from cache.cache_handler import global_cache
from telebot.api_handler.metadata_api_parser import api_parser
from telebot.rssHANDLER.run import rssParser
import json
import os



class message_parser:

    def __init__(self):
        TOKEN = bot_token
        self.bot = telegram.Bot(token=TOKEN)
        self.cache = global_cache()
        self.metadata_api = api_parser()
        #rssHandler:
        self.rssHANDLER = rssParser()
        self.rssHANDLER.go()
        self.cacheDirectory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache")
        with open(os.path.join(self.cacheDirectory, "SORTEDtagesschau-articles.json"), 'r') as filedataS:
            dataS = filedataS.read()
            self.SORTEDtagesschau = json.loads(dataS)
        with open(os.path.join(self.cacheDirectory, "UNSORTEDtagesschau-articles.json"), 'r') as filedataU:
            dataU = filedataU.read()
            self.UNSORTEDtagesschau = json.loads(dataU)
        with open(os.path.join(self.cacheDirectory, "tagesschauVideoPodcastLink.json"), 'r') as filedataV:
            dataV = filedataV.read()
            self.tagesschauVideoPodcastLink = json.loads(dataV)
        self.tag100sekLink = self.tagesschauVideoPodcastLink["https://www.tagesschau.de/export/video-podcast/webxl/tagesschau-in-100-sekunden_https/"][0]["enclosure"]["href"]
        self.tag100sekTitel = self.tagesschauVideoPodcastLink["https://www.tagesschau.de/export/video-podcast/webxl/tagesschau-in-100-sekunden_https/"][0]["description"]


    def find_whole_word(self, w):
        return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

    def find_task_in_message(self, chat_id, text, msg_id):

        # make it not case sensitive
        text = text.lower()

        if text == '/update':
            self.rssHANDLER.go()
            # TODO: implementation of rssHANDLER

            # implementation of api_handler (TODO: not complete yet)
            metadata_total_cases = self.metadata_api.get_by_key_and_date('total_cases')
            metadata_new_cases = self.metadata_api.get_by_key_and_date('new_cases')
            metadata_total_deaths = self.metadata_api.get_by_key_and_date('total_deaths')
            metadata_new_deaths = self.metadata_api.get_by_key_and_date('new_deaths')

            message = 'Hier der aktuelle (gestrige) Corona-Stand in Deutschland:\n\n'
            message += f'Alle infektionsfälle: {metadata_total_cases}\n'
            message += f'Neue infektionsfälle: {metadata_new_cases}\n'
            message += f'Alle todesfälle: {metadata_total_deaths}\n'
            message += f'Neue todesfälle: {metadata_new_deaths}\n\n'
            message += f'{self.tag100sekTitel} gibt es hier:\n'
            message += f'{self.tag100sekLink}\n\n'
            message += f'Die letzten {len(self.SORTEDtagesschau)} Schlagzeilen auf Tagesschau.de über das Corona Virus:\n\n'
            i = 0
            while i < len(self.SORTEDtagesschau):
                message += f'{self.SORTEDtagesschau[i]["title"]}\n'
                message += f'Zum ganzen Artikel geht es hier: {self.SORTEDtagesschau[i]["link"]}\n\n'
                i += 1
            print('\n[DEBUG:message_parser_01] send message:\n::::::::\n' + message + '\n::::::::\n')

            self.bot.sendMessage(chat_id=chat_id, text=message, reply_to_message_id=msg_id)

        elif text == '/help':
            
            keywords = self.cache.get_possible_chat_keywords()

            message = 'Mögliche Schlüsselwörter:\n\n'
            
            for keyword in keywords:
                message += f'{keyword}: {keywords[keyword]}\n'

            print('\n[DEBUG:message_parser_02] send message:\n::::::::\n' + message + '\n::::::::\n')

            self.bot.sendMessage(chat_id=chat_id, text=message, reply_to_message_id=msg_id)

        elif text == '/impressum':
            message = '''
            Dieser Chatbot wird von der Frick & Funke technologies GbR zu einem nicht kommerziellen Zweck betrieben.\n
            Die Inhalte stammen unverändert von den Webseiten tagesschau.de und dem Projekt covid.ourworldindata.org\n
            Für Kritik oder weitere Informationen wenden sie sich bitte an info@frifu.de
            '''
            self.bot.sendMessage(chat_id=chat_id, text=message, reply_to_message_id=msg_id)

        elif text == '/updateall':
            message = f'Alle {len(self.UNSORTEDtagesschau)}aktuellen Nachrichten:\n\n'
            i = 0
            while i < len(self.SORTEDtagesschau):
                message += f'{self.UNSORTEDtagesschau[i]["title"]}\n'
                message += f'Zum ganzen Artikel geht es hier: {self.UNSORTEDtagesschau[i]["link"]}\n\n'
                i += 1
            print('\n[DEBUG:message_parser_03] send message:\n::::::::\n' + message + '\n::::::::\n')
            self.bot.sendMessage(chat_id=chat_id, text=message, reply_to_message_id=msg_id)

        elif text == '/togglescheduler':
            user_togglescheduler = self.cache.get_user_togglescheduler(chat_id)
            if self.cache.store_user_togglescheduler(chat_id, user_togglescheduler):
                if user_togglescheduler == False:
                    message = 'Ihre auto-Nachrichten sind ab sofort abbestellt'
                else:
                    message = 'Ihre auto-Nachrichten sind ab sofort aktiviert'
                self.bot.send_message(chat_id=chat_id, text=message, reply_to_message_id=msg_id)
            else:
                message = 'Ein Fehler ist aufgetreten.'
                self.bot.send_message(chat_id=chat_id, text=message, reply_to_message_id=msg_id)
            print('\n[DEBUG:message_parser_04] send message:\n::::::::\n' + message + '\n::::::::\n')

        else:
            message = 'Falscher Befehl. Bitte auf Tippfehler achten.'
            self.bot.sendMessage(chat_id=chat_id, text=message, reply_to_message_id=msg_id)
            print('\n[DEBUG:message_parser_wrong_keyword] send message:\n::::::::\n' + message + '\n::::::::\n')


