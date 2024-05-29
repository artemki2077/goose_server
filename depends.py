from dotenv import load_dotenv
import os
from services.database_service import DataBaseService

load_dotenv()

# os.environ.get()


dataBaseService = DataBaseService()


def get_dataBaseService() -> DataBaseService:
    return dataBaseService