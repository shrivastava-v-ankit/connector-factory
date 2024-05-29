#!/usr/bin/env python3


import logging
import pandas
import os
from ..decorator import Decorator
from pydynamodb import connect

logger = logging.getLogger(__name__)


class DynamoDb(Decorator):
    def __init__(self, config: dict):
        super().__init__(config)
        self.is_valid = False

    def validate_config(self):
        super().validate_config()
        logger.info("Validating the paylod for the DynamoDB connection")
        message = ""

        if not self.is_valid:
            region = self.config.get("region", None)
            if not region:
                message = f"{message}Region is not provided. Default 'us-east-1' will be used.{os.linesep}"

            self.is_valid = True

            if self.is_valid:
                logger.info("Connection is valid")

                if message:
                    logger.info(message)

        return self.is_valid, message

    def create_uri(self):
        raise ValueError(f"Unsupported method for AWS")

    def get_session(self, uri: str, param: dict = {}, description_encoding: bool = False):
        is_valid = True
        message = None
        if not self.session:
            is_valid, message = self.validate_config()

            if not is_valid:
                msg = f"Failed to validate the connection details {message}"
                logger.error(msg)
                raise ValueError(msg)
            else:
                logger.info("Session is not created. Try to create a session")
                self.session = connect(region_name="us-east-1").cursor()

        logger.info("DynaoDB will return the object of PyDynamoDB cursor")
        return self.session, is_valid, message

    def execute_df(self, panda_df: pandas.DataFrame, table_name: str, chunk_size: int = None, exist_action: str = "append"):
        raise ValueError(f"Unsupported method for DynaoDB")

    def __execute_sql(self, sql: str = None):
        logger.info(f"Got SQL statement to execute: {sql}")
        logger.info("Supported DDL/DML queries by PyDanomoDB can be executed")

        if not self.session:
            _, is_valid, message = self.get_session(uri=None)
            if not is_valid:
                msg = f"Failed to validate the connection details {message}"
                logger.error(msg)
                raise ValueError(msg)

        self.session.execute(sql)

    def execute_sql(self, sql: str = None):
        self.__execute_sql(sql=sql)
        if self.session.rowcount and not self.session.errors:
            rows = self.session.fetchall()
            return rows

        msg = f"Failed to execute query, details : {str(self.session.errors)}"
        logger.error(msg)
        raise ValueError(msg)

    def get_df(self, sql: str = None, chunk_size: int = None):
        self.__execute_sql(sql=sql)
        if self.session.rowcount and not self.session.errors:
            df = pandas.DataFrame(self.session.fetchall())
            df.columns = self.session.result_set.metadata.keys()
            return df

        msg = f"Failed to execute query, details : {str(self.session.errors)}"
        logger.error(msg)
        raise ValueError(msg)

    def destroy(self):
        try:
            self.session.close()
        except Exception as err:
            message = f"Failed to close connection"
            logger.error(message)
