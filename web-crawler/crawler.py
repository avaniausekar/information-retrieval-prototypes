from collections import deque
from bs4 import BeautifulSoup 
import time
from urllib.parse import urljoin, urlparse

from web_page import WebPage
from threadPool import ThreadPool
from threading import Lock
from fileStorage import FileStorage

class Crawler(object):
    def __init__(self):
        self.depth = 3  
        self.currentDepth = 1  
        self.keyword = "crawl"
        self.visitedUrls = set()   
        self.unvisitedUrls = deque()
        self.url = "https://simplescraper.io/docs/crawling-lists-of-urls"
        self.unvisitedUrls.append(self.url)
        self.isCrawling = False
        self.database = FileStorage()
        self.threadPool = ThreadPool(10)
        self.lock = Lock()

    def start(self):
        print("Crawling started")
        if not self.isDbConnected():
            print("Unable to initialize storage.")
        else:
            self.isCrawling = True
            self.threadPool.startThreads() 
            while self.currentDepth <= self.depth:
                self._assignCurrentDepthTasks()
                # Wait until all tasks at current depth are done
                while self.threadPool.getTaskLeft():
                    time.sleep(1)
                print(f"Depth {self.currentDepth} Finish. Total visited {len(self.visitedUrls)} links.")
                self.currentDepth += 1
            self.stop()

    def stop(self):
        self.isCrawling = False
        self.threadPool.stopThreads()
        self.database.close()
        print("Crawling completed")

    def getVisitedUrls(self):
        return len(self.visitedUrls) - self.threadPool.getTaskLeft()

    def _assignCurrentDepthTasks(self):
        urls_at_current_depth = len(self.unvisitedUrls)
        for _ in range(urls_at_current_depth):
            if not self.unvisitedUrls:
                break
                
            url = self.unvisitedUrls.popleft()
            
            # Skip if URL is already visited
            with self.lock:
                if url in self.visitedUrls:
                    continue
                self.visitedUrls.add(url)
            
            # Add task to thread pool
            self.threadPool.putTask(self.taskHandler, url)
            
    def taskHandler(self, url):
        webPage = WebPage(url)
        if webPage.fetch():
            self.saveTaskResults(webPage)
            self.addUnvisitedUrls(webPage)
            
    def saveTaskResults(self, webPage):
        url, pageSource = webPage.getData()
        try:
            # Check if the keyword exists in the page source
            if not self.keyword or self.keyword.lower() in pageSource.lower():
                success = self.database.saveData(url, pageSource, self.keyword)
                if success:
                    print(f"Saved page: {url}")
                else:
                    print(f"Failed to save page: {url}")
        except Exception as e:
            print(f"Error saving {url}: {e}")

    def addUnvisitedUrls(self, webPage):
        url, pageSource = webPage.getData()
        urls = self.getAllUrls(url, pageSource)

        for href in urls:
            with self.lock:  # Thread safety for shared collections
                if not self.isUrlRepeated(href):
                    self.unvisitedUrls.append(href)
    
    def isDbConnected(self):
        if self.database.isConnected():
            return True
        return False
    
    def isUrlRepeated(self, href):
        if href in self.visitedUrls:
            return True
        
        # Need to check if URL is in the unvisitedUrls queue
        # This is inefficient - HOW TO MAKE MORE EFFICIENT ?????????????
        for url in self.unvisitedUrls:
            if url == href:
                return True
        return False
    
    def getAllUrls(self, url, pageSource):
        urls = [] 
        try:
            soup = BeautifulSoup(pageSource, 'html.parser')
            results = soup.find_all('a', href=True)
            for a in results:
                href = a['href']
                if not href.startswith('http'):
                    href = urljoin(url, href)
                
                # Filter out invalid URLs
                parsed = urlparse(href)
                if parsed.scheme in ('http', 'https'):
                    urls.append(href)
        except Exception as e:
            print(f"Error parsing URLs from {url}: {e}")
            
        return urls

if __name__ == "__main__":
    crawler = Crawler()
    crawler.start()