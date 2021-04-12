import requests
import datetime as dt
import json
from cache.cache_handler import api_parser_cache

class api_parser:

    def __init__(self, country=None):

        # set up global variables
        if not country:
            self.country = 'DEU'
        elif country.lower() == 'world':
            self.country = 'OWID_WRL'
        elif country.lower() == 'kos':
            self.country = 'OWID_KOS'
        else:
            self.country = country

        self.url = 'https://covid.ourworldindata.org/data/owid-covid-data.json'
        self.cache = api_parser_cache()
        
        if not self.cache.already_up_to_date:

            # read content from url, store in globvar, throw exception if necessary
            try:
                response = requests.get(url=self.url)
                print('[DEBUG:metadata_api_parser_01] api get request succesfull')
            except Exception as e:
                print(f'[DEBUG_ERROR:metadata_api_parser_01] occured while api request getting raw data:\n{e}\n')

            self.content = json.loads(response.content)
            self.metadata = self.content[self.country]['data']
        else:
            if self.cache.get_data():
                self.content = self.cache.get_data()
            else:
                # read content from url, store in globvar, throw exception if necessary
                try:
                    response = requests.get(url=self.url)
                    print('[DEBUG:metadata_api_parser_01.1] api get request succesfull')
                except Exception as e:
                    print(f'[DEBUG_ERROR:metadata_api_parser_01.1] occured while api request getting raw data:\n{e}\n')

                self.content = json.loads(response.content)
                self.cache.store_data(self.content)
                self.metadata = self.content[self.country]['data']
                

    def get_country_info(self):

        result = self.content[self.country]
        result.pop('data')
        country_info_result = []

        for category in result:
            print(category.replace('_', ' ') + ' :: ' + str(result[category]))
            country_info_result.append(category.replace('_', ' ') + ' :: ' + str(result[category]))

        return country_info_result

    def get_new_cases_from_date(self, date=None):

        # if date given, return new cases from date
        if date:
            for daily_entry in self.metadata:
                if daily_entry['date'] == date:
                    print(
                        'new cases from ' + daily_entry['date'].replace('-', '.') + ' in ' + self.country + ' :: ' + str(daily_entry['new_cases']))
                    return str(daily_entry['new_cases'])

        # if no date given, return new cases from most current date
        if not date:
            today = dt.date.today()
            yesterday = today - dt.timedelta(days=1)
            yesterday = str(yesterday)

            for daily_entry in self.metadata:
                if daily_entry['date'] == yesterday:
                    print(
                        'new cases from ' + daily_entry['date'].replace('-', '.') + ' in ' + self.country + ' :: ' + str(daily_entry['new_cases']))
                    return str(daily_entry['new_cases'])

    def get_by_key_and_date(self, key, date=None):
        '''
        possible keys:
        "total_cases",
        "new_cases",
        "new_cases_smoothed",
        "total_deaths",
        "new_deaths",
        "new_deaths_smoothed",
        "total_cases_per_million",
        "new_cases_per_million",
        "new_cases_smoothed_per_million",
        "total_deaths_per_million",
        "new_deaths_per_million",
        "new_deaths_smoothed_per_million" 
        '''
        try:
            # if date given, return new cases from date
            if date:
                for daily_entry in self.metadata:
                    if daily_entry['date'] == date:
                        print(str(key) + ' from ' +
                              daily_entry['date'].replace('-', '.') + ' in ' + self.country + ' :: ' + str(daily_entry[key]))
                        return str(daily_entry[key])
                print('[DEBUG:api_parser_01] No entry with matching date found.')
                return False

            # if no date given, return new cases from most current date
            if not date:
                today = dt.date.today()
                yesterday = today - dt.timedelta(days=1)
                yesterday = str(yesterday)
                twodaysago = today - dt.timedelta(days=2)
                twodaysago = str(twodaysago)

                for daily_entry in self.metadata:
                    if daily_entry['date'] == yesterday:
                        print('[DEBUG:api_parser_01]' + str(key) + ' from ' +
                              daily_entry['date'].replace('-', '.') + ' in ' + self.country + ' :: ' + str(daily_entry[key]))
                        if daily_entry:
                            return str(daily_entry[key])
                
                for daily_entry in self.metadata:
                    if daily_entry['date'] == twodaysago:
                        print('[DEBUG:api_parser_01]' + str(key) + ' from ' +
                              daily_entry['date'].replace('-', '.') + ' in ' + self.country + ' :: ' + str(daily_entry[key]))
                        if daily_entry:
                            print('[DEBUG_ERROR_SOFT:api_parser_01] No entry for yesterday found, returned the entry from two days ago instead.')
                            return str(daily_entry[key])


        except KeyError as e:
            possible_keys = [
                "total_cases",
                "new_cases",
                "new_cases_smoothed",
                "total_deaths",
                "new_deaths",
                "new_deaths_smoothed",
                "total_cases_per_million",
                "new_cases_per_million",
                "new_cases_smoothed_per_million",
                "total_deaths_per_million",
                "new_deaths_per_million",
                "new_deaths_smoothed_per_million"
            ]

            # TODO: Add appropriate return types to following errors, no print() statement
            for i in possible_keys:
                if i == key:
                    print(
                        f'[ERROR] No entry found with given key and date. Try a later Date.')
                    return False
                elif i != key:
                    print(f'[ERROR] key not valid:\n{e}\n')
                    return False

    def get_possible_countries(self):

        countries = []

        for country in self.content:
            if country != 'OWID_WRL':
                if country != 'OWID_KOS':
                    print(country)
                    countries.append(country)
                else:
                    print('KOS')
                    countries.append('KOS')


        return countries

    def return_possible_keys(self):
        possible_keys = [
            "total_cases",
            "new_cases",
            "new_cases_smoothed",
            "total_deaths",
            "new_deaths",
            "new_deaths_smoothed",
            "total_cases_per_million",
            "new_cases_per_million",
            "new_cases_smoothed_per_million",
            "total_deaths_per_million",
            "new_deaths_per_million",
            "new_deaths_smoothed_per_million"
        ]

        for i in possible_keys:
            print(i)

        return possible_keys