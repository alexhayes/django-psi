from appconf import AppConf

class PsiAppConf(AppConf):
    MEDIA_PATH = 'psi'
    SCREENSHOT = True
    URLS = []
    CELERY_QUEUE = 'default'