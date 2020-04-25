
import pymysql



class UiContentClass(object):


    def getAllItemFromDatabase(self,):

        db = pymysql.connect("127.0.0.1", "root", "password", "finalyearproject")
        cursor = db.cursor()

        sqlSearch = ("SELECT ITEM_DESC FROM finalyearproject.`items details` ")

        cursor.execute(sqlSearch)


        return cursor.fetchall()
