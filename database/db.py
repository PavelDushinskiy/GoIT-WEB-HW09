from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# from configparser import ConfigParser
# import os
# import sqlite3
# import pathlib

# ------- Postgresql configuration -------
# file_config = pathlib.Path(__file__).parent.parent.joinpath('config.ini')
# config = ConfigParser()
# config.read(file_config)

# user = config.get("DB-DEV", "user")
# password = config.get("DB-DEV", "password")
# host = config.get("DB-DEV", "domain")
# port = config.get("DB-DEV", "port")
# db_name = config.get("DB-DEV", "db_name")
#
# url = f'postgresql://{user}:{password}@{host}:{port}/{db_name}'
url = 'sqlite:///assistant.db'

Base = declarative_base()
engine = create_engine(url, echo=True, pool_size=5)
DBSession = sessionmaker(bind=engine)
session = DBSession()
