#!/usr/bin/env python

"""
File holds the module of Migration database manager and decide to connect with
multiple databases using the configuration parameters.
URI of database handled automatically for multiple databases using SQLAlchemy
"""

import os
import logging
import pandas


logger = logging.getLogger(__name__)

SUPPORTED_ENGINE = ["postgre",
                    "mysql",
                    "mariadb",
                    "snowflake",
                    "redshift",
                    "sqlite",
                    "salesforce",
                    "s3select"
                    "aws"]

SUPPORTED_SECRET_MANAGER_CLOUD = ["aws", "gcp"]


class ConnectorFactory(object):
    """Class handle the Database Manager using SQLAlchemy Dialects or specific
    object of supported python libraries which don't supports SQLAlchemy.
    If any connector doesn't support SQLAlchemy, then wrapper is limited to select
    and get. For extended functionality get_session method class can be called to get
    pure object and that can be used further in the code as per need.

    Example: Databases which supports SQLAlchemy:
      * Snowflake
      * Redshift
      * PostgresSQL
      * MySql
      * MariaDb and etc
    Example: Which don't support SQLAlchemy:
      * Salesforce: It uses simple-salesforce python library
      * S3: It uses boto3 python library
      * S3Select: It uses boto3 python library

    Methods:
    --------

        __init__:               Initaization functions
        fetch_from_secret:      Method to fetch the values from Cloud Secret Manager
        Service.
        create_uri:             Method uses the initalization parameter and
        create the uri for the provided engine with proper driver.
        create_session:         Method to create the SQLAlchemy session for the
                                initalized the engine type.
        execute_sql:            Function to execute DML or DDL queries and return
                                with rows if rows exist.
        execute_df:             Function to execute Pandas DataFrame object.
        get_df:                 Function to execute DML select queries and return
                                as Pandas DataFrame.
        object
    """

    def __init__(self,
                 connector_type: str,
                 config: dict,
                 debug: bool = False
                 ):
        """Initialization function to initlaize the object

        Args:
            connector_type (str): (Required) => Type of connector type for connection.
                                    One of the below supported engines:
                                    * postgre
                                    * mysql
                                    * mariadb
                                    * snowflake
                                    * s3select
                                    * sqlite
                                    * redshift
                                    * salesforce
            config (dict):  (Required) => Dictonary of connection details like username, password, host, port etc.
            debug (bool, optional): (Optional) => Detailed logs for debugging.. Defaults to False.
        """

        self.engine_type = connector_type
        self.config = config
        self.debug = debug
        self.config["connection_type"] = self.engine_type
        self.config["debug"] = self.debug
        self.connection = None
        self.is_connector = False

        if self.engine_type in ["sqlite"]:
            from .connectors.sqlite3 import Sqlite3 as Connector
            self.is_connector = True
        elif self.engine_type in ["postgre"]:
            from .connectors.postgreSQL import PostgreSQL as Connector
            self.is_connector = True
        elif self.engine_type in ["mysql", "mariadb"]:
            from .connectors.mysql import Mysql as Connector
            self.is_connector = True
        elif self.engine_type in ["snowflake"]:
            from .connectors.snowflake import Snowflake as Connector
            self.is_connector = True
        elif self.engine_type in ["bigquery"]:
            pass
        elif self.engine_type in ["salesforce"]:
            from .connectors.salesforce import Salesforce as Connector
            self.is_connector = True
        elif self.engine_type in ["redshift"]:
            from .connectors.redshift import Redshift as Connector
            self.is_connector = True
        elif self.engine_type in ["s3select"]:
            from .connectors.s3select import S3Select as Connector
            self.is_connector = True
        elif self.engine_type in ["aws"]:
            from .connectors.aws import Aws as Connector
            self.is_connector = True

        if self.is_connector:
            self.connection = Connector(self.config)

    def create_session(self):
        """Method to create the SQLAlchemy session for the initalized the engine type.
        Use the class variables and update to hold the sessions.

        Raises:
            ValueError: Exception message
        """
        if self.is_connector:
            try:
                logger.info(
                    f"Creating session scope for the requested connection.")
                self.connection.get_session(uri=None)
                logger.info(f"Connection session scope is created")
            except Exception as err:
                logger.exception(
                    f"Failed to create session with given paramaters for Database", err)
                raise ValueError(err)
        else:
            return f"Invalid connection type : {self.engine_type}. Valid type is anyone from {SUPPORTED_ENGINE}"

    # def fetch_from_secret(self):
    #     """
    #     Method to fetch the values from Cloud Secret Manager Service.
    #     Use the class variables for the paramaters.

    #     *******
    #     Return:
    #     -------

    #         secret: Secrets if secret id is provided else None
    #     """
    #     secret = None

    #     if self.secret_id and self.secrete_manager_cloud:
    #         logger.info(f"Fetch secrets from cloud secret manager service")
    #         try:
    #             secret = Common.get_secret(
    #                 secret_id=self.secret_id,
    #                 secrete_manager_cloud=self.secrete_manager_cloud,
    #                 aws_region=self.aws_region)
    #         except Exception as err:
    #             logger.exception(
    #                 f"Failed to fetch secrets from the Secret Manager Service", err)
    #     else:
    #         logger.info(
    #             f"Secret id is not set. Will use plain authentication.")

    #     return secret

    def get_connection(self):
        self.create_session()

        if self.is_connector:
            connection, valid, message = self.connection.get_session(uri=None)
            if not valid:
                logger.error(message)
                raise ValueError(message)
            else:
                return connection
        else:
            return f"Invalid connection type : {self.engine_type}. Valid type is anyone from {SUPPORTED_ENGINE}"

    def execute_sql(self, sql: str):
        """
        Function to execute DML or DDL queries and return if rows exist.

        ***********
        Attributes:
        -----------

            sql:        (Required) => Plain DDL or DML query to execute on
                        Database.
                        Default is None. One of paramater sql_query or
                        panda_df is required. If both is provided panda_df
                        will be taken as priority and sql_query is ignored.
        *******
        Return:
        -------

            rows:       If rows in case of DML select queries else none.
        """

        if self.is_connector:
            return self.connection.execute_sql(sql=sql)
        else:
            return f"Invalid connection type : {self.engine_type}. Valid type is anyone from {SUPPORTED_ENGINE}"

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

        if self.is_connector:
            return self.connection.execute_df(panda_df=panda_df,
                                              table_name=table_name,
                                              chunk_size=chunk_size,
                                              exist_action=exist_action)
        else:
            return f"Invalid connection type : {self.engine_type}. Valid type is anyone from {SUPPORTED_ENGINE}"

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

        if self.is_connector:
            return self.connection.get_df(sql=sql, chunk_size=chunk_size)
        else:
            return f"Invalid connection type : {self.engine_type}. Valid type is anyone from {SUPPORTED_ENGINE}"
