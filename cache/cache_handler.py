from datetime import datetime
import json
import os

class global_cache:

    def __init__(self):
        self.file_directory = os.path.dirname(os.path.abspath(__file__)) # absolute directory in which the program is placed in. (it is neccesary because of dumb linux)
        self.cache_directory = self.file_directory + '/cache.json'
        if not os.path.isfile(self.cache_directory):
            try:
                first_added_data = {}
                with open(self.cache_directory, 'w') as w:
                    json.dump(first_added_data, w)
                print(f'[DEBUG:global_cache] created cache dir sucessfully at: {self.cache_directory}')
            except OSError as e:
                print(f'[DEBUG_ERROR:global_cache] didn\'t create cache dir because of: {e}')

        # read whole cache data
        with open(self.cache_directory, 'r') as r:
            self.data = json.load(r)

        # check existance of chat_keyword tree, if false creates it
        if not 'chat_keywords' in self.data:
            self.data['chat_keywords'] = {} 
            with open(self.cache_directory, 'w') as w:
                json.dump(self.data, w)

        # check existance of chat tree, if false creates it
        if not 'chats' in self.data:
            self.data['chats'] = {} 
            with open(self.cache_directory, 'w') as w:
                json.dump(self.data, w)

        # check existance of an cache update
        if os.path.isfile(self.file_directory + '/update'):
            os.remove(self.file_directory + '/update')

            # ______IMPORTANT_______
            # TODO:  if added new chat keyword, first add CoronaStatus/cache/update (no file ending) and change the following None into Dict:  {'new-chat-keyword' : 'description please in german', ... } 
            new_chat_keywords = {'/updateall': 'Alle aktuellen Nachrichten unabhängig von Themen', '/togglescheduler':'Schaltet auto-Nachrichten an oder aus', "/help": "Info \u00fcber jedes verf\u00fcgbare Schl\u00fcsselwort", "/update": "Der aktuelle Stand der Infektionsdaten und -neuigkeiten von Tagesschau.de und ourworldindata.org"}

            if new_chat_keywords:
                for keyword in new_chat_keywords:
                    self.save_new_possible_chat_keyword(keyword, new_chat_keywords[keyword])
            else:
                print(f'[DEBUG_ERROR:global_cache_01] didn\'t find new_chat_keyword')

    def store_chat_id(self, chat_id):
        '''
        stores chat_id with empty message dictionary if not exists
        '''

        # check if chat_id already exists
        if chat_id in self.data['chats']:
            return False

        self.data['chats'][chat_id] = {'messages' : {}}

        with open(self.cache_directory, 'w') as w:
            json.dump(self.data, w)
            return True

    def store_chat_messages(self, chat_id, message):
        '''
        stores chat messages for certain chat_id with a timestamp.
        '''

        # check if chat_id exists  
        if not chat_id in self.data['chats']:
            return False

        timestamp = datetime.now().strftime("%d/%m/%Y_%H:%M:%S")
        self.data['chats'][chat_id]['messages'][timestamp] = message

        with open(self.cache_directory, 'w') as w:
            json.dump(self.data, w)
            return True

    def store_user_togglescheduler(self, chat_id, toggle=True):

        # check if chat_id exists  
        if not chat_id in self.data['chats']:
            return False

        self.data['chats'][chat_id]['togglescheduler'] = toggle

        with open(self.cache_directory, 'w') as w:
            json.dump(self.data, w)
            return True

    def get_user_togglescheduler(self, chat_id):

        # check if chat_id exists  
        if not chat_id in self.data['chats']:
            return False

        if not 'togglescheduler' in self.data['chats'][chat_id]:
            return False
        else:
            return bool(self.data['chats'][chat_id]['togglescheduler'])


    def get_chat_ids(self):
        '''
        returns all stored chat_ids
        '''

        chat_ids = []
        for chat_id in self.data['chats']:
            chat_ids.append(chat_id)

        return chat_ids

    def get_chat_messages(self, chat_id):
        '''
        returns all stored chat messageses from certain chat_id
        '''

        # check if chat_id already exists  
        if not chat_id in self.data['chats']:
            return False

        return self.data['chats'][chat_id]['messages']

    def get_possible_chat_keywords(self):
        '''
        returns all stored possible chat keywords
        '''

        keywords = {}

        for id in self.data['chat_keywords']:
            for keyword in self.data['chat_keywords'][id]:
                keywords[keyword] = self.data['chat_keywords'][id][keyword]

        return keywords

    # following function my only be necessary for debugging and one-time use for setting cache.json up in the server (only for use in e.g. testing file)
    def save_new_possible_chat_keyword(self, chat_keyword, description):
        '''
        stores new possible chat keyword
        '''

        # check if keyword already exists  
        if chat_keyword in self.data['chat_keywords']:
            return False

        count = 0

        for id in self.data['chat_keywords']:
            count += 1

        count += 1

        self.data['chat_keywords'][count] = {chat_keyword : description}

        with open(self.cache_directory, 'w') as w:
            json.dump(self.data, w)
            print(f'[DEBUG:global_cache_01] added new possible chat keyword with description: {chat_keyword}')
            return True

