from datetime import datetime # for logfile
import os


class logger():
    cacheDirectory = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "cache", "rssHandlerLOG.txt")
    time = datetime.now().strftime("%d/%m/%y %H:%M:%S")
    
    if len(open(cacheDirectory, 'a+').readlines()) > 100: # if file gets to big its being reset.
        f = open(cacheDirectory, 'w+')
        log_file = f.read()
        log_file += ("\n --------------- \n" + time + '\nJust successfully downloaded and sorted. \n')    
        f.write(log_file)
        f.close()
    else:
        with open(cacheDirectory, 'a+') as log_file: # log to rssHandler.log
            log_file.write("\n --------------- \n" + time + '\nJust successfully downloaded and sorted. \n')    