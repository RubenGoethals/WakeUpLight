import mysql.connector

class DbClass:
    def __init__(self):
        import mysql.connector as connector
        # import MySQLdb as mdb

        self.__dsn = {
            "host": "localhost",
            "user": "root",
            "passwd": "mariaRub",
            "db": "easywakeup"
        }

        self.__connection = connector.connect(**self.__dsn)
        
    def get_light(self):
        # Query zonder parameters
        sqlQuery = "SELECT * FROM ledstrip WHERE ledstrip_id = 1"
        self.__connection.reset_session()
        cursor = self.__connection.cursor()
        cursor.execute(sqlQuery)
        result = cursor.fetchall()
        ledstrip=result
        cursor.close()
        return ledstrip
    
    def get_wakeup(self):
        # Query zonder parameters
        sqlQuery = "SELECT * FROM wakeup WHERE wakeup_id = 1"
        self.__connection.reset_session()
        cursor = self.__connection.cursor()
        cursor.execute(sqlQuery)
        result = cursor.fetchall()
        wakeup=result
        cursor.close()
        return wakeup
    
    def get_music(self):
        # Query zonder parameters
        sqlQuery = "SELECT * FROM music WHERE music_id = 1"
        self.__connection.reset_session()
        cursor = self.__connection.cursor()
        cursor.execute(sqlQuery)
        result = cursor.fetchall()
        music=result
        cursor.close()
        return music
    
    def set_light(self, state):
        # Query zonder parameters
        sqlQuery = "UPDATE ledstrip SET ledstrip_state='"+state+"'"
        self.__connection.reset_session()
        cursor = self.__connection.cursor()
        cursor.execute(sqlQuery)
        self.__connection.commit()
        print("SQL uitgevoerd")
        cursor.close()
        return None
    
    
    
    
    