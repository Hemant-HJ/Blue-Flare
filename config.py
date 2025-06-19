import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI")
TOKEN = os.getenv('TOKEN')
WEBHOOK = os.getenv('WEBHOOK')
