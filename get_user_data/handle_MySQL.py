import gspread
import mysql.connector
import json
import hashlib
import time
import os
from get_user_data.handle_google_sheet import google_sheets

MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')
MYSQL_PORT = os.getenv('MYSQL_PORT')
GOOGLE_SHEET_URL = os.getenv('GOOGLE_SHEET_URL')
GOOGLE_SERVICE_ACCOUNT_FILE = os.getenv('GOOGLE_SERVICE_ACCOUNT_FILE')

# 連接到 MySQL 數據庫
mydb = mysql.connector.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DATABASE,
    port=MYSQL_PORT,
)
mycursor = mydb.cursor()

# get worksheet info 
data_profile = google_sheets.get_worksheet_info(sheet_name = "profile",worksheet_name = "健康評估")
data_answer = google_sheets.get_worksheet_info(sheet_name = "profile",worksheet_name = "健康評估")

# 連接到 Google Sheets
# gc = gspread.service_account(filename="C:/Users/taian/OneDrive/Desktop/global-phalanx-421818-9a75b24317ed.json")

# def hash_data(data):
#     data_str = json.dumps(data, sort_keys=True)
#     return hashlib.md5(data_str.encode()).hexdigest()

def londdata():
    # 獲取 profile 數據並插入或更新
    # worksheet_profile = gc.open_by_url(GOOGLE_SHEET_URL).worksheet('profile')
    # data_profile = worksheet_profile.get_all_records()

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

    # 提交事物，確保 profile 表的數據已經插入或更新
    mydb.commit()

    # 獲取 answer 數據並插入或更新
    # worksheet_answer = gc.open_by_url(GOOGLE_SHEET_URL).worksheet('answer')
    # data_answer = worksheet_answer.get_all_records()
    for row in data_answer:
        user_id = row['用戶ID']
        
        # 先檢查 profile 表中是否存在該用戶ID
        mycursor.execute("SELECT 用戶ID FROM profile WHERE 用戶ID = %s", (user_id,))
        result = mycursor.fetchone()
        
        # 如果 profile 表中不存在該用戶ID，則插入一條新數據
        if result is None:
            username = "default"  # 如果 profile 表中不存在該用戶ID，則用預設值填充
            gender = "default"
            age = 0
            height = 0.0
            weight = 0.0
            sql_profile = """
                INSERT INTO profile (用戶ID, 用戶名稱, 性別, 年齡, 身高, 體重)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            val_profile = (user_id, username, gender, age, height, weight)
            mycursor.execute(sql_profile, val_profile)
        
        # 準備 answer 表的插入或更新數據
        meals = row['請問您一天中吃幾餐?']
        breakfast_habit = row['您是否有定期吃早餐的習慣?']
        enough_water = row['您是否有喝足夠的水?  ( 體重一公斤需35毫升的水 )']
        fruits_daily = row['每日是否有吃至少一份水果?']
        veggies_daily = row['一天中至少有一餐有一份蔬菜']
        weekly_eating_out = row['您一週平均吃幾次外食']
        daily_activity = row['請問您每日的身體活動狀況？']
        weekly_exercise = row['您每週進行多少次體育活動？']
        exercise_duration = row['您一次運動多久呢?']
        move_every_hour = row['您在工作或學習中是否會每一到兩個小時起來活動一下呢?']
        daily_sleep_hours = row['每日平均睡眠時數']
        daily_steps = row['每日平均行走步數']
        stress_level = row['您是否經常感到壓力大']
        anxiety_level = row['您是否經常感到焦慮']
        depression_level = row['您是否經常感到憂鬱、心情低落']
        sleep_quality = row['您是否經常睡眠不正常，例如難以入睡、易醒']
        suicidal_thoughts = row['您是否經常有自殺的想法']
        
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
        val_answer = (user_id, meals, breakfast_habit, enough_water, fruits_daily, veggies_daily, weekly_eating_out,
            daily_activity, weekly_exercise, exercise_duration, move_every_hour, daily_sleep_hours,
            daily_steps, stress_level, anxiety_level, depression_level, sleep_quality, suicidal_thoughts,
            meals, breakfast_habit, enough_water, fruits_daily, veggies_daily, weekly_eating_out,
            daily_activity, weekly_exercise, exercise_duration, move_every_hour, daily_sleep_hours,
            daily_steps, stress_level, anxiety_level, depression_level, sleep_quality, suicidal_thoughts)
        mycursor.execute(sql_answer, val_answer)

    # 提交事物
    mydb.commit()
    print("Data Loaded and Updated!")

def getdata():
    # 重新加载数据到 MySQL 数据库
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="411631236",
        database="database",
        port="3306",
    )
    mycursor = mydb.cursor()

    # 查詢 profile 表數據
    mycursor.execute("SELECT * FROM profile")
    profile_data = mycursor.fetchall()
    print("Profile Data:")
    for row in profile_data:
        print(row)

    # 查詢 answer 表數據
    mycursor.execute("SELECT * FROM answer")
    answer_data = mycursor.fetchall()
    print("\nAnswer Data:")
    for row in answer_data:
        print(row)

    # 關閉游標和數據庫連接
    mycursor.close()
    mydb.close()
    
def monitor_updates():
    last_profile_hash = None
    last_answer_hash = None
    
    while True:
        current_profile_hash = hash_data(data_profile)
        current_answer_hash = hash_data(data_answer)
        
        if current_profile_hash != last_profile_hash:
            londdata()  # 如果 profile 數據有更新，重新加载數據到 MySQL 數據庫
            last_profile_hash = current_profile_hash
        
        if current_answer_hash != last_answer_hash:
            londdata()  # 如果 answer 數據有更新，重新加载數據到 MySQL 數據庫
            last_answer_hash = current_answer_hash
        
        time.sleep(60)  # 每 60 秒檢查一次數據是否有更新

# 調用監控函數
monitor_updates()