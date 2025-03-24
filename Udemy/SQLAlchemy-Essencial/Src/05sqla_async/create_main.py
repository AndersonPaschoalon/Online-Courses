from conf.db_session import create_tables

use_sqlite = True


if __name__ == "__main__":
    create_tables(use_sqlite)
    print("create_main.py finished successfully.")
