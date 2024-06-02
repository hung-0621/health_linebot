from flask import Flask, request, abort, jsonify
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import*
import os,time
from text_message.gemini import Gemini
from text_message.message import message
from location import Location
from keep_bot_awake import*
from get_user_data.handle_MySQL import*
from health_assessment.eat_assessment import eat
from health_assessment.life_assessment import life
from health_assessment.mental_assessment import mental

class Main:
    def __init__(self):
        self.app = Flask(__name__)
        self.line_bot_api = LineBotApi(os.getenv("CHANNEL_ACCESS_TOKEN"))
        self.handler = WebhookHandler(os.getenv("CHANNEL_SECRET"))
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(SCHEDULED_HANDLER.handler, 'interval', minutes=14)
        self.scheduler.start()

        # 跟LineBot連接
        @self.app.route("/callback", methods=['POST'])
        def webhook():
            signature = request.headers['X-Line-Signature']
            body = request.get_data(as_text=True)
            try:
                self.handler.handle(body, signature)
            except InvalidSignatureError:
                abort(400)
            return 'OK'

        # 文字訊息
        @self.handler.add(MessageEvent, message=TextMessage)
        def handle_text_message(event):
            # 用戶訊息
            mtext = event.message.text
            # 用戶ID
            user_id = event.source.user_id
            # 用戶名稱
            profile = self.line_bot_api.get_profile(user_id)
            user_name = profile.display_name
            print(user_name)
            print(mtext)
            # A.
            if mtext == '*操作說明*':
                self.send_message(line_bot_api=self.line_bot_api,event=event, message=message.how_to_use())
            # B. LocationMessage
            # C.
            elif mtext == '*健康評估*':
                self.send_message(line_bot_api=self.line_bot_api,event=event, message=message.health_assessment(user_name=user_name,user_id=user_id))
            # D.
            elif mtext == '*取得飲食狀況分析結果*':
                eat_assessment = eat(user_id=user_id)
                self.send_message(line_bot_api=self.line_bot_api,event=event, message=eat_assessment.eat_template())
            # E.
            elif mtext == '*取得心理健康狀況分析結果*':
                mental_assessment = mental(user_id=user_id)
                self.send_message(line_bot_api=self.line_bot_api,event=event, message=mental_assessment.mental_template())# type TextSendMessage
            # F.
            elif mtext == '*取得生活作息狀況分析結果*':
                life_assessment = life(user_id=user_id)
                self.send_message(line_bot_api=self.line_bot_api,event=event, message=life_assessment.life_template())
            #                        ===機器人回復===
            elif mtext[0] != "*" and mtext[-1] != "*":
                bot = Gemini()
                self.send_message(line_bot_api=self.line_bot_api,event=event,message=bot.call_gemini(mtext=mtext))

        # 位置訊息        
        @self.handler.add(MessageEvent,message=LocationMessage)
        # B.
        def handle_location_message(event):
            location = Location()
            self.send_message(line_bot_api=self.line_bot_api,event=event, message=location.map_location(event))
    
        # 填完表單更新DB
        @self.app.route('/update', methods=['POST'])
        def update_MySQL():
            data = request.get_json()
            status = data.get("status")
            if bool(status):
                try:
                    print("=== update database ===")
                    time.sleep(2)
                    database = handle_MySQL()
                    database.load_data()
                    print("=== finish update ===")
                    return jsonify({'message': 'POST request received'}), 200
                except Exception as e:
                    print(f"An error occurred: {e}")
                    return jsonify({'message': 'An error occurred'}), 500
            else:
                return "status : False"

    # 向Line傳送訊息
    def send_message(self, line_bot_api, event, message):
        try:
            return line_bot_api.reply_message(event.reply_token,message)
        except:
            return line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

    def run(self):
        self.app.run()
        
if __name__ == "__main__":
    bot = Main()
    bot.run()
