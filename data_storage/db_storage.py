# data_storage/db_storage.py
import sqlite3
import json
from .i_data_storage import IDataStorage


class DBStorage(IDataStorage):
    @staticmethod
    def get_db_connection():
      conn = sqlite3.connect("dataBaseTomas.db")
      conn.row_factory = sqlite3.Row
      return conn

    def get_fb_by_number(self, data):
      conn = self.get_db_connection()
      query = conn.execute(f'SELECT resultFb FROM fizzBuzz WHERE number = {data}').fetchone()
      conn.close()
      return query
    
    def get_activate_fb(self, data):
       conn = self.get_db_connection()
       cursor = conn.cursor()
       result = cursor.execute("SELECT number, resultFb FROM FizzBuzz WHERE number = ? AND active = '1'", (data,)).fetchone()
       conn.close()
       return result
    
    def post_fb(self,data):
      conn = self.get_db_connection()
      query = f"INSERT INTO fizzBuzz (number, resultFb) VALUES ('{data.get('number')}','{data.get('result')}')"
      conn.execute(query)
      conn.commit()
      conn.close()

    def update_inactive_data(self, data):
       conn = self.get_db_connection()
       cursor = conn.cursor()
       cursor.execute("UPDATE fizzBuzz SET active = '1' WHERE number = ?", (data,))
       conn.commit()
       conn.close()
    
    def get_range(self, lower_limit, upper_limit):
      conn = self.get_db_connection()
      cursor = conn.cursor()
      result = conn.execute("SELECT * FROM fizzBuzz WHERE number BETWEEN ? AND ? AND active = '1'", (lower_limit, upper_limit)).fetchall()
      conn.close()
      return result
    
    def delete_fb(self, data):
       conn = self.get_db_connection()
       cursor = conn.cursor()
       cursor.execute("UPDATE fizzBuzz SET active = '0' WHERE number = ?", (data,))
       conn.commit()
       conn.close()
    
# Hard delete to be used by admin
    def get_number(self,data):
      conn = self.get_db_connection()
      query = conn.execute(f'SELECT number FROM fizzBuzz WHERE number = {data}').fetchone()
      conn.close()
      return query
       
       
    def hard_delete_fb(self,data):
       conn = self.get_db_connection()
       cursor = conn.cursor()
       cursor.execute("DELETE FROM fizzBuzz WHERE number = ?", (data,))
       conn.commit()
       conn.close()
       
    

       
  
