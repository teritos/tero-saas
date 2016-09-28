from django.apps import AppConfig


class FtpdConfig(AppConfig):
    name = 'ftpd'
    verbose_name = 'FTP server'

    def ready(self):
        import plugins.ftpd.signals


