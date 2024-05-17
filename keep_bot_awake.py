import requests,os
from zoneinfo import ZoneInfo
from apscheduler.schedulers.background import BackgroundScheduler

# class SCHEDULED_HANDLER:
#         scheduler = BackgroundScheduler()
#         def __init__(self, line_bot_api,configuration):
#                 self.line_bot_api = line_bot_api
#                 self.configuration = configuration
#                 if not self.scheduler.running:
#                         self.set_schedule()
#                         self.scheduler.start()
#         # 讓Render不要休眠
#         def make_bot_keep_awake(self):
#                 print("== Make bot keep awake ==")
#                 requests.get(os.getenv('API_URL', None))
                
#         def set_schedule(self):
#                 self.scheduler.add_job(self.make_bot_keep_awake, 'interval',
#                                         minutes=1, timezone=ZoneInfo('Asia/Taipei'))
class SCHEDULED_HANDLER:
        
        def handler():
                url = os.getenv('API_URL', None)
                try:
                        response = requests.get(url)
                        if response.status_code == 200:
                                print('Server pinged successfully')
                        else:
                                print(f'Server ping failed with status code: {response.status_code}')
                except Exception as e:
                        print(f'Request failed with error {e}')

scheduler = BackgroundScheduler()
scheduler.add_job(SCHEDULED_HANDLER.handler, 'interval', minutes=1)
scheduler.start()
