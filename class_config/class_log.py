# -*- coding: utf-8 -*-
"""
Created on 2023-11-28

@author: island78
"""
import os
from class_config.class_env import Config
from loguru import logger


class ConfigLogger:
    LOG_FORMAT = "[{time}] [{level}] [PID: {process}] - {message}"

    def __init__(self, log_name='app_log', backupCount=365):
        self.config = Config()
        self.log_name = log_name
        self.backupCount = backupCount
        self.setup_log_listener()

    def setup_log_listener(self):
        """로깅 리스너 설정"""
        log_dir = self.config.django_log_path
        log_file = os.path.join(log_dir, self.log_name)
        
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        logger.remove()  # Remove default handler
        logger.add(
            log_file,
            rotation="00:00",  # Rotate at midnight
            retention=f"{self.backupCount} days",
            format=self.LOG_FORMAT,
            enqueue=True  # Ensure thread/process safety
        )

    @staticmethod
    def get_logger(name):
        # In loguru, loggers are configured globally, so we return the global logger.
        return logger.bind(name=name)
        
# SQLAlchemy 로거 설정
def setup_sqlalchemy_logger():
    config_logger = ConfigLogger('sqlalchemy_log', 60)
    return config_logger.get_logger('sqlalchemy.engine')



