# connector-factory

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI](https://img.shields.io/pypi/v/connector-factory.svg)](https://pypi.org/project/connector-factory)


Connector factory is used to manage/create connection with execute queries using the connection.
The concept of having single source to connect various sources and perform operations on top of it.


User need not to worry on the crafting the connection string and to identify the methods for the basic operations.
Connector factory supports DML / DDL executions and have support of Pandas DataFrame to create or replace existing tables.

Connector factory is wrapper on various sources and for database source it uses sqlalchemy for crafting the connection and supports below databases:

```bash
* Sqlite3
* PostgreSQl
* BigQuery (Upcomming)
* Snowflake
* MariaDB
* MySQL
* Redshift
* Salesforce
* S3Select
* Databricks
* Synapse
* DynamoDB
* IBM DB2
```

* Note: Only select operations are supported for Salesforce and S3Select and limited functionality. These are not managed by the usage of sqlalchemy.

* Note: Connector factory can be enhanced for all the sqlalchemy supported database.

* Note: DynamoDB is supported via PyDynao. Please check the features and limitations at [PyDynamoDB](https://github.com/passren/PyDynamoDB/wiki).

Connector factory also provide the facility to create the connections for Salesforce
using simple-saleforce python package. Only Select query is supported in Salesforce. For advance usage it exposes the Salesforce object (simple-saleforce python package) which can be used as per the requirements. Refer [simple-saleforce](https://pypi.org/project/simple-salesforce/) for more detail.

## Getting Started

```bash
pip install connector-factory
```

By default connector-factory is installed with only SQlite3 support only. For other support it can be installed using combinations of below flags
* postgres
* redshift
* snowflake
* mysql
* mariadb
* salesforce
* s3select
* databricks
* synapse
* db2
* dynamodb
* bigquery (upcomming)
* all (For all supported types)


### Using connector-factory
-----
```python
from connector_factory import ConnectorFactory
import tempfile

temp_dir = tempfile.gettempdir()
config = {
  "path": temp_dir,
  "database": "site.db"
  }
db = ConnectorFactory(connector_type="sqlite", config=config)

db.execute_sql(sql="create table test (id int PRIMARY KEY)")
db.execute_sql(sql="insert into test values (1)")
db.execute_sql(sql="insert into test values (2)")

rows = db.execute_sql(sql="select * from test")
if rows:
  print(rows)


df = db.get_df(sql="select * from test")
print(df)

db.execute_df(panda_df=df, table_name="copy_test", exist_action="replace")
# db.execute_df(panda_df=df, table_name=copy_test, exist_action="replace", chunk_size=100)
db.execute_sql(sql="insert into copy_test values (3)")
rows_copy = db.execute_sql(sql="select * from copy_test")
if rows_copy:
  print(rows_copy)
```

## Appendix
### Supported database type:
----
```
*   sqlite (default)
*   postgres
*   mysql
*   mariadb
*   snowflake
*   redshift
*   salesforce
*   s3select
*   databricks
*   synapse
*   db2
*   dynamodb
```

### Configuration parameters for sqlite:
-----
-----
```python
* connector_type: sqlite
* config = {
    "path": "<folder_path_where_sqlite_database_file_exist>",
    "database": "<name_of_sqlite_database_file>"
}
```
**Details:**
* path: (Optional)=> Default user home directory. Path to folder where flat sqlite database file is present.
* database (Required)=> .db is optional, if not present .db will attach to look for database flat file. If file not present will create the file.
-----

### Connection parameters for postgres:
-----
-----
```python
* connector_type: postgres
* config = {
    "username": "<postgres_user>",
    "password": "<user_password>",
    "host": "<host_of_postgres_service>",
    "port": "<port_of_postgres_service>",
    "database": "<name_of_database>"
}
```

**Details:**
* username: (Required)=> Name of user for connection.
* password (Required)=> Password of user.
* host: (Required)=> Host of PostgreSql service.
* port: (Optional)=> Default 5432. Port of PostgreSql service.
* database: (Optional)=> If provided will be used as default database in connection. If not then query should comply with fully qualified path to table.
-----

### Connection parameters for mysql:
-----
-----
```python
* connector_type: mysql
* config = {
    "username": "<mysql_user>",
    "password": "<user_password>",
    "host": "<host_of_mysql_service>",
    "port": "<port_of_mysql_service>",
    "database": "<name_of_database>"
}
```

**Details:**
* username: (Required)=> Name of user for connection.
* password (Required)=> Password of user.
* host: (Required)=> Host of MySQL service.
* port: (Optional)=> Default 3306. Port of MySQL service.
* database: (Optional)=> If provided will be used as default database in connection. If not then query should comply with fully qualified path to table.
-----

### Connection parameters for mariadb:
-----
-----
```python
* connector_type: mariadb
* config = {
    "username": "<mariadb_user>",
    "password": "<user_password>",
    "host": "<host_of_mariadb_service>",
    "port": "<port_of_mariadb_service>",
    "database": "<name_of_database>"
}
```

**Details:**
* username: (Required)=> Name of user for connection.
* password (Required)=> Password of user.
* host: (Required)=> Host of MariaDB service.
* port: (Optional)=> Default 3306. Port of MariaDB service.
* database: (Optional)=> If provided will be used as default database in connection. If not then query should comply with fully qualified path to table.
-----

### Connection parameters for snowflake:
-----
-----
```python
* connector_type: snowflake
* config = {
    "username": "<snowflake_user>",
    "password": "<user_password>",
    "role": "<snowflake_role>",
    "account": "<snowflake_account>",
    "warehouse": "<snowflake_warehouse>",
    "schema": "<snowflake_schema>",
    "database": "<name_of_database>",
    "key": "<private_key_path>"
}
```

**Details:**
* username: (Required)=> Name of user for connection.
* account: (Required)=> Snowflake account name.
* password (Optional)=> Password of user/private key. Required if private key is not provided.
* role: (Optional)=> If not provided user default role will be used. Consider USE statement to switch from default role.
* database: (Optional)=> If provided will be used as default database in connection. If not then query should comply with fully qualified path to table.
* warehouse: (Optional)=> If not provided user default warehouse will be used. Consider USE statement to switch from default warehouse.
* schema: (Optional)=> If not provided default public schema will be used. Consider USE statement to switch from default schema or fully qualified path to table. Ignored if database is not proivided.
* key: (Optional)=> Either Key or Password is required. If key is present and password is also present then password will be used to decrypt the key. If password is not given then consider the unencrypted key. We strongly recommended to use only encrypted key.
-----

### Connection parameters for redshift:
-----
-----
```python
* connector_type: redshift
* config = {
    "username": "<redshift_user>",
    "password": "<user_password>",
    "host": "<host_of_redshift_service>",
    "port": "<port_of_redshift_service>",
    "database": "<name_of_database>"
}
```

**Details:**
* username: (Required)=> Name of user for connection.
* password (Required)=> Password of user.
* host: (Required)=> Host of Redshift service.
* port: (Optional)=> Default 5469. Port of Redshift service.
* database: (Required)=> Name of database for connection.
-----

### Connection parameters for Salesforce:
-----
-----
```python
* connector_type: salesforce
* config = {
    "username": "<salesforce_user>",
    "password": "<user_password>",
    "domain": "<domain_of_salesforce_service>",
    "token": "<user_token_for_salesforce_service>"
}
```

**Details:**
* username: (Required)=> Name of user for connection.
* password (Required)=> Password of user.
* domain: (Required)=> Host of Salesforce service.
* token: (Required)=> User token for Salesforce service.
-----


### Connection parameters for S3select:
-----
-----
```python
* connector_type: s3select
* config = {
    "bucket": "<AWS_S3_bucket>",
    "file": "<Path_of_file_in_bucket>",
    "type": "<file_type>",
    "limit": "<limit_of_record_to_fetch>",
    "compression": "<compression_type>"
}
```

**Details:**
* bucket: (Required)=> Name of AWS S3 bucket to look for files for queries.
* type: (Required)=> Supported types is one of csv, json or parquet.
* file (Required)=> Full file path without bucket or prefix key to serach for similar files as per the type of files provided. First line is considered as header of file for csv. Example: if only prefix is provided like mypath/mydatafile and type is csv then all files named as mypath/mydatafile*.csv will be read.
* limit: (Optional)=> Commulative number of records to read from the file (multiple files).
* compression: (Optional)=> Supported types is one of GZIP, BZIP2 or NONE.
-----


### Connection parameters for Synapse:
-----
-----
```python
* connector_type: synapse
* config = {
    "username": "<synapse_user>",
    "password": "<user_password>",
    "host": "<hostname_of_synapse_service>",
    "port": "<port_of_synapse_service>",
    "database": "<database_name>",
    "driver": "<driver_to_connect_synapse_service>",
    "trust_certificate": "<trust_the_synapse_connection>",
    "authentication_with": "<authentication_type_of_synapse_service>",
    "connection_timeout": "<connection_timeout_to_synapse_service>"
}
```

**Details:**
* username: (Required)=> Name of user for connection.
* password (Required)=> Password of user.
* host: (Required)=> Host of Synapse service.
* port: (Optional)=> Port of Synapse service. Default to 1433
* database: (Required)=> Database name.
* driver: (Optional)=> Name of driver to use. Default to ODBC Driver 17 for SQL Server.
* trust_certificate: (Optional)=> Trust the connection with certificate. Default to no.
* authentication_with: (Optional)=> Default to None and not in use to authenticate with. If service principal or AD authenitication is used then pass appropriate value.
* connection_timeout: (Optional)=> Connection timeout. Default to 30.
-----


### Connection parameters for Databricks:
-----
-----
```python
* connector_type: databricks
* config = {
    "hostname": "<hostname_of_databricks_service>",
    "token": "<pat_token_of_databricks_as_password>",
    "http_path": "<path_of_warehouse_or_cluster>",
    "catalog": "<catalog_name_of_databricks>",
    "schema": "<schema_name_of_databricks>",
}
```

**Details:**
* hostname: (Required)=> Databricks hostname.
* token (Required)=> Pat token of user.
* http_path: (Required)=> Path of warehouse or cluster.
* catalog: (Required)=> Unity catalog name
* schema: (Required)=> Schema name under catalog.
-----


### Connection parameters for IBM DB2:
-----
-----
```python
* connector_type: db2
* config = {
    "username": "<hostname_of_databricks_service>",
    "password": "<pat_token_of_databricks_as_password>",
    "host": "<path_of_warehouse_or_cluster>",
    "port": "<catalog_name_of_databricks>",
    "database": "<schema_name_of_databricks>",
}
```

**Details:**
* username: (Required)=> Name of user for connection.
* password (Required)=> Password of user.
* host: (Required)=> Host of IBM DB2 Server.
* port: (Optional)=> Port of IBM DB2 Server. Default to 50000
* database: (Required)=> Database name.
-----


### Connection parameters for DynamoDB:
-----
-----
```python
* connector_type: dynamodb
* config = {
    "region": "<aws_region_of_dynamodb>"
}
```

**Details:**
* region: (Optional)=> AWS Region. Default is us-east-1
-----


### Development Setup

#### Using virtualenv

```bash
python3 -m venv venv
source env/bin/activate
pip install .[all]
```

### Contributing

1. Fork repo- https://github.com/shrivastava-v-ankit/connector-factory.git
2. Create your feature branch - `git checkout -b feature/name`
3. Install Python packages under all virtual environments of Python 3.8, 3.9, 3.10, 3.11
    * pip install .[all]
    * pip install coverage==7.2.3
    * pip install exceptiongroup==1.1.1
    * pip install pluggy==1.0.0
    * pip install pytest==7.3.0
    * pip install pytest-cov==4.0.0
    * pip install tomli==2.0.1
4. Run Python test (pytest)
    * For Python 3.8:
      ```python
      pytest -v --cov --cov-report=html:test-results/connection_factory_test/htmlcov.3.8 --cov-report=xml:test-results/connection_factory_test/coverage.3.8.xml --junitxml=test-results/connection_factory_test/results.3.8.xml
      ```
    * For Python 3.9:
      ```python
      pytest -v --cov --cov-report=html:test-results/connection_factory_test/htmlcov.3.9 --cov-report=xml:test-results/connection_factory_test/coverage.3.9.xml --junitxml=test-results/connection_factory_test/results.3.9.xml
      ```
    * For Python 3.10:
      ```python
      pytest -v --cov --cov-report=html:test-results/connection_factory_test/htmlcov.3.10 --cov-report=xml:test-results/connection_factory_test/coverage.3.10.xml --junitxml=test-results/connection_factory_test/results.3.10.xml
      ```
    * For Python 3.11:
      ```python
      pytest -v --cov --cov-report=html:test-results/connection_factory_test/htmlcov.3.11 --cov-report=xml:test-results/connection_factory_test/coverage.3.11.xml --junitxml=test-results/connection_factory_test/results.3.11.xml
      ```
5. Add Python test (pytest) and covrage report for new/changed feature generated under test-results/connection_factory_test/
6. Commit your changes - `git commit -am "Added name"`
7. Push to the branch - `git push origin feature/name`
8. Create a new pull request

