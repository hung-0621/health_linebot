# import sys
# sys.path.append("C:/Users/Kenny/Documents/health_linebot_project/health_linebot/health_assessment")
from health_assessment.assessment import health_assessment
from linebot.models import *

class life(health_assessment):
    def __init__(self, user_id: str):
        super().__init__(user_id)
        self.life_title = self.title[7:12]
        self.life_answer = self.answer[7:12]
        self.life_correct_answer = self.correct_answer[6:11]
        self.life_respond = self.respond[6:11]