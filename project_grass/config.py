import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'universities.db')}"
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')  # Путь для загрузки файлов
    SECRET_KEY = "supersecretkey"  # 🔥 Добавляем секретный ключ!
