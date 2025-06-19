import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = "random"
TOKEN = os.getenv('TOKEN')
WEBHOOK = os.getenv('WEBHOOK')
