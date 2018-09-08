import os, sqlite3

class databaseConnection:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.path = os.path.abspath("/home/pi/workspace/sql/cpu.db")

    def insert(self, temperature, humidity):
        try:
            conn = sqlite3.connect(self.path)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO temps(temperature, humidity) VALUES((?),(?))", (temperature, humidity))
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.commit()
            conn.close()
    
    def connect(self):
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        return conn,cursor
    
    def closeConnection(self, cursor, conn):
        cursor.close()
        conn.commit()
        conn.close()

if __name__  == "__main__":
    db = databaseConnection()
    db.insert(20, 95)