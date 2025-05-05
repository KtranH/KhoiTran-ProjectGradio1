import os
from dotenv import load_dotenv

# Load biến môi trường từ file .env
load_dotenv()

# Cấu hình kết nối SQL Server
DB_CONFIG = {
    "driver": os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server"),
    "server": os.getenv("DB_SERVER", "localhost"),
    "database": os.getenv("DB_NAME", ""),
    "username": os.getenv("DB_USER", ""),
    "password": os.getenv("DB_PASSWORD", ""),
    "trusted_connection": os.getenv("DB_TRUSTED_CONNECTION", "yes"),
}

# Tạo connection string
def get_connection_string():
    if DB_CONFIG["trusted_connection"].lower() == "yes":
        return f"DRIVER={{{DB_CONFIG['driver']}}};SERVER={DB_CONFIG['server']};DATABASE={DB_CONFIG['database']};Trusted_Connection=yes;"
    else:
        return f"DRIVER={{{DB_CONFIG['driver']}}};SERVER={DB_CONFIG['server']};DATABASE={DB_CONFIG['database']};UID={DB_CONFIG['username']};PWD={DB_CONFIG['password']};" 