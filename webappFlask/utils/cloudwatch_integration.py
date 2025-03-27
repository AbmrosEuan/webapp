import os
import time
import logging
from configparser import ConfigParser

from statsd import StatsClient
from functools import wraps
from flask import request
from app.setting import Settings
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 配置文件和数据文件目录
CONFIG_DIR = os.path.join(BASE_DIR, 'config')

CONFIG = ConfigParser()
CONFIG.read(os.path.join(CONFIG_DIR, 'develop' + '_config.conf'), encoding='utf-8')

# Configure StatsD client to send to local CloudWatch Agent (make sure Agent is listening on port 8125)
statsd = StatsClient(host='localhost', port=8125, prefix='flaskapp')
statsd.incr('my_custom_metric')

# Configure logging (send logs to a file that CloudWatch Agent will watch)
logging.basicConfig(
    filename= CONFIG['LOG']['flask_log'],
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

logger = logging.getLogger(__name__)


def metrics_timer(metric_name):
    """
    Decorator to wrap Flask endpoints or any function to measure duration and call count.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            statsd.incr(f"{metric_name}.count")  # Count each call
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.exception(f"Exception in {metric_name}: {str(e)}")
                raise
            finally:
                elapsed_ms = int((time.time() - start) * 1000)
                statsd.timing(f"{metric_name}.latency", elapsed_ms)  # Report time in ms
        return wrapper
    return decorator


def log_request():
    """
    Logs incoming request info for audit/debug.
    """
    logger.info(f"Request: method={request.method}, path={request.path}, endpoint={request.endpoint}, remote_addr={request.remote_addr}")


def log_error(e):
    logger.exception(f"Error occurred: {e}")


# Usage example in Flask views or resource classes:
# @metrics_timer("api.upload_file")
# def upload_file(): ...
#
# @metrics_timer("db.query.user")
# def get_user(): ...
#
# Within request hooks:
# log_request()
