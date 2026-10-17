from django.apps import AppConfig


class HomeConfig(AppConfig):
    name = 'home'

    def ready(self):
        from . import checks  # noqa: F401
