# import sys
# sys.path.append("C:/Users/Kenny/Documents/health_linebot_project/health_linebot/health_assessment")
from health_assessment.assessment import health_assessment
from linebot.models import *

class life(health_assessment):
    def __init__(self, user_id: str):
        super().__init__(user_id)
        self.life_title = self.title[7:13]
        self.life_answer = self.answer[7:13]
        self.life_correct_answer = self.correct_answer[6:12]
        self.life_respond = self.respond[6:12]
        self.life_incorrect_answer = self.handle_incorrect_answer(user_answer=self.life_answer,correct_answer=self.life_correct_answer)
        self.life_incorrect_answer_index = self.handle_incorrect_answer_index(user_answer=self.life_answer,correct_answer=self.life_correct_answer)
        self.life_incorrect_title = [self.correct_answer[i] for i in self.life_incorrect_answer_index]
        
    # E.生活作息建議
    def life_template(self)->TemplateSendMessage:
        message = TemplateSendMessage(
            alt_text='生活作息建議',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url="https://imgur.com/dxHQuNH.jpg",
                        title = f"題目:{self.life_incorrect_title[i]}\n您的回答:{self.life_incorrect_answer[i]}",
                        text=self.life_respond[i],
                        actions=[
                            PostbackTemplateAction(
                                label=' ',
                                data='do_nothing'
                            )
                        ]
                    )for i in range(len(self.life_incorrect_title))
                ]
            )
        )
        return message