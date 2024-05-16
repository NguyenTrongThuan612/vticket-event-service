from abc import ABC, abstractmethod
from django.core.files.base import File

class ImageStorageProvider(ABC):
    @abstractmethod
    def upload_image(self, file: File, file_name: str) -> str:
        pass