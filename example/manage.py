#!/usr/bin/env python
import os
import sys
from multiprocessing import Process

# python manage.py runserver 0.0.0.0:2001 --noreload
if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
    os.environ.setdefault("DJANGO_SETTINGS_ENV", "DEV")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # process = Process(target=execute_from_command_line, args=(["", "runworker", 'NotifyTask', 'AsyncTask'],))
    # print("启动子进程")
    # process.start()

    execute_from_command_line(sys.argv)
    # process.join()
