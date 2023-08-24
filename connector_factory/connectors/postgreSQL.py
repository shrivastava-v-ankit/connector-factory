#!/usr/bin/env python3


import logging
import os
from urllib.parse import quote_plus as urlquote

from ..decorator import Decorator

logger = logging.getLogger(__name__)


class PostgreSQL(Decorator):
    def __init__(self, config: dict):
        super().__init__(config)
        self.is_valid = False

    def validate_config(self):
        super().validate_config()
        logger.info("Validating the paylod for the PostgreSQL connection")
        message = ""

        if not self.is_valid:
            username = self.config.get("username", None)
            password = self.config.get("password", None)
            host = self.config.get("host", None)
            port = self.config.get("port", 5432)
            database = self.config.get("database", None)

            if not username or not password or not host:
                message = f"Invalid connection details. Username, host and password are required.{os.linesep}"
                self.is_valid = False
                logger.error(message)
            else:
                self.is_valid = True

            if not database:
                message = f"{message}Database is not provided. Consider USE statement to switch database or use fully qualified path.{os.linesep}"

            if not port:
                message = f"{message}Port is not provided will use default port as 5432.{os.linesep}"

            if self.is_valid:
                logger.info("Connection is valid")

                if message:
                    logger.info(message)

        return self.is_valid, message

    def create_uri(self):
        super().create_uri()
        logger.info("Call for creating the URI for PostgreSQL")

        is_valid, message = self.validate_config()
        uri = None
        if is_valid:
            username = self.config.get("username", None)
            password = self.config.get("password", None)
            host = self.config.get("host", None)
            port = self.config.get("port", 5432)
            database = self.config.get("database", "")

            if password:
                password = urlquote(password)

            uri = f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}"

            logger.info("URI created for PostgreSQL")
        return uri, is_valid, message

    def get_session(self, uri: str, param: dict = {}, description_encoding: bool = False):
        is_valid = False
        message = None
        if not self.session:
            logger.info("Session is not created. Try to create a session")
            uri, is_valid, message = self.create_uri()

            if is_valid:
                param = dict(client_encoding="utf8")
                description_encoding = True

                if uri:
                    super().get_session(uri, param, description_encoding)
            else:
                raise ValueError(message)

        return self.session, is_valid, message
