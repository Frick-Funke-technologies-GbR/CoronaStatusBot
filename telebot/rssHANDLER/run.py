# This program is used to activate the rssGRABBER and rssSorter.

from telebot.rssHANDLER.rssGRABBER import rssGRABBER
from telebot.rssHANDLER.rssSorter import rssSorter
from telebot.rssHANDLER.logger import logger

class rssParser():
    def go(self):
        rssGRABBER().main()
        print("")
        rssSorter().main()
        print("")
        print("")
        print("")
        print("[DEBUG rssHANDLER] We sucessfully got everything we wanted to download!!!")
        print('"Ein hoch auf die Wissenschaft!"')
        logger()
if __name__ == "__main__":
    rssParser().go()