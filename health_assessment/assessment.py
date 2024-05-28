# import sys
# sys.path.append("/Users/Kenny/Documents/health_linebot_project/health_linebot")

from get_user_data.handle_MySQL import *

class health_assessment():
    
    #使用者answer index範圍
    def __init__(self,user_id:str):
        self.user_id = user_id
        self.profile = self.handle_user_data(table_name = "profile",user_id=self.user_id)
        self.answer = self.handle_user_data(table_name = "answer",user_id=self.user_id)
        self.correct_answer = self.handle_correct_answer()
        self.respond = handle_MySQL.get_table_data(table_name="respond")
        self.title = self.handle_column_data()
        
        self.life_answer = self.answer[7:12]
        self.mental_answer = self.answer[12:] 
    # 取得使用者訊息 profile, answer
    def handle_user_data(self,table_name:str,user_id:str)->tuple:
        data = handle_MySQL()
        # 取得使用者的answer資料
        table_data = data.get_table_data(table_name=table_name)
        user_data = data.get_user_id_row(table_data=table_data, user_id=user_id)
        return user_data
    
    # google sheet "answer" worksheet column name
    def handle_column_data()->tuple:
        data = handle_MySQL()
        column_data = data.get_column_data(table_name="answer")
        return column_data
    
    # 取得正確答案 correctanswer
    def handle_correct_answer()->list:
        data = handle_MySQL()
        # 取得正確答案的資料
        correct_answer = data.get_table_data(table_name="correctanswer")
        correct_answer = data.new_correct_answer(correct_answer)
        return correct_answer
    
    # 取得回答不正確的答案
    def handle_incorrect_answer(self,user_answer:tuple,correct_answer:list)->list:
        # 回答不正確的答案(i+1因為有user_id)
        return [user_answer[i] for i in range(len(correct_answer)) if user_answer[i] not in correct_answer[i]]
    
    # 取得不確答案在使用者answer的第幾項
    def handle_incorrect_answer_index(self,user_answer:tuple,correct_answer:list)->list:
        return [i for i in range(len(correct_answer)) if user_answer[i] not in correct_answer[i]]

    