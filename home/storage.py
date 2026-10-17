import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage


class PrivateVoiceStorage(FileSystemStorage):
    @property
    def base_location(self):
        return settings.PRIVATE_VOICES_ROOT

    @property
    def location(self):
        return os.path.abspath(self.base_location)

    def url(self, name):
        raise ValueError('Ovoz faqat ruxsat tekshiriladigan tinglash sahifasi orqali ochiladi.')


def private_voice_storage():
    return PrivateVoiceStorage()
