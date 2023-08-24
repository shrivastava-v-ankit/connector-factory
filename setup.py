#!/usr/bin/env python

"""
Prerequesites -
  Python Packages:
    * setuptools
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


from setuptools import setup, find_packages
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
    "pandas==2.0.3"
]

dependencies_base = [
    "pytz==2023.3",
    "python-dateutil==2.8.2",
    "tzdata==2023.3",
    "numpy==1.24.4" if python_version in [
        "3.8"] else "numpy==1.25.2" if python_version in [
            "3.9", "3.10", "3.11"] else "numpy",
    "six==1.16.0"
]

rds_type = [
    # Database Abstraction Library
    "sqlalchemy==1.4.49"
]

dependencies_rds_type = [
    "greenlet==2.0.2"
]

aws = s3select = [
    # The AWS SDK for Python
    "boto3==1.28.22"
]

dependencies_aws = [
    "botocore==1.31.22",
    "jmespath==1.0.1",
    "s3transfer==0.6.1",
    "urllib3==1.26.16",
]

gcp = [
    # This library simplifies using Google’s various server-to-server authentication mechanisms to access Google APIs.
    "google-auth==2.22.0",
    # This library provides an httplib2 transport for google-auth.
    "google-auth-httplib2==0.1.0",
    # Google API Client Library for Python
    "google-api-python-client==2.96.0",
    # Google Secret Manager API API client library
    "google-cloud-secret-manager==2.16.3"
]


dependencies_gcp = [
    "cachetools==5.3.1",
    "pyasn1==0.5.0",
    "pyasn1-modules==0.3.0",
    "rsa==4.9",
    "urllib3==1.26.16",
    "six==1.16.0",
    "httplib2==0.22.0",
    "pyparsing==3.1.1",
    "python-dateutil==2.8.2",
    "protobuf==4.24.0",
    "packaging==23.1",
    "idna==3.4",
    "grpcio==1.56.2",
    "google-crc32c==1.5.0",
    "charset-normalizer==3.2.0",
    "certifi==2023.7.22",
    "requests==2.31.0",
    "proto-plus==1.22.3",
    "googleapis-common-protos==1.60.0",
    "google-resumable-media==2.5.0",
    "grpcio-status==1.56.2",
    "google-api-core==2.11.1",
    "google-cloud-core==2.3.3",
    "uritemplate==4.1.1",
    "grpc-google-iam-v1==0.12.6",
    "future==0.18.3"
]

bigquery = [
    # SQLAlchemy dialect for BigQuery
    "pybigquery==0.10.2" if python_version in [
        "3.8", "3.9"] else "pybigquery==0.5.0" if python_version in [
            "3.10", "3.11"] else "pybigquery"
]

dependencies_bigquery = [
    "future==0.18.3",
    "google-cloud-bigquery==3.11.4",
    "google-api-core==2.11.1",
    "python-dateutil==2.8.2",
    "google-resumable-media==2.5.0",
    "grpcio==1.56.2",
    "proto-plus==1.22.3",
    "protobuf==4.24.0",
    "google-cloud-core==2.3.3",
    "packaging==23.1",
    "requests==2.31.0",
    "greenlet==2.0.2",
    "google-auth==2.22.0",
    "googleapis-common-protos==1.60.0",
    "grpcio-status==1.56.2",
    "six==1.16.0",
    "certifi==2023.7.22",
    "idna==3.4",
    "urllib3==1.26.16",
    "charset-normalizer==3.2.0",
    "pyasn1-modules==0.3.0",
    "cachetools==5.3.1",
    "rsa==4.9",
    "pyasn1==0.5.0",
]

snowflake = [
    # Snowflake Connector Library
    "snowflake-connector-python==3.1.0",
    # Snowflake SQLAlchemy Dialect
    "snowflake-sqlalchemy==1.4.7",
    # cryptography is a package which provides cryptographic recipes and primitives.
    "cryptography==41.0.3"
]

dependencies_snowflake = [
    "pyjwt==2.8.0",
    "packaging==23.1",
    "filelock==3.12.2",
    "platformdirs==3.8.1",
    "urllib3==1.26.16",
    "pycryptodomex==3.18.0",
    "certifi==2023.7.22",
    "sortedcontainers==2.4.0",
    "charset-normalizer==3.2.0",
    "asn1crypto==1.5.1",
    "pyOpenSSL==23.2.0",
    "tomlkit==0.12.1",
    "idna==3.4",
    "requests==2.31.0",
    "oscrypto==1.3.0",
    "typing-extensions==4.7.1",
    "cffi==1.15.1"
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
    # Python HTTP for Humans.
    "requests==2.31.0"
]

dependencies_salesforce = [
    "pyjwt==2.8.0",
    "cryptography==41.0.3",
    "zeep==4.2.1",
    "requests==2.31.0",
    "charset-normalizer==3.2.0",
    "urllib3==1.26.16",
    "certifi==2023.7.22",
    "idna==3.4",
    "cffi==1.15.1",
    "platformdirs==3.8.1",
    "lxml==4.9.3",
    "requests-toolbelt==1.0.0",
    "requests-file==1.5.1",
    "isodate==0.6.1",
    "attrs==23.1.0",
    "pycparser==2.21",
    "six==1.16.0"
]


setups = []


extra_dependencies = {
    "sqlite": (rds_type + dependencies_rds_type),
    "snowflake": (rds_type + dependencies_rds_type + snowflake + dependencies_snowflake),
    "aws": (aws + dependencies_aws),
    "s3select": (aws + dependencies_aws),
    "postgres": (rds_type + dependencies_rds_type + postgres),
    "redshift": (rds_type + dependencies_rds_type + redshift),
    "mysql": (rds_type + dependencies_rds_type + mysql),
    "mariadb": (rds_type + dependencies_rds_type + mysql),
    "salesforce": (salesforce + dependencies_salesforce),
    "gcp": (gcp + dependencies_gcp),
    "bigquery": (gcp + dependencies_gcp + bigquery + dependencies_bigquery + rds_type + dependencies_rds_type),
    "all": (rds_type + dependencies_rds_type + snowflake + dependencies_snowflake + aws + dependencies_aws + postgres + redshift + mysql + salesforce + dependencies_salesforce + gcp + dependencies_gcp + bigquery + dependencies_bigquery)
}

ir = (base + dependencies_base + extra_dependencies["sqlite"])
install_requires = ir


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
        extras_require=extra_dependencies,
        license="MIT",
        python_requires=">=3.8, <3.12",
        platforms="any",
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
