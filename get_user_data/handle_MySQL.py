import gspread
import mysql.connector
import json
import hashlib
import os
from dotenv import load_dotenv # 本地開發時打開

# # load .env文件
load_dotenv() # 本地開發時打開

class handle_MySQL:
    def __init__(self):
        
        self.MYSQL_HOST = os.getenv('MYSQL_HOST')
        self.MYSQL_USER = os.getenv('MYSQL_USER')
        self.MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
        self.MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')
        self.MYSQL_PORT = os.getenv('MYSQL_PORT')
        self.GOOGLE_SHEET_URL = os.getenv('GOOGLE_SHEET_URL')
        
        # 連接到 Google Sheets
        # "C:/Users/Kenny/Downloads/global-phalanx-421818-9a75b24317ed.json"
        # "/etc/secrets/google_sheet_json_keyfile"
        self.gc = gspread.service_account(filename="C:/Users/Kenny/Downloads/global-phalanx-421818-9a75b24317ed.json")
    
    def connect_to_database(self):
        return mysql.connector.connect(
            host=self.MYSQL_HOST,
            user=self.MYSQL_USER,
            password=self.MYSQL_PASSWORD,
            database=self.MYSQL_DATABASE,
            port=self.MYSQL_PORT,
        )
    
    def hash_data(self, data):
        data_str = json.dumps(data, sort_keys=True)
        return hashlib.md5(data_str.encode()).hexdigest()
    
    def load_data(self):
        mydb = self.connect_to_database()
        mycursor = mydb.cursor()

        try:
            # 获取 profile 数据并插入或更新
            worksheet_profile = self.gc.open_by_url(self.GOOGLE_SHEET_URL).worksheet('profile')
            data_profile = worksheet_profile.get_all_records()

            for row in data_profile:
                user_id = row['用戶ID']
                username = row['用戶名稱']
                gender = row['性別']
                age = row['年齡']
                height = row['身高']
                weight = row['體重']
                sql_profile = """
                    INSERT INTO profile (用戶ID, 用戶名稱, 性別, 年齡, 身高, 體重)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE 用戶名稱=%s, 性別=%s, 年齡=%s, 身高=%s, 體重=%s
                """
                val_profile = (user_id, username, gender, age, height, weight, username, gender, age, height, weight)
                mycursor.execute(sql_profile, val_profile)

            mydb.commit()

            # 获取 answer 数据并插入或更新
            worksheet_answer = self.gc.open_by_url(self.GOOGLE_SHEET_URL).worksheet('answer')
            data_answer = worksheet_answer.get_all_records()

            for row in data_answer:
                user_id = row['用戶ID']
                mycursor.execute("SELECT 用戶ID FROM profile WHERE 用戶ID = %s", (user_id,))
                result = mycursor.fetchone()

                if result is None:
                    # 插入默认的 profile 数据
                    sql_profile = """
                        INSERT INTO profile (用戶ID, 用戶名稱, 性別, 年齡, 身高, 體重)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """
                    val_profile = (user_id, "default", "default", 0, 0.0, 0.0)
                    mycursor.execute(sql_profile, val_profile)

                sql_answer = """
                    INSERT INTO answer (用戶ID, 請問您一天中吃幾餐, 您是否有定期吃早餐的習慣, 您是否有喝足夠的水,
                        每日是否有吃至少一份水果, 一天中至少有一餐有一份蔬菜, 您一週平均吃幾次外食, 請問您每日的身體活動狀況,
                        您每週進行多少次體育活動, 您一次運動多久呢, 您在工作或學習中是否會每一到兩個小時起來活動一下呢,
                        每日平均睡眠時數, 每日平均行走步數, 您是否經常感到壓力大, 您是否經常感到焦慮,
                        您是否經常感到憂鬱、心情低落, 您是否經常睡眠不正常，例如難以入睡、易醒, 您是否經常有自殺的想法)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE 請問您一天中吃幾餐=%s, 您是否有定期吃早餐的習慣=%s, 您是否有喝足夠的水=%s,
                        每日是否有吃至少一份水果=%s, 一天中至少有一餐有一份蔬菜=%s, 您一週平均吃幾次外食=%s, 請問您每日的身體活動狀況=%s,
                        您每週進行多少次體育活動=%s, 您一次運動多久呢=%s, 您在工作或學習中是否會每一到兩個小時起來活動一下呢=%s,
                        每日平均睡眠時數=%s, 每日平均行走步數=%s, 您是否經常感到壓力大=%s, 您是否經常感到焦慮=%s,
                        您是否經常感到憂鬱、心情低落=%s, 您是否經常睡眠不正常，例如難以入睡、易醒=%s, 您是否經常有自殺的想法=%s
                """
                val_answer = (user_id, row['請問您一天中吃幾餐?'], row['您是否有定期吃早餐的習慣?'], row['您是否有喝足夠的水?  ( 體重一公斤需35毫升的水 )'],
                              row['每日是否有吃至少一份水果?'], row['一天中至少有一餐有一份蔬菜'], row['您一週平均吃幾次外食'], row['請問您每日的身體活動狀況？'],
                              row['您每週進行多少次體育活動？'], row['您一次運動多久呢?'], row['您在工作或學習中是否會每一到兩個小時起來活動一下呢?'],
                              row['每日平均睡眠時數'], row['每日平均行走步數'], row['您是否經常感到壓力大'], row['您是否經常感到焦慮'],
                              row['您是否經常感到憂鬱、心情低落'], row['您是否經常睡眠不正常，例如難以入睡、易醒'], row['您是否經常有自殺的想法'],
                              row['請問您一天中吃幾餐?'], row['您是否有定期吃早餐的習慣?'], row['您是否有喝足夠的水?  ( 體重一公斤需35毫升的水 )'],
                              row['每日是否有吃至少一份水果?'], row['一天中至少有一餐有一份蔬菜'], row['您一週平均吃幾次外食'], row['請問您每日的身體活動狀況？'],
                              row['您每週進行多少次體育活動？'], row['您一次運動多久呢?'], row['您在工作或學習中是否會每一到兩個小時起來活動一下呢?'],
                              row['每日平均睡眠時數'], row['每日平均行走步數'], row['您是否經常感到壓力大'], row['您是否經常感到焦慮'],
                              row['您是否經常感到憂鬱、心情低落'], row['您是否經常睡眠不正常，例如難以入睡、易醒'], row['您是否經常有自殺的想法'])
                mycursor.execute(sql_answer, val_answer)

            mydb.commit()
            print("Data Loaded and Updated!")

        except Exception as e:
            mydb.rollback()
            print(f"An error occurred: {e}")

        finally:
            mycursor.close()
            mydb.close()
            
    # 取得table資料
    def get_table_data(self,table_name:str)->tuple:
        mydb = self.connect_to_database()
        mycursor = mydb.cursor()

        try:
            # 查找table
            mycursor.execute(f"SELECT * FROM {table_name}")
            data = mycursor.fetchall()
            return data
                
        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            mycursor.close()
            mydb.close()
            
    # 取得user那列
    def get_user_id_row(self,table_data:tuple,user_id:str)->tuple:
        for row in table_data:
            try:
                if row[0]==user_id:
                    return row
            except:
                print("user not in table")
                
    # 原本的資料很醜，所以調整一下位置         
    def new_correct_answer(self,correct_answer:tuple)->list:
        new_correct_answer=[[answer] for answer in correct_answer[0]]
        for answer in correct_answer[1:]:
            for i in range(0,len(answer)):
                if answer[i]!=None:
                    new_correct_answer[i].append(answer[i])
        return new_correct_answer
    
    def get_column_data(self,table_name:str)->tuple:
        mydb = self.connect_to_database()
        mycursor = mydb.cursor()

        try:
            # 查找table
            mycursor.execute(f"SHOW COLUMNS FROM {table_name}")
            data = mycursor.fetchall()
            result=[]
            for i in range(len(data)):
                result.append(data[i][0])
            return result
        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            mycursor.close()
            mydb.close()