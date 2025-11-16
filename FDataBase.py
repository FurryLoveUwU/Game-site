
import sqlite3
from flask import url_for


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()
    



    def register_user(self, username, password, email):

        check_part1 = True
        check_part2 = True



        # ПРОВЕРКА 1 - ЮЗЕРНЕЙМ
        self.__cur.execute("SELECT COUNT() as count FROM users WHERE username = ?", (username,))
        res = self.__cur.fetchone()
        if res['count'] > 0:
            check_part1 = False

        # ПРОВЕРКА 1 - ПОЧТА
        self.__cur.execute("SELECT COUNT() as count FROM users WHERE email = ?", (email,))
        res = self.__cur.fetchone()
        if res['count'] > 0:
            check_part2 = False



       

        if check_part1[0] == True and check_part2 == True:
            self.__cur.execute("INSERT INTO users VALUES(NULL, ?, ?, ?)", (username, password, email))
            self.__db.commit()

            return True
        else:
            return False
            
        

    