import pymysql
import dbconfig

import datetime

class DBHelper(object):

    def connect(self, database="crimemap"):
        return pymysql.connect(host='localhost',
                               user=dbconfig.db_user,
                               passwd=dbconfig.db_passwd,
                               db=database)

    # def get_all_inputs(self):
    #     connection = self.connect()
    #     try:
    #         query = """
    #         SELECT description 
    #         FROM crimes;
    #         """
    #         with connection.cursor() as cursor:
    #             cursor.execute(query)
    #         return cursor.fetchall()
    #     finally:
    #         connection.close()

    # def add_input(self, data):
    #     connection = self.connect()

    #     try:
    #         query = """
    #         INSERT INTO crimes (description) VALUES (%s);
    #         """
    #         with connection.cursor() as cursor:
    #             cursor.execute(query, data)
    #             connection.commit()
    #     finally:
    #         connection.close()

    # def clear_all(self):
    #     connection = self.connect()
    #     try:
    #         query = "DELETE FROM crimes;"
    #         with connection.cursor() as cursor:
    #             cursor.execute(query)
    #             connection.commit()
    #     finally:
    #         connection.close()

    def add_crime(self, category, date, latitude, longitude, description):
        connection = self.connect()
        try:
            query = """
            INSERT INTO crimes (category, date, latitude, longitude, description) \
            VALUES (%s, %s, %s, %s, %s)
            """
            with connection.cursor() as cursor:
                cursor.execute(query, (category, date, latitude, longitude, description))
                connection.commit()
        except Exception as e:
            print(e)
        finally:
            connection.close()

    def get_all_crimes(self):
        connection = self.connect()
        crimes = list()

        try:
            query = """
            SELECT latitude, longitude, date, category, description
            FROM crimes;
            """
            with connection.cursor() as cursor:
                cursor.execute(query)

            for crime in cursor:
                crime_dict = {'latitude': crime[0], 
                              'longitude': crime[1], 
                              'date': datetime.datetime.strftime(crime[2], '%Y-%m-%d'), 
                              'category': crime[3], 
                              'description': crime[4]}
                crimes.append(crime_dict)
            return crimes

        except Exception as e:
            print(e)
        finally:
            connection.close()

