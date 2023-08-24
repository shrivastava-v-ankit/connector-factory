#!/usr/bin/env python3


import logging
import os
import sys

from ..decorator import Decorator

logger = logging.getLogger(__name__)


class Sqlite3(Decorator):
    def __init__(self, config: dict):
        path = config.get("path", None)
        if not path:
            # Check current OS, it is Windows or Linux
            is_windows = sys.platform.lower().startswith("win")
            if is_windows:
                path = f"{os.environ['HOMEDRIVE']}{os.environ['HOMEPATH']}"
            else:
                path = os.environ["HOME"]
            config["path"] = path
        super().__init__(config)
        self.is_valid = False

    def validate_config(self):
        super().validate_config()
        logger.info("Validating the paylod for the Sqlite3 connection")
        message = None

        if not self.is_valid:
            path = self.config.get("path", None)
            database = self.config.get("database", None)

            if not database:
                message = f"Invalid connection details. database name is required.{os.linesep}"
                self.is_valid = False
                logger.error(message)

            if ".db" not in database:
                database = f"{database}.db"

            db_file = os.path.join(path, database)
            # if not os.path.exists(db_file):
            #     message = f"Invalid connection details. Database is not present at {db_file}.{os.linesep}"
            #     self.is_valid = False
            #     logger.error(message)
            # else:
            #     self.is_valid = True

            self.is_valid = True
            if self.is_valid:
                logger.info("Connection is valid")

                if message:
                    logger.info(message)

        return self.is_valid, message

    def create_uri(self):
        super().create_uri()
        logger.info("Call for creating the URI for Sqlite3")

        is_valid, message = self.validate_config()
        if is_valid:
            path = self.config.get("path", None)
            database = self.config.get("database", None)

            if ".db" not in database:
                database = f"{database}.db"

            uri = f"sqlite:///{os.path.join(path, database)}"
            logger.info("URI created for Sqlite3")
            return uri, None, None
        else:
            return None, is_valid, message

    def get_session(self, uri: str, param: dict = {}, description_encoding: bool = False):
        is_valid = False
        message = None
        if not self.session:
            logger.info("Session is not created. Try to create a session")
            uri, is_valid, message = self.create_uri()
            param = {}
            description_encoding = None

            if uri:
                super().get_session(uri, param, description_encoding)

        return self.session, is_valid, message
