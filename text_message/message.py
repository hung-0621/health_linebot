from linebot.models import *
# 處理輸入文字
class message():
    
    # ===選單按鈕文字處理===
    
    # A.使用說明
    def how_to_use()->TextSendMessage:
        message = TextSendMessage(  
            text=
       """歡迎使用健康生活LineBot
        \n\t======使用說明======
        \n1. 請點選選單中的"健康評估"填寫表單，健康生活linebot將會為您分析各項數據。
        \n2. 在您填寫完表單後，您將可以使用「心理健康建議」、「飲食建議」、「生活作息建議」功能查看您的健康數據。
        \n3. 如果您需要一些建康相關的建議(不論是飲食、心理、生活、運動)，只要有相關的問題傳送給健康生活LineBot，他都會回應你！
        """
        )
        return message
    
    # C.健康評估
    def health_assessment(user_name:str,user_id:str)->TextSendMessage:
        form_url = "https://docs.google.com/forms/d/e/1FAIpQLSd-wniwRvdQl6xSBVvMV0ZqO4QfK46aKN3Upki01VeD712I7w/viewform"
        form_url_with_id = f"{form_url}?entry.1419820681={user_name}&entry.935941896={user_id}"
        message = TextSendMessage(  
            text = f"""健康評估功能介紹：\n1.請您先填寫健康評估表單。
                                        \n2.完成填寫後可以使用「飲食建議」、「心理健康建議」、「運動模式建議」查詢我們為您分析的結果。
                                        \n這是健康評估表單的連結：{form_url_with_id}"""        
                                        )
        return message
    # D.飲食建議
    def eat_assessment():
        # TDEE
        pass
    # E.心理健康建議
    def mental_assessment():
        pass

    # F.生活作息建議
    def life_assessment():
        pass