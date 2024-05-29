#!/usr/bin/env python

"""
Prerequesites -
  Python Packages:
    * setuptools
    * wheel
    * GitPython
  System Packages:
    * make
    * Python 3
Commands: python setup.py [bdist_wheel / [sdist [--format=[gztar][,tar]]]
Ex:
  * python setup.py bdist_wheel
  * python setup.py sdist
  * python setup.py sdist --format=gztar
  * python setup.py sdist --format=tar
  * python setup.py sdist --format=gztar,tar
  * python setup.py sdist --format=gztar
  * python setup.py bdist_wheel sdist --format=gztar,tar
"""

"""
distutils/setuptools install script.
"""


from setuptools import setup
from setuptools import find_packages
from setuptools import Command
from textwrap import wrap
import traceback
import shutil
import re
import os
import sys
__NAME__ = "connector-factory"

ROOT = os.path.dirname(os.path.abspath(__file__))
VERSION_FILE = os.path.join(ROOT, __NAME__.replace("-", "_"), ".version")
VERSION_RE = re.compile(r'''__version__ = ['"]([0-9.]+)['"]''')
python_version = f"{sys.version_info[0]}.{sys.version_info[1]}"

base = [
    # Powerful data structures for data analysis, time series, and statistics
    "pandas==2.0.3",
    # Database Abstraction Library
    "sqlalchemy==1.4.49",
    "greenlet==2.0.2",
    "numpy==1.24.4" if python_version in [
        "3.8"] else "numpy==1.25.2" if python_version in [
            "3.9", "3.10", "3.11"] else "numpy",
    "python-dateutil==2.8.2",
    "pytz==2023.3",
    "six==1.16.0",
    "tzdata==2023.3"
]

aws = s3select = [
    # The AWS SDK for Python
    "boto3==1.28.22",
    "botocore==1.31.22",
    "jmespath==1.0.1",
    "python-dateutil==2.8.2",
    "s3transfer==0.6.1",
    "six==1.16.0",
    "urllib3==1.26.16"
]

gcp = [
    # This library simplifies using Google’s various server-to-server authentication mechanisms to access Google APIs.
    "google-auth==2.22.0",
    # This library provides an httplib2 transport for google-auth.
    "google-auth-httplib2==0.1.0",
    # Google API Client Library for Python
    "google-api-python-client==2.96.0",
    # Google Secret Manager API API client library
    "google-cloud-secret-manager==2.16.3",
    "cachetools==5.3.1",
    "certifi==2023.7.22",
    "charset-normalizer==3.2.0",
    "google-api-core==2.11.1",
    "googleapis-common-protos==1.60.0",
    "grpc-google-iam-v1==0.12.6",
    "grpcio==1.56.2",
    "grpcio-status==1.56.2",
    "httplib2==0.22.0",
    "idna==3.4",
    "proto-plus==1.22.3",
    "protobuf==4.24.0",
    "pyasn1==0.5.0",
    "pyasn1-modules==0.3.0",
    "pyparsing==3.1.1",
    "requests==2.31.0",
    "rsa==4.9",
    "six==1.16.0",
    "uritemplate==4.1.1",
    "urllib3==1.26.16"
]

bigquery = [
    # SQLAlchemy dialect for BigQuery
    "pybigquery==0.10.2" if python_version in [
        "3.8", "3.9"] else "pybigquery==0.5.0" if python_version in [
            "3.10", "3.11"] else "pybigquery",
    "sqlalchemy==1.4.49",
    "cachetools==5.3.1",
    "certifi==2023.7.22",
    "charset-normalizer==3.2.0",
    "future==0.18.3",
    "google-api-core==2.11.1",
    "google-auth==2.22.0",
    "google-cloud-bigquery==3.11.4",
    "google-cloud-core==2.3.3",
    "google-resumable-media==2.5.0",
    "googleapis-common-protos==1.60.0",
    "google-crc32c==1.5.0",
    "greenlet==2.0.2",
    "grpcio==1.56.2",
    "grpcio-status==1.56.2",
    "idna==3.4",
    "packaging==23.1",
    "proto-plus==1.22.3",
    "protobuf==4.24.0",
    "pyasn1==0.5.0",
    "pyasn1-modules==0.3.0",
    "python-dateutil==2.8.2",
    "requests==2.31.0",
    "rsa==4.9",
    "six==1.16.0",
    "typing-extensions==4.7.1",
    "urllib3==1.26.16"
]

