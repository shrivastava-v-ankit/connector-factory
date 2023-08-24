#!/usr/bin/env python3


import logging
import pandas

from ..decorator import Decorator

logger = logging.getLogger(__name__)


class Aws(Decorator):
    def __init__(self, config: dict):
        super().__init__(config)
        self.is_valid = True

    def validate_config(self):
        raise ValueError(f"Unsupported method for AWS")

    def create_uri(self):
        raise ValueError(f"Unsupported method for AWS")

    def get_session(self, uri: str = None, param: dict = {}, description_encoding: bool = False):
        is_valid = True
        message = None
        if not self.session:
            logger.info("Session is not created. Try to create a session")

            access_key = self.config.get("access_key", None)
            secret_key = self.config.get("secret_key", None)
            session_token = self.config.get("session_token", None)
            region = self.config.get("region", "us-east-1")

            import boto3
            self.session = boto3.session.Session(aws_access_key_id=access_key,
                                                 aws_secret_access_key=secret_key,
                                                 aws_session_token=session_token,
                                                 region_name=region)
        logger.info("AWS will return the object of boto3 session")
        return self.session, is_valid, message

    def execute_df(self, panda_df: pandas.DataFrame, table_name: str, chunk_size: int = None, exist_action: str = "append"):
        raise ValueError(f"Unsupported method for AWS")

    def execute_sql(self, sql: str):
        raise ValueError(f"Unsupported method for AWS")

    def get_df(self, sql: str, chunk_size: int = None):
        raise ValueError(f"Unsupported method for AWS")

    def destroy(self):
        pass
