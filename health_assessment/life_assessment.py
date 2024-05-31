# import sys
# sys.path.append("C:/Users/Kenny/Documents/health_linebot_project/health_linebot/health_assessment")
from health_assessment.assessment import health_assessment
from linebot.models import *

class life(health_assessment):
    def __init__(self, user_id: str):
        super().__init__(user_id)
        