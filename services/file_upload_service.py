import random
import time

from quickstart.models import FileSystemData


def upload_file(file):
    time.sleep(2)
    return f"https://example.com/path/to/uploaded/file_{random.randint(1, 100000)}.jpg"

def create_file_records(application, files):
    records = [
        FileSystemData(
            application=application,
            filename=filename,
            file=url
        )
        for filename, url in files
    ]

    return FileSystemData.objects.bulk_create(records)
