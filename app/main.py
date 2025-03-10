#!/usr/bin/env python
# pylint: disable=unused-import
from .app import app
from .v1.endpoints.configtemplate import get_v1_configtemplate_by_name
from .v1.endpoints.fabric import v1_delete_fabric, v1_get_fabric_by_fabric_name, v1_get_fabrics, v1_post_fabric, v1_put_fabric
from .v1.endpoints.fm_about_version import get_v1_fm_about_version
from .v1.endpoints.fm_features import get_v1_fm_features
from .v1.endpoints.inventory import v1_get_switches_by_fabric_name
from .v1.endpoints.lan_fabric.rest_control_switches_fabric_name import v1_get_fabric_name_by_switch_serial_number
from .v1.endpoints.lan_fabric.rest_control_switches_overview import v1_lan_fabric_rest_control_switches_overview_by_fabric_name
from .v1.endpoints.login import post_login
from .v2.endpoints.fabric import v2_delete_fabric, v2_get_fabric_by_fabric_name, v2_get_fabrics, v2_post_fabric, v2_put_fabric
