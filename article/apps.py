from django.apps import AppConfig

import os

VERBOSE_APP_NAME = u"文章列表"
 
 
def get_current_app_name(_file):
    return os.path.split(os.path.dirname(_file))[-1]

class ArticleConfig(AppConfig):
    name = get_current_app_name(__file__)
    verbose_name = VERBOSE_APP_NAME
