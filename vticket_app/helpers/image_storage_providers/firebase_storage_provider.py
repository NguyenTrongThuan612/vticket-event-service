from uuid import uuid4
from django.core.files.base import File
from django.core.files.uploadedfile import InMemoryUploadedFile
from firebase_admin import credentials, initialize_app, storage, get_app

from vticket_app.helpers.image_storage_providers.image_storage_provider import ImageStorageProvider

class FirebaseStorageProvider(ImageStorageProvider):
    __bucket = None
    
    def __init__(self) -> None:
        self.initialize_firebase()

    def initialize_firebase(self):
        self.__bucket = storage.bucket()

    def upload_image(self, file: InMemoryUploadedFile) -> str:
        blob = self.__bucket.blob(f"{str(uuid4())}_{file.name}")
        blob.upload_from_file(file, content_type=file.content_type)
        blob.make_public()
        
        return blob.public_url