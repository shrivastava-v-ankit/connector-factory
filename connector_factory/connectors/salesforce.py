#!/usr/bin/env python3


import logging
import os
import pandas
from requests.exceptions import ConnectionError

from ..decorator import Decorator

logger = logging.getLogger(__name__)

# https://github.com/simple-salesforce/simple-salesforce
# https://intellipaat.com/community/7813/python-simple-salesforce-select-all-fields
# https://readthedocs.org/projects/simple-salesforce/downloads/pdf/latest/


class Salesforce(Decorator):
    def __init__(self, config: dict):
        super().__init__(config)
        self.is_valid = False

    def validate_config(self):
        super().validate_config()
        logger.info("Validating the paylod for the Salesforce connection")
        message = ""

        if not self.is_valid:
            username = self.config.get("username", None)
            password = self.config.get("password", None)
            domain = self.config.get("domain", None)
            token = self.config.get("token", None)

            if not username or not password or not domain or not token:
                message = f"Invalid connection details. Username, password, domain and token are required.{os.linesep}"
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
        logger.info(
            "Salesfore is not ORM so implementation with SQLAlchemy is not created")
        pass

    def get_session(self, uri: str, param: dict = {}, description_encoding: bool = False):
        is_valid = False
        message = None
        if not self.session:
            logger.info("Session is not created. Try to create a session")
            is_valid, message = self.validate_config()

            username = self.config.get("username", None)
            password = self.config.get("password", None)
            domain = self.config.get("domain", None)
            token = self.config.get("token", None)

            if is_valid:
                from simple_salesforce import Salesforce as SimpleSaleforce
                self.session = SimpleSaleforce(username=username,
                                               password=password,
                                               security_token=token,
                                               instance=domain)
            else:
                raise ValueError(message)

        logger.info(
            "Saleforce will return the object of Salesforce class from simple_salesforce pypi plugin")
        return self.session, is_valid, message

    def get_table_name(self, soql):
        sql_splits = soql.split(" ")

        soql_lst = []
        for val in sql_splits:
            if val:
                soql_lst.append(val)

        i = 0
        table = None
        for v in soql_lst:
            if "from" in v.lower():
                table = soql_lst[i + 1]
            i += 1

        return table

    def get_columns(self, soql):
        table = self.get_table_name(soql=soql)
        _module = getattr(self.session, table)
        desc = _module.describe()

        field_names = [field["name"] for field in desc["fields"]]
        columns = []

        soql_lower = soql.lower()
        _all = True

        if "FIELDS(CUSTOM)".lower() in soql_lower:
            _all = False

        for f in field_names:
            column = f

            if not _all and not f.endswith("__c"):
                column = None

            if column:
                columns.append(column)

        return columns

    def replace_columns(self, soql, columns):
        sql_splits = soql.split(" ")

        soql_lst = []
        for val in sql_splits:
            if val:
                soql_lst.append(val)

        i = 0
        for f in soql_lst:
            if "FIELDS(CUSTOM)".lower() in f.lower() or "FIELDS(ALL)".lower() in f.lower():
                soql_lst[i] = ", ".join(columns)
            i += 1
        return " ".join(soql_lst)

    def execute_df(self, panda_df: pandas.DataFrame, table_name: str, chunk_size: int = None, exist_action: str = "append"):
        # return super().execute_df(panda_df, table_name, chunk_size, exist_action)
        raise ValueError(f"Unsupported method for Salesforce")
        pass

    def execute_sql(self, sql: str):
        logger.info(f"Got SQL statement to execute: {sql}")
        logger.info("Only select queries can be executed")

        df = self.get_df(sql=sql)
        rows = df.to_records().tolist()
        return rows

    def get_df(self, sql: str, chunk_size: int = None):
        logger.info(f"Got SQL statement to execute: {sql}")
        logger.info("Only select queries can be executed")

        soql_lower = sql.lower()

        if soql_lower.startswith("select"):
            if "FIELDS(CUSTOM)".lower() in soql_lower or "FIELDS(ALL)".lower() in soql_lower:
                columns = self.get_columns(soql=sql)
                sql = self.replace_columns(soql=sql, columns=columns)

            message = None

            if not self.session:
                _, _, message = self.get_session(None)

            if not self.session:
                raise ValueError(message)

            df = None
            try:
                result = self.session.query_all(query=sql)
            except ConnectionError:
                # Try to handle the timeout with new connection.
                from simple_salesforce import Salesforce as SimpleSaleforce
                self.session = SimpleSaleforce(instance=self.session.sf_instance,
                                               session_id=self.session.session_id)
                # Attempt your request again here...
                result = self.session.query_all(query=sql)

            if result and "records" in result:
                df = pandas.DataFrame(result["records"])
                if "attributes" in df.columns:
                    df.drop(["attributes"], axis=1, inplace=True)
                df = pandas.json_normalize(df.to_dict(orient="records"))
                df = df[columns].copy(deep=True)

            return df

        raise ValueError(
            "Invalid sql statement. Only query is supported in Salesforce using select statement.")

    def destroy(self):
        pass
