import random
import time


def upload_file(file):
    time.sleep(2)
    return f"https://example.com/path/to/uploaded/file_{random.randint(1, 100000)}.jpg"