import requests

class WebPage:
    def __init__(self, url):
        self.url = url
        self.pageSource = None
        
    def fetch(self):
        try:
            response = requests.get(self.url, timeout=10)
            if response.status_code == 200:
                self.pageSource = response.text
                return True
            return False
        except Exception as e:
            print(f"Error fetching {self.url}: {e}")
            return False
    
    def getData(self):
        return self.url, self.pageSource