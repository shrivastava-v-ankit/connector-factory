#!/usr/bin/env python3


import logging
import os
from urllib.parse import quote_plus as urlquote
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

from ..decorator import Decorator

logger = logging.getLogger(__name__)


class Snowflake(Decorator):
    def __init__(self, config: dict):
        super().__init__(config)
        self.is_valid = False

    def validate_config(self):
        super().validate_config()
        logger.info("Validating the paylod for the Snowflake connection")
        message = ""

        if not self.is_valid:
            username = self.config.get("username", None)
            password = self.config.get("password", None)
            account = self.config.get("account", None)
            role = self.config.get("role", None)
            warehouse = self.config.get("warehouse", None)
            database = self.config.get("database", None)
            schema = self.config.get("schema", None)
            key = self.config.get("key", None)

            if key:
                is_key_present = os.path.exists(key)
                if not is_key_present:
                    message = f"Private key file is not present. Will use password based authentication if password are supplied.{os.linesep}"
                    logger.info(message)
                    key = None

            if not username or not account:
                message = f"Invalid connection details. Username and account is required.{os.linesep}"
                self.is_valid = False
                logger.error(message)
            elif not password and not key:
                message = f"Invalid connection details. Either password or key is required.{os.linesep}"
                self.is_valid = False
                logger.error(message)
            else:
                self.is_valid = True

            if not role:
                message = f"{message}Role is not provided. Consider USE statement to switch from default role.{os.linesep}"

            if not warehouse:
                message = f"{message}Warehouse is not provided. Consider USE statement to switch from default warehouse.{os.linesep}"

            if not database:
                message = f"{message}Database is not provided. Consider USE statement to switch database or use fully qualified path.{os.linesep}"

            if not schema:
                message = f"{message}Schema is not provided. Consider USE statement to switch from default public schema or use fully qualified path.{os.linesep}"

            if key and password:
                message = f"{message}Private key and password both are present. Password will be consider to decrypt the key file.{os.linesep}"

            if self.is_valid:
                logger.info("Connection is valid")

                if message:
                    logger.info(message)

        return self.is_valid, message

    def create_uri(self):
        super().create_uri()
        logger.info("Call for creating the URI for snowflake")

        is_valid, message = self.validate_config()
        uri = None
        if is_valid:
            from snowflake.sqlalchemy import URL

            username = self.config.get("username", None)
            password = self.config.get("password", None)
            account = self.config.get("account", None)
            role = self.config.get("role", None)
            warehouse = self.config.get("warehouse", None)
            database = self.config.get("database", None)
            schema = self.config.get("schema", "public")
            key = self.config.get("key", None)

            if password:
                password = urlquote(password)

            if key:
                if not os.path.exists(key):
                    key = None

            conn_arg = {
                "account": account,
                "user": username
            }
            if database:
                conn_arg["database"] = database
            if schema and database:
                conn_arg["schema"] = schema
            if warehouse:
                conn_arg["warehouse"] = warehouse
            if role:
                conn_arg["role"] = role
            if not key and password:
                conn_arg["password"] = password

            uri = URL(**conn_arg)
            logger.info("URI created for Snowflake")
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

                key = self.config.get("key", None)
                password = self.config.get("password", None)

                if key:
                    if not os.path.exists(key):
                        key = None

                if password:
                    password = password.encode()

                if key:
                    with open(key, "rb") as c_key:
                        p_key = serialization.load_pem_private_key(
                            c_key.read(),
                            password=password,
                            backend=default_backend()
                        )

                    pkb = p_key.private_bytes(
                        encoding=serialization.Encoding.DER,
                        format=serialization.PrivateFormat.PKCS8,
                        encryption_algorithm=serialization.NoEncryption())
                    param["connect_args"] = {"private_key": pkb}

                if uri:
                    super().get_session(uri, param, description_encoding)
            else:
                raise ValueError(message)

        return self.session, is_valid, message
