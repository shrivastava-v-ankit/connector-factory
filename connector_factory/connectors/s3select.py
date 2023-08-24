#!/usr/bin/env python3


import logging
import pandas
import os
import io
from pathlib import Path
import botocore
import json
from ..decorator import Decorator

logger = logging.getLogger(__name__)


class S3Select(Decorator):
    def __init__(self, config: dict):
        super().__init__(config)
        self.is_valid = False
        self.aws = None
        self.aws_session = None
        self.files = []

    def validate_config(self):
        super().validate_config()
        logger.info("Validating the paylod for the Redshift connection")
        message = ""

        if not self.is_valid:
            import botocore

            bucket = self.config.get("bucket", None)
            file = self.config.get("file", None)
            file_type = self.config.get("type", None)
            compression = self.config.get("compression", None)
            record_delimiter = self.config.get("record_delimiter", None)
            field_delimiter = self.config.get("field_delimiter", None)

            if not bucket or not file or not file_type:
                message = f"Invalid connection details. file, password and file_type are required.{os.linesep}"
                self.is_valid = False
                logger.error(message)
            else:
                self.is_valid = True

            if file_type.lower() not in ["json", "csv", "parquet"]:
                message = f"Invalid file type, valid values are JSON, CSV or Parquet.{os.linesep}"
                self.is_valid = False
                logger.error(message)

            if not compression:
                pass
            elif compression and compression.upper() not in ["BZIP2", "GZIP", "NONE"]:
                message = f"Invalid compression type, valid values are BZIP2 or GZIP.{os.linesep}"
                self.is_valid = False
                logger.error(message)

            if not compression:
                message = f"{message}Compression type is not provided. Will not use any compression.{os.linesep}"

            if not record_delimiter:
                message = f"{message}Record delimiter is not provided. Default '\n' will be used.{os.linesep}"

            if not field_delimiter:
                message = f"{message}Field_delimiter is not provided. Default ',' will be used.{os.linesep}"

            if self.is_valid:
                logger.info("Connection is valid")

                if message:
                    logger.info(message)

        return self.is_valid, message

    def create_uri(self):
        raise ValueError(f"Unsupported method for AWS")

    def validate_files(self):
        bucket = self.config.get("bucket", None)
        file = self.config.get("file", None)
        file_type = self.config.get("type", None)

        suffix = Path(file).suffix
        if suffix:
            try:
                self.session.head_object(Bucket=bucket, Key=file)

                # self.session.Object(bucket, file).load()
                self.files.append(f"{file}")
                self.is_valid = True
                message = ""
            except botocore.exceptions.ClientError as e:
                self.is_valid = False
                if e.response['Error']['Code'] == "404":
                    # The key does not exist.
                    message = f"File '{file}' not found in AWS S3 '{bucket}' under region \'{self.config.get('region', 'us-east-1')}\'"
                elif e.response['Error']['Code'] == 403:
                    # Unauthorized, including invalid bucket
                    message = f"Unauthorized access"
                else:
                    # Something else has gone wrong.
                    message = "Something goes wrong while looking for the file to query."
                logger.error(message)
        else:
            file_list = []
            files_in_folder = self.session.list_objects_v2(Bucket=bucket,
                                                           Prefix=file)
            for content in files_in_folder.get('Contents', []):
                key = content.get("Key")
                suffix = Path(key).suffix.lower()
                if suffix in [f".{file_type.lower()}"]:
                    logger.info(
                        f"File found for the S3Select as {key}")
                    file_list.append(key)

            if not file_list:
                self.is_valid = False
                message = f"File(s) '{file}' not found in AWS S3 '{bucket}' under region \'{self.config.get('region', 'us-east-1')}\'"
            else:
                self.files = file_list

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
                from .aws import Aws
                self.aws = Aws(self.config)
                self.aws_session, is_valid, message = self.aws.get_session()
                self.session = self.aws_session.client("s3")

                self.validate_files()

        logger.info("S3Select will return the object of boto3 S3 client")
        return self.session, is_valid, message

    def execute_df(self, panda_df: pandas.DataFrame, table_name: str, chunk_size: int = None, exist_action: str = "append"):
        raise ValueError(f"Unsupported method for S3Select")

    def execute_sql(self, sql: str = None):
        logger.info(f"Got SQL statement to execute: {sql}")
        logger.info("Only select queries can be executed")

        df = self.get_df(sql=None)
        rows = df.to_records().tolist()

        return rows

    def get_df(self, sql: str = None, chunk_size: int = None):
        bucket = self.config.get("bucket", None)
        # file = self.config.get("file", None)
        file_type = self.config.get("type", None)
        compression = self.config.get("compression", "NONE")
        compression = compression.upper()
        record_delimiter = self.config.get("record_delimiter", "\n")
        field_delimiter = self.config.get("field_delimiter", ",")
        limit = self.config.get("limit", None)

        limit_str = ""
        if limit:
            limit_str = f"LIMIT {limit}"

        # specify the SQL query to select a random sample of data from the file
        query = f"SELECT * FROM S3Object {limit_str}"
        if file_type.lower() == "csv":
            select_object_content_config = {
                "InputSerialization": {
                    "CSV": {
                        "FileHeaderInfo": "None",
                        "RecordDelimiter": record_delimiter,
                        "FieldDelimiter": field_delimiter
                    },
                    "CompressionType": compression
                },
                "OutputSerialization": {
                    "CSV": {
                        "RecordDelimiter": record_delimiter,
                        "FieldDelimiter": field_delimiter
                    }
                }
            }
        elif file_type.lower() == "json":
            select_object_content_config = {
                "InputSerialization": {
                    "JSON": {
                        "Type": "DOCUMENT"
                    },
                    "CompressionType": compression
                },
                "OutputSerialization": {
                    "JSON": {
                        "RecordDelimiter": ","
                    }
                }
            }
        elif file_type.lower() == "parquet":
            select_object_content_config = {
                "InputSerialization": {
                    "Parquet": {},
                    "CompressionType": compression
                },
                "OutputSerialization": {
                    "JSON": {
                        "RecordDelimiter": ","
                    }
                }
            }
        else:
            raise ValueError(
                "Invalid file type, Valid values if CSV, JSON or Parquet")

        df_list = []
        total_row_count = 0
        check_limit = False

        if limit:
            check_limit = True

        for file in self.files:
            header = 0
            end_event_received = False

            if not check_limit or total_row_count < limit:
                # Response with data
                response = self.session.select_object_content(
                    Bucket=bucket,
                    Key=file,
                    Expression=query,
                    ExpressionType="SQL",
                    InputSerialization=select_object_content_config['InputSerialization'],
                    OutputSerialization=select_object_content_config['OutputSerialization']
                )

                records = ""
                for event in response['Payload']:
                    if 'Records' in event:
                        records += event['Records']['Payload'].decode("utf-8")
                    # elif 'Stats' in event:
                    #     statsDetails = event['Stats']['Details']
                    #     print("Stats details bytesScanned: ")
                    #     print(statsDetails['BytesScanned'])
                    #     print("Stats details bytesProcessed: ")
                    #     print(statsDetails['BytesProcessed'])
                    #     print("Stats details bytesReturned: ")
                    #     print(statsDetails['BytesReturned'])
                    # elif 'Progress' in event:
                    #     print(event['Progress']['Details'])
                    # End event indicates that the request finished successfully
                    elif 'End' in event:
                        # print('Result is complete')
                        end_event_received = True

                if not end_event_received:
                    raise Exception(
                        "End event not received, request incomplete.")

                if file_type.lower() in ["json", "parquet"]:
                    if records.endswith(","):
                        records = records[:-1]

                    if file_type.lower() in ["parquet"]:
                        records = f"[{records}]"

                    records = json.loads(records)
                    new_records = []

                    if file_type.lower() in ["parquet"]:
                        new_records = records
                    else:
                        for k, v in records.items():
                            new_records += v

                    df_tmp = pandas.read_json(
                        json.dumps(new_records)).reset_index(drop=True)
                elif file_type.lower() in ["csv"]:
                    df_tmp = pandas.read_csv(io.StringIO(records),
                                             header=header).reset_index(drop=True)

                if check_limit:
                    total_row_count += len(df_tmp)

                    # check total row count against threshold
                    if total_row_count > limit:
                        rows_to_extract = total_row_count - limit
                        df_tmp = df_tmp.head(len(df_tmp) - rows_to_extract)

                df_list.append(df_tmp)

        df = pandas.concat(df_list, ignore_index=True).reset_index(drop=True)
        return df

    def destroy(self):
        try:
            self.session.close()
        except Exception as err:
            message = f"Failed to close connection"
            logger.error(message)
