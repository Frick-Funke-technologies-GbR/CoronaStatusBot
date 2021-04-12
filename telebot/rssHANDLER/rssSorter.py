import json
import os

class rssSorter:
    def __init__(self):
        self.fileDirectory = os.path.dirname(os.path.abspath(__file__)) # absolute directory in which the program is placed in. (it is neccesary because of dumb linux)
        self.cacheDirectory = os.path.join(os.path.dirname(os.path.dirname(self.fileDirectory)), "cache")
        with open(os.path.join(self.cacheDirectory, "UNSORTEDtagesschau-articles.json"), "r") as feed:
            self.unfilteredDict = json.load(feed)

        with open(os.path.join(os.path.dirname(self.fileDirectory), "settings.json"), "r") as settings_file:
            self.settings = json.load(settings_file) # is a dictionary!!!

        self.keywords = self.settings["rssGRABBER"]["filter"]["keywords"] # the list with the keywords
        self.filteredDict = []

        



    def test(self):
        print(type(self.unfilteredDict[0]["description"]))
        print(type(self.keywords))
        for word in self.keywords:
            print(word)

    def sorter(self):
        for i in self.unfilteredDict: # iterate over all entries
            if any(word in i["description"] for word in self.keywords):
                self.filteredDict.append(i)
                
                
    def save_function(self): # saves the collected data to cache/SORTEDtagesschau-articles.json
            with open(os.path.join(self.cacheDirectory, "SORTEDtagesschau-articles.json"), "w+") as outfile:
                json.dump(self.filteredDict, outfile)

    def dialog(self):
        print("[DEBUG rssSorter] There are " + str(len(self.filteredDict)) + " articles with content about corona.")

    def main(self):
        try:
            print("Started sorting")
            self.sorter()
            self.save_function()
            self.dialog()
            print("Finished sorting!!!")
        except Exception as e:
            print(e)
            print(self.test())
            print("[ERROR rssSorter] An error occured while sorting the data. Look at the data above!")
