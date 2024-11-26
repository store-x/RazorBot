from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    BOT_TOKEN = os.getenv("BOT_TOKEN", '7003380139:AAG-FAxLg2ODj5f3MwPzYos67tp3EMziSHc')
    API_ID = int(os.getenv("API_ID", 12380656)) 
    API_HASH = os.getenv("API_HASH", 'd927c13beaaf5110f25c505b7c071273')  
    MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://queenxytra:queenxytra@cluster0.ivuxz80.mongodb.net/?retryWrites=true&w=majority")
    # Razorpay Keys
    RAZORPAY_API_KEY = os.getenv("RAZORPAY_API_KEY")
    RAZORPAY_API_SECRET = os.getenv("RAZORPAY_API_SECRET")
    # General Bot Settings
    MAX_CHANNELS_PER_PAGE = int(os.getenv("MAX_CHANNELS_PER_PAGE", 5))  # Default is 5 channels per page
    PAYMENT_TIMEOUT_MINUTES = int(os.getenv("PAYMENT_TIMEOUT_MINUTES", 15))  # Default is 15 minutes
    ADMINS = list(map(int, os.getenv("ADMIN_IDS", '22,6567513746').split(",")))  # Comma-separated admin user ID
    LOG_GROUP = 7594

