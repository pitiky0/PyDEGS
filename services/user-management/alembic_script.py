import os
import shutil

from alembic.config import Config
from alembic import command
from sqlalchemy import create_engine, text

from database import SQLALCHEMY_DATABASE_URL, DB_DATABASE


def init_alembic():
    if os.path.exists("alembic/versions"):
        # delete alemic/ directory and all its contents
        shutil.rmtree("alembic/")

    # Initialize Alembic
    command.init(config=Config(file_="alembic.ini"), directory="alembic")

def generate_revision(message):
    # Generate a new revision
    command.revision(config=Config(file_="alembic.ini"), message=message, autogenerate=True)

def upgrade_head():
    # Upgrade to the latest revision
    command.upgrade(config=Config(file_="alembic.ini"), revision="head")

def create_database_if_not_exists(database_url):
    database_url_without_db = database_url.rsplit("/", 1)[0]
    # Create a database engine without specifying the database name
    engine = create_engine(database_url_without_db, isolation_level="AUTOCOMMIT")

    # Check if any alembic migration exists if so, drop the file
    if os.path.exists("alembic/versions"):
        print("alembic/versions directory exists")
        if len(os.listdir("alembic/versions")) > 0:
            print("alembic/versions directory is not empty")
            print("deleting all files in alembic/versions directory")
            for file in os.listdir("alembic/versions"):
                if file.endswith(".py"):
                    os.remove(f"alembic/versions/{file}")
            print("all files in alembic/versions directory deleted")
        else:
            print("alembic/versions directory is empty")

    # Execute SQL statement to create the database if it does not exist
    with engine.connect() as connection:
        connection.execute(text(f"CREATE DATABASE IF NOT EXISTS {DB_DATABASE}"))
        connection.execute(text(f"USE {DB_DATABASE}"))
        # check if alembic version table exists
        result = connection.execute(text("SHOW TABLES LIKE 'alembic_version'"))
        print("table alembic_version exists" if result.rowcount != 0 else "table alembic_version does not exist")
        if result.rowcount != 0:
            connection.execute(text("drop table alembic_version"))
            print("table alembic_version dropped")

if __name__ == "__main__":
    # Check if alembic.ini exists, if not, initialize Alembic
    if not os.path.exists("alembic.ini"):
        print("Alembic configuration file (alembic.ini) not found.")

    print("Initializing Alembic...")
    init_alembic()

    # Create database if it does not exist
    print(f"Creating database if not exists")
    create_database_if_not_exists(SQLALCHEMY_DATABASE_URL)

    # Update SQLAlchemy database URL in alembic.ini
    with open("alembic.ini", "r") as file:
        lines = file.readlines()

    for idx, line in enumerate(lines):
        if line.startswith("sqlalchemy.url = driver://"):
            lines[idx] = f"sqlalchemy.url = {SQLALCHEMY_DATABASE_URL}\n"

    with open("alembic.ini", "w") as file:
        file.writelines(lines)

    # modify target_metadata in env.py from None to Base.metadata
    with open("alembic/env.py", "r") as file:
        lines = file.readlines()

    for idx, line in enumerate(lines):
        if line.startswith("target_metadata = None"):
            lines[idx] = f"from models import Base\ntarget_metadata = Base.metadata\n"

    with open("alembic/env.py", "w") as file:
        file.writelines(lines)

    # Generate a new revision
    revision_message = "create tables"
    print(f"Generating revision: {revision_message}")
    generate_revision(revision_message)

    # Upgrade to the latest revision
    print("Upgrading to the latest revision...")
    upgrade_head()

    print("Done.")
