#!/usr/bin/env python
# pylint: disable=unused-import
from .app import app
from .db import create_db_and_tables
from .endpoints.fabric import delete_fabric, get_fabric_by_fabric_name, get_fabrics, post_fabric, put_fabric
from .endpoints.login import post_login
from .endpoints.v1_configtemplate import get_v1_configtemplate_by_name
from .endpoints.v1_fm_about_version import get_v1_fm_about_version
from .endpoints.v1_fm_features import get_v1_fm_features
from .endpoints.v1_lan_fabric_rest_control_switches_overview import v1_lan_fabric_rest_control_switches_overview_by_fabric_name


@app.on_event("startup")
def on_startup():
    """
    App entry point
    """
    create_db_and_tables()
