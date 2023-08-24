#!/usr/bin/env python

import pytest
import os
import tempfile
from connector_factory import ConnectorFactory
from connector_factory.common.common import Common


def test_database_factory():

    temp_dir = tempfile.gettempdir()

    db_file = os.path.join(temp_dir, "test_db.db")

    os.remove(db_file) if os.path.exists(db_file) else None
    config = {
        "database": "test_db",
        "path": temp_dir
    }

    db = ConnectorFactory(connector_type="sqlite", config=config)
    db.create_session()

    db.execute_sql(sql="create table test (id int PRIMARY KEY)")
    db.execute_sql(sql="insert into test values (1)")
    db.execute_sql(sql="insert into test values (2)")

    assert os.path.exists(db_file) == 1

    rows = db.execute_sql(sql="select * from test")
    assert rows == [(1,), (2,)]

    df = db.get_df(sql="select * from test")
    assert df.values.tolist() == [[1], [2]]

    db.execute_df(panda_df=df, table_name="copy_test", exist_action="replace")
    db.execute_sql(sql="insert into copy_test values (3)")
    rows_copy = db.execute_sql(sql="select * from copy_test")
    assert rows_copy == [(1,), (2,), (3,)]

    dict1 = {"name": "myname", "type": "myposition"}
    dict2 = Common.normaize_connection_dict(
        connection_dict=dict1, is_to_upper=True)
    assert dict2 == {"NAME": "myname", "TYPE": "myposition"}

    dict3 = Common.normaize_connection_dict(connection_dict=dict2)
    assert dict3 == dict1


def test_error_database_factory():
    temp_dir = tempfile.gettempdir()

    db_file = os.path.join(temp_dir, "test_error.db")

    os.remove(db_file) if os.path.exists(db_file) else None
    config = {
        "database": "test_error",
        "path": temp_dir
    }
    db = ConnectorFactory(connector_type="sqlite", config=config)
    db.create_session()

    db.execute_sql(sql="create table test (id int PRIMARY KEY)")

    try:
        db.execute_sql(sql="insert into test values (asd)")
    except Exception as e:
        assert "no such column: asd" in str(e)

    db2 = ConnectorFactory(connector_type="myengine", config=config)
    error_str = db2.create_session()
    assert error_str.startswith(
        "Invalid connection type : myengine. Valid type is anyone from")

    db_file = os.path.join(temp_dir, "test_error.db")
    os.remove(db_file) if os.path.exists(db_file) else None

    config = {
        "database": "test_error",
        "path": temp_dir,
        "password": "y@pwd"
    }
    db3 = ConnectorFactory(connector_type="sqlite", config=config)
    db3.create_session()
    db3.execute_sql(sql="create table test (id int PRIMARY KEY)")
    db3.execute_sql(sql="insert into test values (1)")
    db3.execute_sql(sql="insert into test values (2)")

    assert os.path.exists(db_file) == 1
