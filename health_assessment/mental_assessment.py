# import sys
# sys.path.append("C:/Users/Kenny/Documents/health_linebot_project/health_linebot/health_assessment")
from health_assessment.assessment import health_assessment
from linebot.models import *

class mental(health_assessment):
    def __init__(self,user_id):
        super().__init__(user_id)
        
        self.mental_title = self.title[13:]
        self.mental_answer = self.answer[13:]
        self.mental_correct_answer = [[4,5] for i in range(5)]
        self.mental_respond = self.respond[12:]
        self.mental_incorrect_answer = self.handle_incorrect_answer(user_answer=self.mental_answer,correct_answer=self.mental_correct_answer)
        self.mental_incorrect_answer_index = self.handle_incorrect_answer_index(user_answer=self.mental_answer,correct_answer=self.mental_correct_answer)
        self.mental_incorrect_title = [self.mental_title[i] for i in self.mental_incorrect_answer_index]
        
    # E.心理健康建議
    def mental_template(self):
        message = TemplateSendMessage(
            alt_text='心理健康建議',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url="https://raw.githubusercontent.com/hung-0621/health_linebot/get_user_data/images/mental_image.jpg",
                        title = f"題目:{self.mental_incorrect_title[i]}\n您的回答:程度{self.mental_incorrect_answer[i]}",
                        text=self.mental_respond[i],
                        actions=[
                            PostbackTemplateAction(
                                label=' ',
                                data='do_nothing'
                            )
                        ]
                    )for i in range(len(self.mental_incorrect_title))
                ]
            )
        )
        return message
                