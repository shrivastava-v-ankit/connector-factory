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
    "pandas<=2.2.2",
    # Database Abstraction Library
    "sqlalchemy<=2.0.31",
    "greenlet<=3.0.3",
    "numpy<=2.0.0",
    "python-dateutil<=2.9.0",
    "pytz<=2024.1",
    "six<=1.16.0",
    "tzdata<=2024.1",
    "typing-extensions<=4.12.2"
]

aws = s3select = [
    # The AWS SDK for Python
    "boto3<=1.34.137",
    "botocore<=1.34.137",
    "jmespath<=1.0.1",
    "s3transfer<=0.10.2",
    "urllib3<=1.26.19"
]

# gcp = [
#     # This library simplifies using Google’s various server-to-server authentication mechanisms to access Google APIs.
#     "google-auth",
#     # This library provides an httplib2 transport for google-auth.
#     "google-auth-httplib2",
#     # Google API Client Library for Python
#     "google-api-python-client",
#     # Google Secret Manager API API client library
#     "google-cloud-secret-manager",
#     "cachetools",
#     "certifi<=2024.6.2",
#     "charset-normalizer<=3.3.2",
#     "google-api-core",
#     "googleapis-common-protos",
#     "grpc-google-iam-v1",
#     "grpcio",
#     "grpcio-status",
#     "httplib2",
#     "idna<=3.7",<=2.32.3
#     "proto-plus",
#     "protobuf",
#     "pyasn1",
#     "pyasn1-modules",
#     "pyparsing<=3.1.2",
#     "requests<=2.32.3",
#     "rsa",
#     "uritemplate",
#     "urllib3<=1.26.19"
# ]

# bigquery = [
#     # SQLAlchemy dialect for BigQuery
#     "pybigquery==0.10.2" if python_version in [
#         "3.8", "3.9"] else "pybigquery" if python_version in [
#             "3.10", "3.11"] else "pybigquery",
#     "cachetools",
#     "certifi<=2024.6.2",
#     "charset-normalizer<=3.3.2",
#     "future",
#     "google-api-core",
#     "google-auth",
#     "google-cloud-bigquery",
#     "google-cloud-core",
#     "google-resumable-media",
#     "googleapis-common-protos",
#     "google-crc32c",
#     "grpcio",
#     "grpcio-status",
#     "idna<=3.7",
#     "packaging<=24.1",
#     "proto-plus",<=2.32.3
#     "protobuf",
#     "pyasn1",
#     "pyasn1-modules",
#     "requests<=2.32.3",
#     "rsa",
#     "urllib3<=1.26.19"
# ]

snowflake = [
    # Snowflake Connector Library
    "snowflake-connector-python<=3.11.0",
    # Snowflake SQLAlchemy Dialect
    "snowflake-sqlalchemy<=1.5.3",
    "pyjwt<=2.8.0",
    "asn1crypto<=1.5.1",
    "certifi<=2024.6.2",
    "cffi<=1.16.0",
    "charset-normalizer<=3.3.2",
    "cryptography<=42.0.8",
    "filelock<=3.15.4",
    "idna<=3.7",
    "oscrypto<=1.3.0",
    "packaging<=24.1",
    "platformdirs<=4.2.2",
    "pyOpenSSL<=24.1.0",
    "pycparser<=2.22",
    "pycryptodomex<=3.20.0",
    "requests<=2.32.3",
    "sortedcontainers<=2.4.0",
    "tomlkit<=0.12.5",
    "urllib3<=1.26.19"
]

redshift = postgres = [
    # PostgreSQL interface library.
    "psycopg2-binary<=2.9.9"
]

mysql = [
    # Pure Python MySQL Driver
    "pymysql<=1.1.1"
]

salesforce = [
    # A basic Salesforce.com REST API client.
    "simple-salesforce<=1.12.6",
    "pyjwt<=2.8.0",
    "attrs<=23.2.0",
    "certifi<=2024.6.2",
    "cffi<=1.16.0",
    "charset-normalizer<=3.3.2",
    "cryptography<=42.0.8",
    "idna<=3.7",
    "isodate<=0.6.1",
    "lxml<=5.2.2",
    "more-itertools<=10.3.0",
    "platformdirs<=4.2.2",
    "pycparser<=2.22",
    "requests<=2.32.3",
    "requests-file<=2.1.0",
    "requests-toolbelt<=1.0.0",
    "urllib3<=1.26.19",
    "zeep<=4.2.1"
]

databricks = [
    "databricks-sql-connector<=3.2.0",
    "certifi<=2024.6.2",
    "charset-normalizer<=3.3.2",
    "et-xmlfile<=1.1.0",
    "idna<=3.7",
    "lz4<=4.3.3",
    "oauthlib<=3.2.2",
    "openpyxl<=3.1.5",
    "pyarrow<=16.1.0",
    "requests<=2.32.3",
    "urllib3<=1.26.19",
    "thrift<=0.20.0"
]

synapse = [
    "pyodbc<=5.1.0"
]

db2 = [
    "ibm-db-sa<=0.4.0",
    "ibm_db<=3.2.3"
]

dynamodb = [
    "PyDynamoDB<=0.6.1",
    "boto3<=1.34.137",
    "botocore<=1.34.137",
    "jmespath<=1.0.1",
    "pyparsing<=3.1.2",
    "s3transfer<=0.10.2",
    "tenacity<=8.4.2",
    "urllib3<=1.26.19"
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
    "synapse": synapse,
    "db2": db2,
    "dynamodb": dynamodb,
    "all": (snowflake + aws + postgres + redshift + mysql + salesforce + databricks + synapse + db2)
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
                  "snowflake", "aws", "s3select", "salesforce"],
        author="Ankit Shrivastava",
        url="https://github.com/shrivastava-v-ankit/connector-factory",
        packages=find_packages(include=[__NAME__.replace("-", "_")]),
        include_package_data=True,
        setup_requires=setups,
        install_requires=install_requires,
        extras_require=extras,
        license="MIT",
        python_requires=">3.8, <3.13",
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
