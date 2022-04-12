from starlette.config import Config


config = Config(f".env")
DATABASE_URL = config("DATABASE_URL", cast=str, default="")
URL_TRANSACTION_MAIN_SERVER = config("URL_TRANSACTION_MAIN_SERVER", cast=str, default="")
URL_MAIN_HTML = config("URL_MAIN_HTML", cast=str, default="")
