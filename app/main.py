#!/usr/bin/env python
# pylint: disable=unused-import
from .app import app
from .db import create_db_and_tables
from .endpoints.fabric import delete_fabric, get_fabric_by_fabric_name, get_fabrics, post_fabric, put_fabric


@app.on_event("startup")
def on_startup():
    """
    App entry point
    """
    create_db_and_tables()
