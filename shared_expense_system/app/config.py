class Config:
    SECRET_KEY = "dev_secret_key"

    # SQLite database
    SQLALCHEMY_DATABASE_URI = "sqlite:///../instance/database.db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DEBUG = True