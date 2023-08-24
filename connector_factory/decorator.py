#!/usr/bin/env python3


import logging
from abc import ABC, abstractmethod
import pandas
import atexit


logger = logging.getLogger(__name__)


class Decorator(ABC):

    @abstractmethod
    def __init__(self, config: dict) -> None:
        super().__init__()
        self.config = config
        self.engine = None
        self.session = None
        self.engine_type = config.get("connection_type", None)
        self.debug = config.get("debug", False)
        pass

    @abstractmethod
    def validate_config(self):
        """Each database configuration class need to override this method
        and validate the provided connection details are given or not.
        """
        pass

    @abstractmethod
    def create_uri(self):
        """Each database configuration class need to override this method
        and create the URI depending upon the database signature.
        """
        pass

    def destroy(self):
        try:
            if (self.session):
                self.session.remove()
                self.engine.dispose(close=True)
                self.session = None
                self.engine = None
                logger.info("Successfully dispose the connection")
        except Exception as err:
            message = f"Failed to close connection"
            logger.error(message)

    @abstractmethod
    def get_session(self, uri: str, param: dict = {}, description_encoding: bool = False):
        """This method creates and return the SQLAlchemy Dialects session object of request database.

        Args:
            uri (str): Connection string of database to connect.
            param (dict, optional): Additional information to send to SQLAlchemy Dialects for connection. Defaults to {}.
            description_encoding (bool, optional): Specific to Postgres to disable description_encoding. Defaults to False. Reference: https: // github.com/sqlalchemy/sqlalchemy/issues/5645

        Raises:
            ValueError: Failed to create session with given paramaters for Database

        Returns:
            self.session: SQLAlchemy Dialects session object
        """
        from sqlalchemy import create_engine
        from sqlalchemy.orm import scoped_session
        from sqlalchemy.orm import sessionmaker
        try:
            if not self.session:
                logger.info(f"Creating SQLAlchemy Dialects session scope.")
                if param:
                    self.engine = create_engine(uri, echo=self.debug, **param)
                else:
                    self.engine = create_engine(uri, echo=self.debug)

                if description_encoding:
                    # https: // github.com/sqlalchemy/sqlalchemy/issues/5645
                    self.engine.dialect.description_encoding = None

                self.session = scoped_session(sessionmaker(bind=self.engine,
                                                           expire_on_commit=False))
                logger.info(f"SQLAlchemy Dialects session scope is created")

                atexit.register(self.destroy)

            return self.session
        except Exception as err:
            message = f"Failed to create session with given paramaters for Database"
            logger.exception(message, err)
            raise ValueError(message)

    # @abstractmethod
    def execute_sql(self, sql: str):
        """Function to execute DML or DDL queries and return if rows exist.

        Args:
            sql (str): (Required) => Plain DDL or DML query to execute on Database. Default is None. One of paramater sql_query or panda_df is required. If both is provided panda_df will be taken as priority and sql_query is ignored.

        Returns:
            rows: If rows in case of DML select queries else none.
        """
        logger.info(f"Got SQL statement to execute: {sql}")
        message = None

        if not self.session:
            _, _, message = self.get_session(None)

        if not self.session:
            raise ValueError(message)

        rows = None

        result = self.session.execute(sql)
        if result.returns_rows:
            rows = result.fetchall()
        else:
            self.session.commit()
        return rows

    # @abstractmethod
    def execute_df(self,
                   panda_df: pandas.DataFrame,
                   table_name: str,
                   chunk_size: int = None,
                   exist_action: str = "append"):
        """
        Function to execute Pandas DataFrame object to create, replace or
        append table with DataFrame table objects.

        ***********
        Attributes:
        -----------

            panda_df:       (Required) => Pandas DataFrame table object to
                            update the table.
                            Default is None. One of paramater sql_query or
                            panda_df is required. If both is provided panda_df
                            will be taken as priority and sql_query is ignored.
            table_name:     (Optional) => Name of table .
            chunk_size:     (Optional) => chunck size to update the table in
                            chunks for performance rather than insert row one
                            by one.
                            Default: 1 row at a time.
            exist_action:   (Optional) => Action on if table already exist.
                            Default: append mode. Others modes are replace
                            or fail.
        *******
        Return:
        -------

            rows:           If rows in case of DDL queries else none.
        """
        print("*************")
        logger.info(
            "Got pandas dataframe to insert/update in table {table_name}")
        message = None

        if not self.session:
            _, _, message = self.get_session(None)

        if not self.session:
            raise ValueError(message)

        if len(panda_df):
            logger.info(
                f"Got Pandas DataFrame. This will be used to insert data in table.")
            logger.info(
                f"Table name: {table_name} and action on table is already present: {exist_action}")
            logger.info(f"Chunk size to insert data is: {chunk_size}")

            panda_df.to_sql(name=table_name,
                            con=self.session.bind,
                            if_exists=exist_action,
                            chunksize=chunk_size,
                            index=False)
            self.session.commit()
        else:
            msg = f"Invalid DataFrame"
            logger.error(msg)
            raise ValueError(msg)

    # @abstractmethod
    def get_df(self,
               sql: str,
               chunk_size: int = None):
        """
        Function to execute DML select queries and return Pandas DataFrame
        object.

        ***********
        Attributes:
        -----------

            sql:            (Required) => Plain DDL or DML query to execute on
                            Database.
                            Default is None. One of paramater sql_query or
                            panda_df is required. If both is provided panda_df
                            will be taken as priority and sql_query is ignored.
            chunk_size:     (Optional) => If specified, return an iterator
                            where chunk_size is the number of rows to include
                            in each chunk.
                            Default: None to include all records.
        *******
        Return:
        -------

            rows:           If rows in case of DDL queries else none.
        """
        logger.info(f"Return pandas dataframe of a output from sql {sql}")
        message = None

        if not self.session:
            _, _, message = self.get_session(None)

        if not self.session:
            raise ValueError(message)

        if chunk_size:
            chunks_df = []
            for chunk in pandas.read_sql(sql=sql,
                                         con=self.session.bind,
                                         chunksize=chunk_size):
                chunks_df.append(chunk)
            df = pandas.concat(list(chunks_df)).reset_index(drop=True)
        else:
            df = pandas.read_sql(sql=sql,
                                 con=self.session.bind,
                                 chunksize=chunk_size)
        return df
