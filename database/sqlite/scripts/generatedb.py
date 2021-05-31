import sqlite3
import os.path
from contextlib import closing

DB = "../slow.db"
BASE_CREATE_SCRIPT = "./brazil-create-db.sql"
INSERT_SCRIPT = "./brazil-insert-cities.sql"
REPEAT_INSERT = 400

def create_db(cursor):
    db_already_created = os.path.isfile(DB)
    db_already_created = False

    if not db_already_created:
        print("Creating database!!!")
        with open(BASE_CREATE_SCRIPT, "r") as sql:
            cursor.executescript(sql.read())
    else:
        print("Skipping database creation")


def count_cities(cursor):
    return cursor.execute("SELECT count(*) from cities").fetchone()[0]


def main():
    with closing(sqlite3.connect(DB)) as db:
        with closing(db.cursor()) as cursor:
            create_db(cursor)

            with open(INSERT_SCRIPT, "r") as sql:
                insert_script = sql.read()

            for i in range(1, REPEAT_INSERT + 1):
                cursor.executescript(insert_script)
                cities = count_cities(cursor)
                print(f"#{i}: Reinserted! Now you have {cities} cities")


if __name__ == "__main__":
    main()