
import json
import os
from datetime import datetime
from threading import Lock
from bs4 import BeautifulSoup 

class FileStorage:
    def __init__(self, directory="crawler_data"):
        self.directory = directory
        self.lock = Lock()
        self.results = []
        
        # Create directory if it doesn't exist
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        self.connected = True
        self.results_file = os.path.join(directory, f"results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        
    def isConnected(self):
        return self.connected
    
    def saveData(self, url, pageSource, keyword=''):
        try:
            title = ""
            summary = ""
            try:
                soup = BeautifulSoup(pageSource, 'html.parser')
                title_tag = soup.find('title')
                if title_tag:
                    title = title_tag.text.strip()
                
                # Get first para as summary
                first_p = soup.find('p')
                if first_p:
                    summary = first_p.text.strip()[:200] + "..." if len(first_p.text) > 200 else first_p.text.strip()
            except:
                pass
                
            keyword_found = keyword.lower() in pageSource.lower() if keyword else False
            
            page_data = {
                "url": url,
                "title": title,
                "summary": summary,
                "crawled_at": datetime.now().isoformat(),
                "keyword_found": keyword_found
            }
            
            # Saving full page source in a separate file
            page_file = os.path.join(self.directory, self._get_safe_filename(url) + ".html")
            with open(page_file, 'w', encoding='utf-8') as f:
                f.write(pageSource)
            
            # Add to in-memory results
            with self.lock:
                self.results.append(page_data)
                
                # Periodically save results to avoid data loss
                if len(self.results) % 10 == 0:
                    self._save_results_to_file()
                    
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False
    
    def _save_results_to_file(self):
        try:
            with open(self.results_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "crawl_date": datetime.now().isoformat(),
                    "total_pages": len(self.results),
                    "pages": self.results
                }, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving results to file: {e}")
            return False
    
    def _get_safe_filename(self, url):

        filename = url.replace('http://', '').replace('https://', '').replace('/', '_').replace(':', '_')

        if len(filename) > 100:
            filename = filename[:100]
        return filename
    
    def close(self):
        if self.connected:
            self._save_results_to_file()
            self.connected = False
            print(f"All results saved to {self.results_file}")
            print(f"Individual pages saved to {self.directory} directory")
