# import sys
# sys.path.append("C:/Users/Kenny/Documents/health_linebot_project/health_linebot/health_assessment")
from health_assessment.assessment import health_assessment
from linebot.models import *

class eat(health_assessment):
    
    def __init__(self,user_id):
        health_assessment.__init__(self,user_id=user_id)
        self.gender = self.profile[2]
        self.age = self.profile[3]
        self.height = self.profile[4]
        self.weight = self.profile[5]
        self.activity_status = self.answer[7]
        
        self.eat_title = self.title[1:7]
        self.eat_answer = self.answer[1:7]
        self.eat_correct_answer = self.correct_answer[0:6]
        self.eat_respond = self.respond[0:6]
        
    def TDEE_Calculate(self)->float:
        #男性：TDEE = (10 × 体重kg) + (6.25 × 身高cm) - (5 × 年龄岁) + 5
        #女性：TDEE = (10 × 体重kg) + (6.25 × 身高cm) - (5 × 年龄岁) - 161
        TDEE = 10 * self.weight + 6.25 * self.height
        if self.gender == "male":
            TDEE -= (5 * self.age) + 5
        else:
            TDEE -= (5 * self.age) - 161
            
        match self.activity_status:
            case "活動趨於靜態（久坐、躺著不出門）":
                TDEE *= 1.2
            case "活動程度較低（開車、烹飪、散步）":
                TDEE *= 1.375
            case "活動程度正常（做家務、逛街、健走）":
                TDEE *= 1.55
            case "活動程度較高（打球、騎腳踏車、有氧運動）":
                TDEE *= 1.72
            case "活動程度激烈（運動訓練、運動競賽）":
                TDEE *= 1.9
                
        return round(TDEE,2)
    
    # D.飲食建議
    def eat_template(self)->TemplateSendMessage:
        eat_incorrect_answer = self.handle_incorrect_answer(user_answer=self.eat_answer,correct_answer=self.eat_correct_answer)
        eat_incorrect_answer_index = self.handle_incorrect_answer_index(user_answer=self.eat_answer,correct_answer=self.eat_correct_answer)
        eat_incorrect_title = [self.correct_answer[i] for i in eat_incorrect_answer_index]
        message = TemplateSendMessage(
            alt_text='搜尋健身房功能的使用說明',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url="https://imgur.com/dxHQuNH.jpg",
                        title = f"題目:{eat_incorrect_title[i]}\n您的回答:{eat_incorrect_answer[i]}",
                        text=self.eat_respond[i],
                        actions=[
                            PostbackTemplateAction(
                                label=' ',
                                data='do_nothing'
                            )
                        ]
                    )for i in range(len(eat_incorrect_title))
                ]
            )
        )
        return message