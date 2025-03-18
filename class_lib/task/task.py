class Task:
    def __init__(self, name, coroutine, heartbeat_interval=10):
        self.name = name
        self.coroutine = coroutine  # 비동기 작업 함수
        self.heartbeat_interval = heartbeat_interval
        self.last_heartbeat = None
        self.restart_attempts = 0
        self.status = "running"

    def reset_restart_attempts(self):
        self.restart_attempts = 0

    def increment_restart_attempts(self):
        self.restart_attempts += 1
