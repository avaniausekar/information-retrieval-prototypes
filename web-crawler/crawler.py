

from collections import deque
from locale import getdefaultlocale

from bs4 import BeautifulSoup 

# TODO saving in db, thread pools

class Crawler(object):

    def __init__(self, args):
        self.depth = args.depth  
        self.currentDepth = 1  
        self.keyword = args.keyword.decode(getdefaultlocale()[1]) 
        self.visitedUrls = set()   
        self.unvisitedUrls = deque()    
        self.unvisitedUrls.append(args.url) 
        self.isCrawling = False

    def start(self):
        pass

    def stop(self):
        self.isCrawling = False

    def getVisitedUrls(self):
        return 

    def assignDepthTasks(self):
        pass

    def _addUnvisitedUrls(self, webPage):
        pass

    def getAllUrls(self, url, pageSource):
        urls = [] 
        return urls