snowflake = [
    # Snowflake Connector Library
    "snowflake-connector-python==3.1.0",
    # Snowflake SQLAlchemy Dialect
    "snowflake-sqlalchemy==1.4.7",
    "pyjwt==2.8.0",
    "sqlalchemy==1.4.49",
    "asn1crypto==1.5.1",
    "certifi==2023.7.22",
    "cffi==1.15.1",
    "charset-normalizer==3.2.0",
    "cryptography==41.0.3",
    "filelock==3.12.2",
    "greenlet==2.0.2",
    "idna==3.4",
    "oscrypto==1.3.0",
    "packaging==23.1",
    "platformdirs==3.8.1",
    "pyOpenSSL==23.2.0",
    "pycparser==2.21",
    "pycryptodomex==3.18.0",
    "pyjwt==2.8.0",
    "requests==2.31.0",
    "sortedcontainers==2.4.0",
    "tomlkit==0.12.1",
    "typing-extensions==4.7.1",
    "urllib3==1.26.16"
]

redshift = postgres = [
    # PostgreSQL interface library.
    "psycopg2-binary==2.9.7"
]

mysql = [
    # Pure Python MySQL Driver
    "pymysql==1.1.0"
]

salesforce = [
    # A basic Salesforce.com REST API client.
    "simple-salesforce==1.12.4",
    "pyjwt==2.8.0",
    "attrs==23.1.0",
    "certifi==2023.7.22",
    "cffi==1.15.1",
    "charset-normalizer==3.2.0",
    "cryptography==41.0.3",
    "idna==3.4",
    "isodate==0.6.1",
    "lxml==4.9.3",
    "platformdirs==3.8.1",
    "pycparser==2.21",
    "pytz==2023.3",
    "requests==2.31.0",
    "requests-file==1.5.1",
    "requests-toolbelt==1.0.0",
    "six==1.16.0",
    "urllib3==1.26.16",
    "zeep==4.2.1"
]

databricks = [
    "databricks-sql-connector==2.9.6",
    "certifi==2023.7.22",
    "sqlalchemy==1.4.49",
    "charset-normalizer==3.2.0",
    "et-xmlfile==1.1.0",
    "greenlet==2.0.2",
    "idna==3.4",
    "lz4==4.3.3",
    "numpy==1.24.4" if python_version in [
        "3.8"] else "numpy==1.25.2" if python_version in [
            "3.9", "3.10", "3.11"] else "numpy",
    "oauthlib==3.2.2",
    "openpyxl==3.1.2",
    "pandas==2.0.3",
    "pyarrow==14.0.2",
    "python-dateutil==2.8.2",
    "pytz==2023.3",
    "six==1.16.0",
    "requests==2.31.0",
    "typing-extensions==4.7.1",
    "tzdata==2023.3",
    "urllib3==1.26.16",
    "thrift==0.16.0"
]

synapse = [
    "pyodbc==5.1.0"
]

db2 = [
    "ibm-db-sa==0.4.0",
    "ibm_db==3.2.3",
    "sqlalchemy==1.4.49",
    "greenlet==2.0.2",
    "typing-extensions==4.7.1",
]

dynamodb = [
    "PyDynamoDB==0.5.7",
    "boto3==1.28.22",
    "botocore==1.31.22",
    "jmespath==1.0.1",
    "pyparsing==3.1.1",
    "python-dateutil==2.8.2",
    "s3transfer==0.6.1",
    "six==1.16.0",
    "tenacity==8.3.0",
    "urllib3==1.26.16"
]


setups = [
    'gitpython',
    'setuptools',
    'wheel'
]


