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
        self.life_incorrect_title = [self.life_title[i] for i in self.life_incorrect_answer_index]
        
    # F.生活作息建議
    def life_template(self)->TemplateSendMessage:
        if self.life_incorrect_answer == []:
            message = message = TemplateSendMessage(
                alt_text='生活作息建議',
                template=CarouselTemplate(
                    columns=[
                        self.no_incorrect_answer_column(title="生活",image_url="https://raw.githubusercontent.com/hung-0621/health_linebot/get_user_data/images/life_image.jpg")
                    ]
                )
            )
        else:
            message = TemplateSendMessage(
                alt_text='生活作息建議',
                template=CarouselTemplate(
                    columns=[
                        CarouselColumn(
                            thumbnail_image_url="https://raw.githubusercontent.com/hung-0621/health_linebot/get_user_data/images/life_image.jpg",
                            title = f"題目:{self.life_incorrect_title[i]}\n您的回答:{self.life_incorrect_answer[i]}",
                            text = self.life_respond[self.life_incorrect_answer_index[i]],
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