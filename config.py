# config.py
class Config:
    SECRET_KEY = "super-secret"
    JWT_SECRET_KEY = "jwt-secret"
    JWT_TOKEN_LOCATION = ["headers"]
    JWT_HEADER_NAME = "Authorization"
    JWT_HEADER_TYPE = "Bearer"  # ✅ Must match frontend header

    SQLALCHEMY_DATABASE_URI = "sqlite:////mnt/data/data.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
