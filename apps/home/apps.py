from django.apps import AppConfig


class HomeConfig(AppConfig):
    name = 'apps.home'

    def ready(self) :
        from jobs import updater
        updater.start()