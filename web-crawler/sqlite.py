import sqlite3

class Database:
    def __init__(self, dbFile):
        try:
            self.conn = sqlite3.connect(dbFile)
            self.conn.execute(
                "CREATE TABLE IF NOT EXISTS Webpage (id INTEGER PRIMARY KEY AUTOINCREMENT, url TEXT, pageSource TEXT, keyword TEXT)")
        except Exception:
            self.conn = None

    def isConnected(self):
        if self.conn:
            return True
        else:
            return False
    
    def close(self):
        if self.conn:
            self.conn.close()
        else :
            raise sqlite3.OperationalError('Database is not connected.')
        
    def saveData(self, url, pageSource, keyword=''):
        if self.conn:
            query='''INSERT INTO Webpage (url, pageSource, keyword) VALUES (?, ?, ?);'''
            self.conn.execute(query, (url, pageSource, keyword) )
        else :
            raise sqlite3.OperationalError('Database is not connected. Can not save Data!')


