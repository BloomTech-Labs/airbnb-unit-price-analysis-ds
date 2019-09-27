# settings.py
import os
from dotenv import load_dotenv

# loading dotenv
load_dotenv(verbose=True)

DB_NAME=os.getenv("DB_NAME")
DB_USERNAME=os.getenv("DB_USERNAME")
DB_PASSWORD=os.getenv("DB_PASSWORD")
DB_HOST=os.getenv("DB_HOST")