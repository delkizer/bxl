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
        DJANGO_ENV = env_default('DJANGO_ENV', default='development')
        env_file_name = f".env.{DJANGO_ENV}"
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

