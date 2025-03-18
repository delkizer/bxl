import os
import traceback
import asyncio
import signal
import multiprocessing
from class_config.class_log import ConfigLogger
from class_config.class_db import ConfigDB
from class_config.define_task import initialize_task_events
from class_lib.task.task_dummy import TaskDummy

# 이벤트 내부의 child 프로세스가 살아 있는지 여부
# TASK_EVENT에 없는 프로세스 재기동
# 외부에서 시그널을 받으면 해당 child process 재기동
# 일정 시간 동안 상태 업데이트를 못한 child process 재기동


# 이벤트 초기화 설정
events = {
    '''
    '''
    "TaskDummy": TaskDummy,
}
TASK_EVENTS = initialize_task_events(events)

# 로깅 설정
config_logger = ConfigLogger('task_log', 365)
logger = config_logger.get_logger('fastapi')
db_config = ConfigDB()

# SIGCHLD 핸들러 정의
def reap_child(signum, frame):
    while True:
        try:
            # 종료된 자식 프로세스를 수거
            pid, _ = os.waitpid(-1, os.WNOHANG)
            if pid == 0:
                break
            logger.info(f"Child process {pid} terminated and reaped.")
        except ChildProcessError:
            # 수거할 자식 프로세스가 없으면 종료
            break
        except Exception as e:
            logger.error(f"Error while reaping child process: {e} {traceback.format_exc()}")
            break

# SIGCHLD 시그널 핸들러 등록
signal.signal(signal.SIGCHLD, reap_child)

def start_task_process(task_name, handler_class):
    try:
        logger.info(f"Starting task: {task_name}")
        handler_instance = handler_class()
        asyncio.run(handler_instance.run())  # 비동기 태스크 실행
        logger.info(f"Task {task_name} completed successfully.")
    except Exception as e:
        logger.error(f"Error while running task {task_name}: {e} {traceback.format_exc()}")

def start_all_tasks():
    logger.info("Starting all task events with multiprocessing...")
    processes = []
    for task_name, task_info in TASK_EVENTS.items():
        handler_class = task_info["class"]
        process = multiprocessing.Process(target=start_task_process, args=(task_name, handler_class))
        process.start()
        processes.append(process)
        logger.info(f"Started process for task {task_name} with PID {process.pid}")

    # 모든 프로세스가 종료될 때까지 대기
    for process in processes:
        process.join()

if __name__ == "__main__":
    logger.info("Starting main_task with multiprocessing...")
    try:
        start_all_tasks()
    except Exception as e:
        logger.error(f"Critical error occurred in main_task: {e} {traceback.format_exc()}")
    finally:
        logger.info("Shutting down all tasks...")


