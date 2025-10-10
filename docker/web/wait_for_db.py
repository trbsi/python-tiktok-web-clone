#!/usr/bin/env python3
import os
import sys
import time

import django
from django.db import connections
from django.db.utils import OperationalError, ProgrammingError

# configure Django settings module so we can use ORM to check DB
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

# number of retries and delay
RETRIES = int(os.getenv("DB_WAIT_RETRIES", 30))
DELAY = int(os.getenv("DB_WAIT_DELAY", 2))


def main():
    django.setup()
    db_conn = connections['default']
    for attempt in range(RETRIES):
        try:
            # try a simple query
            c = db_conn.cursor()
            c.execute("SELECT 1;")
            return 0
        except (OperationalError, ProgrammingError) as e:
            print(f"[wait_for_db] DB not ready (attempt {attempt + 1}/{RETRIES}): {e}")
            time.sleep(DELAY)
    print("[wait_for_db] Could not connect to DB in time.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
