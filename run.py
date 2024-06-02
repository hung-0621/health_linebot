from flask import Flask, request, abort, jsonify
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import*
import os

from text_message.gemini import gemini
from text_message.message import message
from location import*
from keep_bot_awake import*
from get_user_data.handle_MySQL import*
from health_assessment.eat_assessment import eat
from health_assessment.life_assessment import life
from health_assessment.mental_assessment import mental
#from dotenv import load_dotenv 
# ========================從這裡執行==================================
# load_dotenv()

app = Flask(__name__)

line_bot_api = LineBotApi(os.getenv("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("CHANNEL_SECRET"))

# 跟LineBot連接
@app.route("/callback", methods=['POST'])
def webhook():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

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
    print(mtext)
    print(user_name)
    # A.
    if mtext == '*操作說明*':
        send_message(line_bot_api=line_bot_api,event=event, message=message.how_to_use())
        
    # B. LocationMessage
    
    # C.
    elif mtext == '*健康評估*':
        send_message(line_bot_api=line_bot_api,event=event, message=message.health_assessment(user_name=user_name,user_id=user_id))
    # D.
    elif mtext == '*取得飲食狀況分析結果*':
        eat_assessment = eat(user_id=user_id)
        send_message(line_bot_api=line_bot_api,event=event, message=eat_assessment.eat_template())
    # E.
    elif mtext == '*取得心理健康狀況分析結果*':
        mental_assessment = mental(user_id=user_id)
        send_message(line_bot_api=line_bot_api,event=event, message=mental_assessment.mental_template())# type TextSendMessage
    # F.
    elif mtext == '*取得生活作息狀況分析結果*':
        life_assessment = life(user_id=user_id)
        send_message(line_bot_api=line_bot_api,event=event, message=life_assessment.life_template())
    
    #                        ===機器人回復===
    
    elif mtext[0] != "*" and mtext[-1] != "*":
        send_message(line_bot_api=line_bot_api,event=event,message=gemini.call_gemini(mtext=mtext))

# 位置訊息        
@handler.add(MessageEvent,message=LocationMessage)
# B.
def handle_location_message(event):
    send_message(line_bot_api=line_bot_api,event=event, message=location.map_location(event))
    
# 填完表單更新DB
@app.route('/update', methods=['POST'])
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
            
    
# 喚醒Render
scheduler = BackgroundScheduler()
scheduler.add_job(SCHEDULED_HANDLER.handler, 'interval', minutes=14)
scheduler.start()


if __name__ == "__main__":
    app.run()
    