extras = {
    "snowflake": snowflake,
    "aws": aws,
    "s3select": aws,
    "postgres": postgres,
    "redshift": redshift,
    "mysql": mysql,
    "mariadb": mysql,
    "salesforce": salesforce,
    "databricks": databricks,
    "gcp": gcp,
    "bigquery": (gcp + bigquery),
    "synapse": synapse,
    "db2": db2,
    "dynamodb": dynamodb,
    "all": (snowflake + aws + postgres + redshift + mysql + salesforce + gcp + bigquery + databricks + synapse + db2)
}

install_requires = base


def delete(path):
    if os.path.exists(path=path):
        try:
            if os.path.isfile(path=path):
                os.remove(path=path)
            else:
                shutil.rmtree(path=path)
        except:
            pass


def write_version(version, sha, filename):
    text = f"__version__ = '{version}'\n__REVESION__ = '{sha}'"
    with open(file=filename, mode="w") as file:
        file.write(text)


def get_version(filename):
    version = "1.0.0"  # Adding default version

    # This block is for reading the version from foundry distribution
    if os.path.exists(path=filename):
        contents = None
        with open(file=filename, mode="r") as file:
            contents = file.read()
            version = VERSION_RE.search(contents).group(1)
            return version

    # If file not found. Then may be local or want to get the version
    version_python_file = os.path.join(ROOT, "version.py")
    if os.path.exists(path=version_python_file):
        import version as ver
        version = ver.version

        sha = ""
        try:
            import git
            repo = git.Repo(path=".", search_parent_directories=True)
            sha = repo.head.commit.hexsha
            sha = repo.git.rev_parse(sha, short=6)
        except ImportError:
            print(f"Import error on git, can be ignored for build")
            pass
        except Exception as exception:
            print(str(exception))
            traceback.print_tb(exception.__traceback__)
            pass
        write_version(version=version, sha=sha, filename=filename)
    return version


with open("README.md", "r") as f:
    long_description = f.read()


class List_Extras(Command):
    """
    List all available extras
    Registered as cmdclass in setup() so it can be called with ``python setup.py list_extras``.
    """

    description = "List available extras"
    user_options = []

    def initialize_options(self):
        """Set default values for options."""

    def finalize_options(self):
        """Set final values for options."""

    def run(self):
        """List extras."""
        print("\n".join(wrap(", ".join(extras.keys()), 100)))


def do_setup():
    setup(
        name=__NAME__,
        version=get_version(filename=VERSION_FILE),
        description="Connector Factory;",
        long_description=long_description,
        long_description_content_type="text/markdown",
        keywords=["python", "os independent", "database", "sqlalchemy",
                  "sqlite3", "sqlite", "postgres", "mysql", "maridb",
                  "snowflake", "bigquery", "gcp", "aws", "s3select", "salesforce"],
        author="Ankit Shrivastava",
        url="https://github.com/shrivastava-v-ankit/connector-factory",
        packages=find_packages(include=[__NAME__.replace("-", "_")]),
        include_package_data=True,
        setup_requires=setups,
        install_requires=install_requires,
        extras_require=extras,
        license="MIT",
        python_requires=">=3.8, <3.12",
        platforms="any",
        cmdclass={
            'list_extras': List_Extras,
        },
        project_urls={
            "Source": "https://github.com/shrivastava-v-ankit/connector-factory/",
            "Tracker": "https://github.com/shrivastava-v-ankit/connector-factory/issues",
        },
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Environment :: Web Environment",
            "Intended Audience :: Developers",
            "Natural Language :: English",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "Topic :: Software Development :: Version Control :: Git",
        ],
    )


if __name__ == "__main__":
    do_setup()

    if "sdist" in sys.argv or "bdist_wheel" in sys.argv:
        egg_info = os.path.join(ROOT, __NAME__.replace("-", "_") + ".egg-info")
        delete(path=egg_info)
        eggs = os.path.join(ROOT, ".eggs")
        delete(path=eggs)
        delete(path=VERSION_FILE)
        build_dir = os.path.join(ROOT, "build")
        delete(path=build_dir)
