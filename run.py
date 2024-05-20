from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import*
import os

from text_message.gemini import gemini
from text_message.message import message
from location import*
from keep_bot_awake import*
from get_user_data.handle_google_sheet import*
from health_assessment.eat_assessment import eat
# ========================從這裡執行==================================

app = Flask(__name__)

# 從環境變數取得CHANNEL_ACCESS_TOKEN and CHANNEL_SECRET(要自己設定)
# 或是用下面這個
# line_bot_api = LineBotApi() # 填你的line CHANNEL_ACCESS_TOKEN
# handler = WebhookHandler() # 填你的line CHANNEL_ACCESS_TOKEN
# 請不要向任何人提供你的CHANNEL_ACCESS_TOKEN 和 CHANNEL_SECRET

line_bot_api = LineBotApi(os.getenv("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("CHANNEL_SECRET"))

# 跟Line連接
@app.route("/callback", methods=['POST'])
def webhook():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 喚醒Render
scheduler = BackgroundScheduler()
scheduler.add_job(SCHEDULED_HANDLER.handler, 'interval', minutes=14)
scheduler.start()

# 向Line傳送訊息
def send_message(line_bot_api,event,message):
    try:
        return line_bot_api.reply_message(event.reply_token,message)
    except:
        return line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
    
# 文字訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    # 用戶訊息
    mtext = event.message.text
    # 用戶ID
    user_id = event.source.user_id
    # 用戶名稱
    profile = line_bot_api.get_profile(user_id)
    user_name = profile.display_name
    print(user_name)
    print(user_id)
    # A.
    if mtext == '*操作說明*':
        send_message(line_bot_api=line_bot_api,event=event, message=message.how_to_use())
    # B.
    elif mtext == '*搜尋附近健身房的使用說明*':
        send_message(line_bot_api=line_bot_api,event=event, message=message.how_to_use_location())
    # C.
    elif mtext == '*健康評估*':
        send_message(line_bot_api=line_bot_api,event=event, message=message.health_assessment(user_name=user_name,user_id=user_id))
    # D.
    elif mtext == '*取得飲食狀況分析結果*':
        eat_assessment = eat()
        send_message(line_bot_api=line_bot_api,event=event, message=eat_assessment)
    # E.
    # elif mtext == '*取得心理健康狀況分析結果*':
    #     mental_assessment = google_sheets.mental()
    #     send_message(line_bot_api=line_bot_api,event=event, message=mental_assessment)# type TextSendMessage
    # F.
    # elif mtext == '*取得生活作息狀況分析結果*':
    #     sport_assessment = google_sheets.sport()
    #     send_message(line_bot_api=line_bot_api,event=event, message=life_assessment)
    
    #                        ===機器人回復===
    
    elif mtext[0] != "*" and mtext[-1] != "*":
        send_message(line_bot_api=line_bot_api,event=event,message=gemini.call_gemini(mtext=mtext))

# 位置訊息        
@handler.add(MessageEvent,message=LocationMessage)
def handle_location_message(event):
    send_message(line_bot_api=line_bot_api,event=event, message=location.map_location(event))

if __name__ == "__main__":
    app.run()