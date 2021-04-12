# This is a program, which gets Status-Updates from News-Websites about the Corona-Virus

import json
import os

# For timing the function
import time

import feedparser  # for downloading the link of the videopodcast
import requests  # for http request

# for processing the http-anwser to xml:
from bs4 import BeautifulSoup


class rssGRABBER:
    def __init__(self):  # initiate
        self.fileDirectory = os.path.dirname(
            os.path.abspath(__file__)
        )  # absolute directory in which the program is placed in. (it is neccesary because of dumb linux)
        self.cacheDirectory = os.path.join(
            os.path.dirname(os.path.dirname(self.fileDirectory)), "cache"
        )
        with open(
            os.path.join(os.path.dirname(self.fileDirectory), "settings.json"), "r"
        ) as settings_file:
            self.settings = json.load(settings_file)  # is a dictionary!!!
        self.article_list = []
        self.error_occurred = False
        self.RSSvideoData = {}

    # scrape Data from site:
    def newsFEED_rss(self):

        FeedLink = self.settings["rssGRABBER"]["sources"]["websites"][
            "tagesschau-Newsfeed"
        ]  # the URLs of the websites to grab from
        request = requests.get(FeedLink)  # this is the request
        request_content = request.content
        soup = BeautifulSoup(
            request_content, features="lxml"
        )  # this is the raw XML Data

        def RSS_to_JSON_Feed(self, soup, request):
            articles = soup.findAll("item")

            for a in articles:
                title = a.find(
                    "title"
                ).text  # this are the keywords to find in the xml file
                link = a.find("guid").text
                published = a.find("pubdate").text
                description = a.find("description").text
                # image = a.find('img') # not able to use images yet

                # convert the data to JSON
                bericht = {  # one article
                    "title": title,  # at the front are the names as which they are being saved as
                    "link": link,
                    "published": published,
                    "description": description,
                    #'image': image,
                }
                self.article_list.append(bericht)  # finished JSON-Data

        def testing_Feed(self, request, soup):
            # keep switched off:
            print(soup)  # To test if there is any XML Data!!!
            print(self.settings)  # test if there is any Data in the settingsfile and w
            print(
                "above is the XML-Data. It is simultaniously put into the file: XMLdata[RSS2].html"
            )
            print(request.status_code)  # status of the http request - should be 200
            print(
                request.headers["content-type"]
            )  # which type of data is transmitted? - should be XML
            print(request.encoding)  # which encoding is used? - should be none
            f = open(
                os.path.join(self.fileDirectory, "cache", "XMLdata[RSS2].html"), "w+"
            )
            f.write(str(soup))
            f.close()

        try:
            RSS_to_JSON_Feed(self, soup, request)

        except Exception as e:
            testing_Feed(
                self, request, soup
            )  # only to test the http requests functionality
            print(e)
            print(
                "[ERROR rssGRABBER] An error has occurred while downloading the "
                + "\033[1;\033[4m"
                + "Newsfeed"
                + "\033[0m"
                + "!!! Look at the data above."
            )
            global error_occurred  # load the global variable
            error_occurred = True  # is used to determine, wheather there is a error

    def testing_Video(self, request, soup):
        # keep switched off:
        print(soup)  # To test if there is any XML Data!!!
        print(self.settings)  # test if there is any Data in the settingsfile and w
        print(
            "above is the XML-Data. It is simultaniously put into the file: XMLDataForVideopodcast.html"
        )
        print(request.status_code)  # status of the http request - should be 200
        print(
            request.headers["content-type"]
        )  # which type of data is transmitted? - should be XML
        print(request.encoding)  # which encoding is used? - should be none

    def newspodcast(self):
        request = ""
        soup = ""
        try:
            Tagesschau_video_site = self.settings["rssGRABBER"]["sources"]["websites"][
                "VideoPodcast"
            ].values()  # the URL of the websites to grab from
            for value in Tagesschau_video_site:
                RSSSendung = []
                request = requests.get(value)  # this is the request
                request_content = request.content
                soup = BeautifulSoup(
                    request_content, features="lxml"
                )  # this is the raw XML Data
                d = feedparser.parse(value)
                data = soup.findAll("item")

                i = 0
                while i < len(data) and i < 5:

                    title = (
                        data[i].find("title").text
                    )  # this are the keywords to find in the xml file
                    link = data[i].find("guid").text
                    published = data[i].find("pubdate").text
                    description = data[i].find("description").text
                    # image = a.find('img') # not able to use images yet
                    e = d.entries[i]
                    enclosure = e.enclosures[0]  # needs to stay 0

                    # convert the data to JSON
                    Podcastfolge = {  # one article
                        "title": title,  # at the front are the names as which they are being saved as
                        "link": link,
                        "published": published,
                        "description": description,
                        #'image': image,
                        "enclosure": enclosure,
                    }
                    RSSSendung.append(Podcastfolge)  # finished JSON-Data
                    i += 1
                self.RSSvideoData[value] = RSSSendung

        except Exception as e:
            self.testing_Video(request, soup)
            print(e)
            print(
                "[ERROR rssGRABBER - Video] An error has occurred while downloading the "
                + "\033[1;\033[4m"
                + "Link for the Videopodcast"
                + "\033[0m"
                + "!!! Look at the data above."
            )
            self.error_occurred = (
                True  # is used to determine, wheather there is a error
            )

            f = open(
                os.path.join(self.cacheDirectory, "XMLDataForVideopodcast.html"), "w+"
            )
            f.write(str(soup))
            f.close()

    def save_function(
        self,
    ):  # saves the collected data to cache/UNSORTEDtagesschau-articles.json
        with open(
            os.path.join(self.cacheDirectory, "UNSORTEDtagesschau-articles.json"), "w+"
        ) as outfile:
            json.dump(self.article_list, outfile)
        with open(
            os.path.join(self.cacheDirectory, "tagesschauVideoPodcastLink.json"), "w+"
        ) as outfile:
            json.dump(self.RSSvideoData, outfile)

    def dialog(self):

        if len(self.article_list) == 39:
            print("[DEBUG rssGRABBER - feed] As always there are 39 articles.")
        else:
            print(
                "[DEBUG rssGRABBER - feed] For some reason there are "
                + str(len(self.article_list))
                + " articles and not 39 as usual..."
            )

    def main(self):
        print("Started scraping")
        self.article_list = (
            []
        )  # reset article_list otherwise it will become longer and longer
        self.newspodcast()
        self.newsFEED_rss()
        self.save_function()
        self.dialog()
        print("Finished scraping")
