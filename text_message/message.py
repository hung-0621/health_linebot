from linebot.models import *
# 處理輸入文字
class message():
    
    # ===機器人文字回復處理===
    
    # 健康建議(飲食建議、心理健康建議)
    def health_advice():
        message = TextSendMessage(
            text='請選擇需要哪一方面的健康建議',
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=MessageAction(label="飲食建議", text="健康生活Linebot給我飲食建議")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="心理健康建議", text="健康生活Linebot給我心理健康建議")
                    ),
                ]
            )
        )
        return message
    
    # ===選單按鈕文字處理===
    
    # A.使用說明
    def how_to_use()->TextSendMessage:
        message = TextSendMessage(  
            text=
       """歡迎使用健康生活LineBot
        \n\t======使用說明======
        \n1. 輸入"健康評估"填寫表單，健康生活linebot將會為您分析各項數據。
        \n2.在您填寫完表單後，您將可以使用「心理健康建議」、「飲食建議」、「運動模式建議」功能查看您的健康數據。
        \n3. 輸入"健康建議"取得您需要的建議。
        """
        )
        return message
    
    # B.搜尋健身房的使用說明
    def how_to_use_location()->TemplateSendMessage:  #轉盤樣板
        Instruction=[
            '搜尋附近健身房的使用說明：',
            '1.首先點擊左下角的鍵盤按鈕',
            '2.點擊左側的第二個箭頭按鈕',
            '3.點擊左側的加號按鈕',
            '4.點擊位置資訊',
            '5.選取您的位置後，點擊右上角的分享'
            ]
        message = TemplateSendMessage(
            alt_text='搜尋健身房功能的使用說明',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/4QfKuz1.png',
                        title = s,
                        text='（請向右滑動）',
                        actions=[
                            PostbackTemplateAction(
                                label=' ',
                                data='do_nothing'
                            )
                        ]
                    )for s in Instruction
                ]
            )
        )
        return message
    
    # C.健康評估
    def health_assessment(user_name:str,user_id:str)->TextSendMessage:
        form_url = "https://docs.google.com/forms/d/e/1FAIpQLSd-wniwRvdQl6xSBVvMV0ZqO4QfK46aKN3Upki01VeD712I7w/viewform"
        form_url_with_id = f"{form_url}?entry.1419820681={user_name}&entry.935941896={user_id}"
        message = TextSendMessage(  
            text = f"""健康評估功能介紹：\n1.請您先填寫健康評估表單
                                        \n2.完成填寫後可以使用「飲食建議」、「心理健康建議」、「運動模式建議」查詢我們為您分析的結果
                                        \n這是健康評估表單的連結：{form_url_with_id}
                                        \n***請注意不要修改「用戶名稱」、「用戶ID」欄位***"""
        )
        return message
    # D.心理健康建議
    def mental_assessment():
        pass
    # E.飲食建議
    def eat_assessment():
        pass
    # F.合適運動
    def sport_assessment():
        pass