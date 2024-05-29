#!/usr/bin/env python3


import logging
import os
from urllib.parse import quote_plus as urlquote
from ..decorator import Decorator

logger = logging.getLogger(__name__)


class Databricks(Decorator):
    def __init__(self, config: dict):
        super().__init__(config)
        self.is_valid = False

    def validate_config(self):
        super().validate_config()
        logger.info("Validating the paylod for the Databricks connection")
        message = ""

        if not self.is_valid:
            hostname = self.config.get("hostname", None)
            token = self.config.get("token", None)
            http_path = self.config.get("http_path", None)
            catalog = self.config.get("catalog", None)
            schema = self.config.get("schema", None)

            if not hostname:
                message = f"Invalid connection details. Hostname is required.{os.linesep}"
                self.is_valid = False
                logger.error(message)
            elif not token:
                message = f"Invalid connection details. Token is required.{os.linesep}"
                self.is_valid = False
                logger.error(message)
            elif not http_path:
                message = f"Invalid connection details. Http path is required.{os.linesep}"
                self.is_valid = False
                logger.error(message)
            elif not catalog:
                message = f"Invalid connection details. Catalog is required.{os.linesep}"
                self.is_valid = False
                logger.error(message)
            elif not schema:
                message = f"Invalid connection details. Schema is required.{os.linesep}"
                self.is_valid = False
                logger.error(message)
            else:
                self.is_valid = True

            if self.is_valid:
                logger.info("Connection is valid")

                if message:
                    logger.info(message)

        return self.is_valid, message

    def create_uri(self):
        super().create_uri()
        logger.info("Call for creating the URI for Databricks")

        is_valid, message = self.validate_config()
        uri = None
        if is_valid:
            hostname = self.config.get("hostname", None)
            token = self.config.get("token", None)
            http_path = self.config.get("http_path", None)
            catalog = self.config.get("catalog", None)
            schema = self.config.get("schema", None)
            if token:
                token = urlquote(token)

            uri = (
                f"databricks://token:{token}@{hostname}?"
                f"http_path={http_path}&catalog={catalog}&schema={schema}"
            )

            logger.info("URI created for Databricks")
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
