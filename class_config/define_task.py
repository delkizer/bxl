
def initialize_task_events(events):
    task_events = {}

    for event_name, event_class in events.items():
        task_events[event_class.TASK_NAME] = {
            "class": event_class,
            "description": event_class.DESCRIPTION,
            "status": "initialized",     # 초기 상태를 설정 (initialized, running, error 등)
            "last_update": None,  # 마지막 상태 갱신 시간
            "job_types": [
                {
                    "job_type": event_class.TASK_NAME,
                    "job_description": event_class.DESCRIPTION
                }
            ]
        }

    return task_events