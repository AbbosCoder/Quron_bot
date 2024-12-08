from django.apps import AppConfig
from robot.utils import control



class RobotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'robot'
    verbose_name = 'Telegram bot'

    