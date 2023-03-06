from django.apps import AppConfig


class HomeConfig(AppConfig):
    name = 'home'

    def ready(self) :
        from jobs import updater
        updater.start()