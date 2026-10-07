import os
from dotenv import load_dotenv

# Cargar variables de entorno del archivo .env
load_dotenv()

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./inventario.db")
    DB_FILE = os.getenv("DB_FILE", "inventario.db")

settings = Settings()
