import os

from typing import Union

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from random import randint

# get connection string
from sandbox.working_code_staging.env_var import create_env_variables
create_env_variables()

# get models
from sandbox.working_code_staging.create_models  import SnekMovesMain

# define functions for connection
def get_connection_string() -> str:
    """
    returns the connection string from the environment

    :return: connection string
    """
    return os.environ.get("SNEK_CONNECTION_STRING")

def set_up_session(connection_string) -> Union[sessionmaker, create_engine]:
    """
    Return a session object using for a particular database connection using SQLAlchemy

    :param connection_string: connection string
    :return: None
    """
    engine = create_engine(connection_string)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session, engine

def loop_through_records(session, table):
    """
    loop through records and print them

    :param session: session object
    :return: None
    """
    for record in session.query(table).all():
        print(record)

def add_record(session, table, record):
    """
    add a record to the database

    :param session: session object
    :param table: table object
    :param record: record object
    :return: None
    """
    session.add(record)
    session.commit()

def main():
    """
    main function
    """
    # get string, connect to database, and set up session
    connection_string = get_connection_string()
    session, engine = set_up_session(connection_string)

    # get all records from SnekMovesMain
    records = session.query(SnekMovesMain).all()

    # print all records
    loop_through_records(session, SnekMovesMain)

    # add a record
    game, snek, record = [randint(1, 100000) for i in range(0, 3)]
    NewSnekMovesMain = SnekMovesMain(record=record, game=game, snek=snek, snek_name="Snek1", move_number=12,
                                     move_content="move1", outcome="win")
    add_record(session, SnekMovesMain, NewSnekMovesMain)