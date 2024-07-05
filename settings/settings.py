from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URI = os.getenv("DATABASE_URI")
JWT_SECRET = os.getenv("JWT_SECRET")