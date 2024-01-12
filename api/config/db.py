from database.register import UserDatabase
from dotenv import load_dotenv
import os

load_dotenv()


db = UserDatabase(os.getenv("url"))
