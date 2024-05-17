import requests,os
from zoneinfo import ZoneInfo
from apscheduler.schedulers.background import BackgroundScheduler

class SCHEDULED_HANDLER:
        
        def handler():
                url = os.getenv('API_URL', None)
                try:
                        requests.get(url)
                        print('Server pinged successfully')
                except Exception as e:
                        print(f'Request failed with error {e}')


