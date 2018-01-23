from django.apps import AppConfig

import os

VERBOSE_APP_NAME = u"访客列表"

def get_current_app_name(_file):
    return os.path.split(os.path.dirname(_file))[-1]

class AccessorConfig(AppConfig):
    name = get_current_app_name(__file__)
    verbose_name = VERBOSE_APP_NAME
