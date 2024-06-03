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
        
        self.eat_incorrect_answer = self.handle_incorrect_answer(user_answer=self.eat_answer,correct_answer=self.eat_correct_answer)
        self.eat_incorrect_answer_index = self.handle_incorrect_answer_index(user_answer=self.eat_answer,correct_answer=self.eat_correct_answer)
        self.eat_incorrect_title = [self.eat_title[i] for i in self.eat_incorrect_answer_index]
        print(self.eat_correct_answer)
        print(self.eat_incorrect_answer)
        print(self.eat_incorrect_answer_index)
        print(self.eat_incorrect_title)
        print(self.eat_respond[5])
        
    def BRM_Calculate(self)->float:
        # 男生=66+(13.7體重)+(5.0身高)-(6.8*年齡)
        # 女生=655+(9.6體重)+(1.8身高)-(4.7*年齡)

        if self.gender == "男性":
            BRM = 66 + (13.7 * self.weight) + (5.0 * self.height) - (6.8 * self.age)
        else:
            BRM = 655 + (9.6 * self.weight) + (1.8 * self.height) - (4.7 * self.age)
            
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
                    text = '%-6s:%2.2f\n%-6s:%5.2f\n%-s:%2.2f%s\n(數據可能因為計算公式不同而有變動)' % ("BMI",self.BMI_Calculate(),"TDEE",self.TDEE_Calculate(),"體脂率",self.Body_fat_Calculate(),chr(37)),
                    actions=[
                        URITemplateAction(
                            label='BMI相關文章',
                            uri='https://www.hpa.gov.tw/Search/GoogleSearch.aspx?queryString=BMI'
                        ),
                        URITemplateAction(
                            label="TDEE相關文章",
                            uri="https://ricky.tw/all/what-is-tdee/"
                        ),
                        URITemplateAction(
                            label="體脂率相關文章",
                            uri="https://tools.heho.com.tw/bodyfat/"
                        )
                    ]
                )
        return message
    # D.飲食建議
    def eat_template(self)->TemplateSendMessage:
        image_url = "https://raw.githubusercontent.com/hung-0621/health_linebot/get_user_data/images/eat_image.jpg"
        title = "飲食"
        if self.eat_incorrect_answer == []:
            message = TemplateSendMessage(
                alt_text='飲食建議',
                template=CarouselTemplate(
                    columns=[
                        self.body_imformation(),
                        self.no_incorrect_answer_column(
                            title="飲食",
                            image_url="https://raw.githubusercontent.com/hung-0621/health_linebot/get_user_data/images/eat_image.jpg",
                            actions=[
                                PostbackTemplateAction(
                                label=' ',
                                data='do_nothing'
                            ),
                            PostbackTemplateAction(
                                label=' ',
                                data='do_nothing'
                            ),
                            PostbackTemplateAction(
                                label=' ',
                                data='do_nothing'
                            )
                        ]
                    )
                ]
            )
        )
        else:
            incorrect_columns = [
                CarouselColumn(
                    thumbnail_image_url=image_url,
                    title = f"題目:{self.eat_incorrect_title[i]}\n您的回答:{self.eat_incorrect_answer[i]}",
                    text = self.eat_respond[self.eat_incorrect_answer_index[i]],
                    actions=[
                        PostbackTemplateAction(
                            label=' ',
                            data='do_nothing'
                        ),
                        PostbackTemplateAction(
                            label=' ',
                            data='do_nothing'
                        ),
                        PostbackTemplateAction(
                            label=' ',
                            data='do_nothing'
                        )
                    ]
                ) for i in range(len(self.eat_incorrect_title))
            ]
            incorrect_columns.insert(0,self.body_imformation())
            message = TemplateSendMessage(
                alt_text=f'{title}建議',
                template=CarouselTemplate(
                    columns=incorrect_columns
                )
            )
        return message