from get_user_data.handle_MySQL import *
from health_assessment.assessment import health_assessment
from health_assessment.eat_assessment import eat

monitor = handle_MySQL(user_id="U8c1f7d50a448839c7f618636a8d2a8c0")
# monitor.monitor_updates()
profile = monitor.get_data(table_name="profile")
answer = monitor.get_data(table_name="answer")
health_eat = eat(profile,answer=answer)
print(health_eat.TDEE_Calculate())