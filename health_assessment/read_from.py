import gspread
from oauth2client.service_account import ServiceAccountCredentials
from health_assessment import eat_assessment


class google_sheets:
    
    def __init__(self,user_name,user_id,sheet_name,worksheet_name):
        self.user_name = user_name
        self.user_id = user_id
        self.sheet_name = sheet_name
        self.worksheet_name = worksheet_name
    
    def get_worksheet_info(self):
        # 使用JSON 憑證檔案
        scope = ['https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name("C:/Users/Kenny/Downloads/global-phalanx-421818-9a75b24317ed.json", scope)
        client = gspread.authorize(creds)

        # 打開試算表並選擇工作表
        sheet = client.open(self.sheet_name).worksheet(self.worksheet_name)

        # 讀取所有資料
        list_of_hashes = sheet.get_all_records()
        return list_of_hashes

# MySheet = google_sheets(user_name="宏",user_id="U8c1f7d50a448839c7f618636a8d2a8c0",sheet_name="健康評估 (回覆)",worksheet_name="DB")
# data = MySheet.get_worksheet_info()
# print(data)
# user_id = MySheet.user_id
# for row in data:
#     if row["用戶ID"] == user_id:
#         user_eat = eat_assessment.eat(user_id = row["用戶ID"],age = row["年齡"],height = row["身高"],weight = row["體重"],gender = row["性別"],activity_status = row["請問您每日的身體活動狀況？"])
#         print(user_eat.TDEE_Calculate())
        