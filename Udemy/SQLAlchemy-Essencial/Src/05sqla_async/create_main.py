import asyncio

from conf.db_session import create_tables

if __name__ == "__main__":
    asyncio.run(create_tables(True))
    asyncio.run(create_tables(False))
    print("create_main.py finished successfully.")
