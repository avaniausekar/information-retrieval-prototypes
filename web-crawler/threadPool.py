
from threading import Thread, Lock
from queue import Queue
import time
class ThreadPool:
    def __init__(self, num_threads):
        self.num_threads = num_threads
        self.task_queue = Queue()
        self.threads = []
        self.lock = Lock()
        self.running = False
        
    def worker(self):
        while self.running:
            try:
                if not self.task_queue.empty():
                    task_func, args = self.task_queue.get(block=False)
                    try:
                        task_func(*args)
                    except Exception as e:
                        print(f"Error executing task: {e}")
                    finally:
                        self.task_queue.task_done()
                else:
                    time.sleep(0.1)
            except Exception:
                time.sleep(0.1)
    
    def startThreads(self):
        self.running = True
        for _ in range(self.num_threads):
            thread = Thread(target=self.worker)
            thread.daemon = True
            thread.start()
            self.threads.append(thread)
    
    def stopThreads(self):
        self.running = False
        # Wait
        for thread in self.threads:
            thread.join(timeout=1.0)
        self.threads = []
    
    def putTask(self, func, *args):
        self.task_queue.put((func, args))
    
    def getTaskLeft(self):
        return self.task_queue.qsize()