class api_parser_cache:

    def __init__(self):
        self.file_directory = os.path.dirname(os.path.abspath(__file__)) # absolute directory in which the program is placed in. (it is neccesary because of dumb linux)
        self.cache_directory = self.file_directory + '/cache_api_parser.json'
        self.cache_update_file_directory = self.file_directory + '/update_cache_api_parser.txt'
        if not os.path.isfile(self.cache_directory):
            try:
                first_added_data = {}
                with open(self.cache_directory, 'w') as w:
                    json.dump(first_added_data, w)
                print(f'[DEBUG:api_parser_chache_handler] created cache dir sucessfully at: {self.cache_directory}')
            except OSError as e:
                print(f'[DEBUG_ERROR:api_parser_chache_handler] didn\'t create cache dir because of: {e}')

        # read whole cache data
        with open(self.cache_directory, 'r') as r:
            self.data = json.load(r)

        # check last date cached
        self.already_up_to_date = None
        if os.path.isfile(self.cache_update_file_directory):
            with open(self.cache_update_file_directory, 'r') as r:
                if r.read() == datetime.now().strftime('%j'):
                    self.already_up_to_date = True
                else:
                    self.already_up_to_date = False

    def store_data(self, data, ignore_actuality=False):

        # check, if data is None so api_parser was not successful
        if not data:
            print(f'[DEBUG_ERROR:api_parser_chache_handler_01] couldn\'t create cache because of data being {data}')
            return False

        self.data = data
        day_of_year = datetime.now().strftime('%j')

        if not ignore_actuality:
            if not self.already_up_to_date:
                if self.already_up_to_date == None:
                    print(f'[DEBUG:api_parser_chache_handler_02] initialize cache system')
                with open(self.cache_directory, 'w') as w:
                    json.dump(self.data, w)
                    with open(self.cache_update_file_directory, 'w') as w:
                        w.write(str(day_of_year))
                        print(f'[DEBUG:api_parser_chache_handler_02] sucessfully parsed and cached api data for day {day_of_year} of the year')
                        return True
            else:
                print(f'[DEBUG_ERROR_SOFT:api_parser_chache_handler_02.1] did\'t parse and cache api data for day {day_of_year} of the year, data already cached')
        else:
            if self.already_up_to_date == None:
                print(f'[DEBUG:api_parser_chache_handler_02] initialize cache system')
            with open(self.cache_directory, 'w') as w:
                json.dump(self.data, w)
                with open(self.cache_update_file_directory, 'w') as w:
                    w.write(str(day_of_year))
                    print(f'[DEBUG:api_parser_chache_handler_02] sucessfully parsed and cached api data for day {day_of_year} of the year, ignoring the actualiy')
                    return True


    def get_data(self):

        # check, if cache is empty
        if self.data == {}:
            print(f'[DEBUG_ERROR:api_parser_chache_handler_03] cache is empty')
            return False

        return self.data
