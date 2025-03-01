#!/usr/bin/env python
# pylint: disable=unused-import
from .app import app
from .v1.endpoints.configtemplate import get_v1_configtemplate_by_name
from .v1.endpoints.fabric import delete_fabric, get_fabric_by_fabric_name, get_fabrics, post_fabric, put_fabric
from .v1.endpoints.fm_about_version import get_v1_fm_about_version
from .v1.endpoints.fm_features import get_v1_fm_features
from .v1.endpoints.lan_fabric_rest_control_switches_overview import v1_lan_fabric_rest_control_switches_overview_by_fabric_name
from .v1.endpoints.login import post_login
from .v2.endpoints.fabric import post_fabric
