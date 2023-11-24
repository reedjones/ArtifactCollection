__author__ = "reed@reedjones.me"

# tasks.py

# from celery import shared_task, Task
# from celery.exceptions import SoftTimeLimitExceeded
#
from celery.exceptions import MaxRetriesExceededError
#
# class RetryTask(Task):
#     max_retries = 5
#     default_retry_delay = 60 * 5  # 5 minutes
#
# @shared_task(base=RetryTask)
# def example_retry_task():
#     # Your task logic here
#     pass


# @shared_task
# def example_periodic_task():
#     try:
#         # Your task logic here
#         pass
#     except SoftTimeLimitExceeded:
#         # Handle time limit exceeded
#         pass
#     except Exception as exc:
#         # Handle other exceptions
#         pass
