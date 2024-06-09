from dotenv import load_dotenv
import os
from services.database_service import DataBaseService

load_dotenv()


dataBaseService = DataBaseService(host='62.113.114.207', port=6380, password=os.environ.get('DB_PASSWOED'))


def get_dataBaseService() -> DataBaseService:
    return dataBaseService
