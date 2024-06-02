# import sys
# sys.path.append("C:/Users/Kenny/Documents/health_linebot_project/health_linebot/health_assessment")
from health_assessment.assessment import health_assessment
from linebot.models import *

class eat(health_assessment):
    
    def __init__(self,user_id):
        health_assessment.__init__(self,user_id)
        self.gender = str(self.profile[2])
        self.age = int(self.profile[3])
        self.height = float(self.profile[4])
        self.weight = float(self.profile[5])
        self.activity_status = str(self.answer[7])
        
        self.eat_title = self.title[1:7]
        self.eat_answer = self.answer[1:7]
        self.eat_correct_answer = self.correct_answer[0:6]
        self.eat_respond = self.respond[0:6]
        self.eat_incorrect_answer=[]
        #self.eat_incorrect_answer = self.handle_incorrect_answer(user_answer=self.eat_answer,correct_answer=self.eat_correct_answer)
        self.eat_incorrect_answer_index = self.handle_incorrect_answer_index(user_answer=self.eat_answer,correct_answer=self.eat_correct_answer)
        self.eat_incorrect_title = [self.eat_title[i] for i in self.eat_incorrect_answer_index]
        
    def BRM_Calculate(self)->float:
        #男性：TDEE = (10 × 体重kg) + (6.25 × 身高cm) - (5 × 年龄岁) + 5
        #女性：TDEE = (10 × 体重kg) + (6.25 × 身高cm) - (5 × 年龄岁) - 161
        BRM = 10 * self.weight + 6.25 * self.height
        if self.gender == "男性":
            BRM -= (5 * self.age) + 5
        else:
            BRM -= (5 * self.age) - 161
        return BRM
            
    def TDEE_Calculate(self)->float:
        BRM = self.BRM_Calculate()        
        match self.activity_status:
            case "活動趨於靜態（久坐、躺著不出門）":
                TDEE = BRM * 1.2
            case "活動程度較低（開車、烹飪、散步）":
                TDEE = BRM * 1.375
            case "活動程度正常（做家務、逛街、健走）":
                TDEE = BRM * 1.55
            case "活動程度較高（打球、騎腳踏車、有氧運動）":
                TDEE = BRM * 1.72
            case "活動程度激烈（運動訓練、運動競賽）":
                TDEE = BRM * 1.9
        return round(TDEE,2)
    
    def BMI_Calculate(self)->float:
        BMI = self.weight / (self.height/100)**2
        return round(BMI,2)
    
    def Body_fat_Calculate(self)->float:
        #體脂率 = 1.2 x BMI + 0.23 x 年齡 – 5.4 -10.8 x 性別（男生的值為 1，女生為 0）
        BMI = self.BMI_Calculate()
        if self.gender == "男性":
            Body_fat = 1.2 * BMI + 0.23 * self.age - 5.4 - 10.8
        else:
            Body_fat = 1.2 * BMI + 0.23 * self.age - 5.4
        return round(Body_fat,2)
    
    # 回傳身體數據
    def body_imformation(self)->CarouselColumn:
        message = CarouselColumn(
                    thumbnail_image_url="https://raw.githubusercontent.com/hung-0621/health_linebot/get_user_data/images/eat_image.jpg",
                    title = "您的相關身體數據：",
                    text='%-6s:%2.2f\n%-6s:%5.2f\n%s:%2.2f' % ("BMI",self.BMI_Calculate(),"TDEE",self.TDEE_Calculate(),"體脂率",self.Body_fat_Calculate()),
                    actions=[
                        PostbackTemplateAction(
                            label=' ',
                            data='do_nothing'
                        )
                    ]
                )
        return message
    # D.飲食建議
    def eat_template(self)->TemplateSendMessage:
        if self.eat_incorrect_answer == []:
            message = message = TemplateSendMessage(
                alt_text='飲食建議',
                template=CarouselTemplate(
                    columns=[
                        self.body_imformation(),
                        self.no_incorrect_answer_column(title="飲食",image_url="https://raw.githubusercontent.com/hung-0621/health_linebot/get_user_data/images/eat_image.jpg")
                    ]
                )
            )
        else:
            message = TemplateSendMessage(
                alt_text='飲食建議',
                template=CarouselTemplate(
                    columns=[
                        self.body_imformation(),
                        CarouselColumn(
                            thumbnail_image_url="https://raw.githubusercontent.com/hung-0621/health_linebot/get_user_data/images/eat_image.jpg",
                            title = f"題目:{self.eat_incorrect_title[i]}\n您的回答:{self.eat_incorrect_answer[i]}",
                            text = self.eat_respond[i],
                            actions=[
                                PostbackTemplateAction(
                                    label=' ',
                                    data='do_nothing'
                                )
                            ]
                        )for i in range(len(self.eat_incorrect_title))
                    ]
                )
            )
        return message