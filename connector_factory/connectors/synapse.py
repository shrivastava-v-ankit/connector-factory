#!/usr/bin/env python3


import logging
import os
from ..decorator import Decorator

logger = logging.getLogger(__name__)


class Synapse(Decorator):
    def __init__(self, config: dict):
        super().__init__(config)
        self.is_valid = False

    def validate_config(self):
        super().validate_config()
        logger.info("Validating the paylod for the Synapse connection")
        message = ""

        if not self.is_valid:
            username = self.config.get("username", None)
            password = self.config.get("password", None)
            host = self.config.get("host", None)
            port = self.config.get("port", None)
            database = self.config.get("database", None)
            driver = self.config.get("driver", None)
            trust_certificate = self.config.get("trust_certificate", None)
            connection_timeout = self.config.get("connection_timeout", None)

            if not username:
                message = f"Invalid connection details. Username is required.{os.linesep}"
                self.is_valid = False
                logger.error(message)
            elif not password:
                message = f"Invalid connection details. Password is required.{os.linesep}"
                self.is_valid = False
                logger.error(message)
            elif not host:
                message = f"Invalid connection details. Host is required.{os.linesep}"
                self.is_valid = False
                logger.error(message)
            elif not database:
                message = f"Invalid connection details. Database is required.{os.linesep}"
                self.is_valid = False
                logger.error(message)
            else:
                self.is_valid = True

            if not port:
                message = f"{message}Port is not provided will use default port as 1433.{os.linesep}"

            if not driver:
                message = f"{message}Driver is not provided will use default driver as ODBC Driver 17 for SQL Server.{os.linesep}"

            if not trust_certificate:
                message = f"{message}Trust certificate is not provided will use to ignore trusted certificate.{os.linesep}"

            if not connection_timeout:
                message = f"{message}Connection timeout with is not provided will use default 30 seconds.{os.linesep}"

            if self.is_valid:
                logger.info("Connection is valid")

                if message:
                    logger.info(message)

        return self.is_valid, message

    def create_uri(self):
        super().create_uri()
        logger.info("Call for creating the URI for Synapse")

        is_valid, message = self.validate_config()
        uri = None
        if is_valid:
            username = self.config.get("username", None)
            password = self.config.get("password", None)
            host = self.config.get("host", None)
            port = self.config.get("port", 1433)
            database = self.config.get("database", None)
            driver = self.config.get("driver", "ODBC Driver 17 for SQL Server")
            trust_certificate = self.config.get("trust_certificate", "no")
            authentication_with = self.config.get("authentication_with", None)
            connection_timeout = self.config.get("connection_timeout", 30)

            query = {
                "driver": driver,
                "TrustServerCertificate": trust_certificate,
                "Connection Timeout": str(connection_timeout)
            }

            query = {**query, **{"authentication": authentication_with}
                     } if authentication_with else query

            from sqlalchemy.engine import URL
            uri = URL.create("mssql+pyodbc",
                             username=username,
                             password=password,
                             host=host,
                             port=port,
                             database=database,
                             query=query)
            logger.info("URI created for Synapse")
        return uri, is_valid, message

    def get_session(self, uri: str, param: dict = {}, description_encoding: bool = False):
        is_valid = False
        message = None
        if not self.session:
            logger.info("Session is not created. Try to create a session")
            uri, is_valid, message = self.create_uri()
            if is_valid:
                param = {}
                description_encoding = None

                if uri:
                    super().get_session(uri, param, description_encoding)
            else:
                raise ValueError(message)

        return self.session, is_valid, message
