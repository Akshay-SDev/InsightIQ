import os

pg_db = os.getenv("POSTGRES_DB", "app_db")
pg_user = os.getenv("POSTGRES_USER", "app_user")
pg_password = os.getenv("POSTGRES_PASSWORD", "app_password")
pg_host = os.getenv("POSTGRES_HOST", "localhost")
pg_port = os.getenv("POSTGRES_PORT", "5432")

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.4")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
OPENAI_TEMPERATURE = float("0.5")