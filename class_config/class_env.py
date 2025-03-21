import environ
from pathlib import Path

class Config():
    BASE_DIR = Path(__file__).resolve().parent.parent
    ENV_FILE_PATH = BASE_DIR / '.env'

    def __init__(self):
        environ.Env.read_env(env_file=str(self.ENV_FILE_PATH))
        #print(f"BASE_DIR:{self.ENV_FILE_PATH}")
        env_default = environ.Env()

        # 환경별 .env 파일 결정
        django_env = env_default('DJANGO_ENV', default='development')
        env_file_name = f".env.{django_env}"
        env_file_path = self.BASE_DIR / env_file_name
        environ.Env.read_env(env_file=str(env_file_path))
        self.env = environ.Env()

    @property
    def project_home_path(self):
        return self.env('PROJECT_HOME_PATH')

    @property
    def django_log_path(self):
        return self.env('LOG_PATH')

    # 추가적으로 필요한 설정들을 property로 정의할 수 있습니다.
    @property
    def postgres_user(self):
        return self.env('POSTGRESSQL_USER')

    @property
    def postgres_pass(self):
        return self.env('POSTGRESSQL_PASSWORD')

    @property
    def postgres_host(self):
        return self.env('POSTGRESSQL_HOST')

    @property
    def postgres_port(self):
        return self.env('POSTGRESSQL_PORT')

    @property
    def postgres_db_name_spotv(self):
        return self.env('DB_NAME_SPOTV')

    @property
    def jwt_key_path(self):
        return self.env('JWT_KEY_PATH')

    @property
    def jwt_expire_minutes(self):
        return self.env('JWT_EXPIRE_MINUTES')

    @property
    def jwt_sub(self):
        return self.env('JWT_SUB')

    @property
    def set_cookie_secret(self):
        cookie_secret_str = str(self.env("SET_COOKIE_SECURE") or "").strip().lower()
        return cookie_secret_str == "true"

    @property
    def set_cookie_samesite(self):
        return self.env("SET_COOKIE_SAMESITE")