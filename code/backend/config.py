import os


class Config():
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'super-secret'
    SECURITY_PASSWORD_SALT = 'super-secret-salt'
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authorization'
    

class LocalDev(Config):
    DEBUG = True

    SECRET_KEY = "shhh.... its secret"
    SECURITY_PASSWORD_SALT = 'super-secret-salt'
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authorization'
    WTF_CSRF_ENABLED = False
    
    
    CACHE_TYPE = "RedisCache"
    CACHE_DEFAULT_TIMEOUT = 30
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_HOST = "localhost"
    CACHE_REDIS_DB = 2
    

class Production(Config):
    DEBUG = False
    SECRET_KEY = 'super-secret'
    SECURITY_PASSWORD_SALT = 'super-secret-salt'
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authorization'
    

    