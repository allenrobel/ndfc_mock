#!/usr/bin/env python
# pylint: disable=unused-import
from .app import app
from .v1.endpoints.configtemplate.rest.config.templates import config_template_by_name
from .v1.endpoints.fabric import v1_post_fabric, v1_put_fabric
from .v1.endpoints.fm_about_version import get_v1_fm_about_version
from .v1.endpoints.fm_features import get_v1_fm_features
from .v1.endpoints.lan_fabric.rest.control.fabrics import fabric_delete, fabric_get, fabrics_get
from .v1.endpoints.lan_fabric.rest.control.fabrics.inventory import v1_get_inventory_switches_by_fabric, v1_post_inventory_discover
from .v1.endpoints.lan_fabric.rest.control.switches import fabric_name, overview, roles
from .v1.endpoints.lan_fabric.rest.control.switches.fabric_name import v1_get_fabric_name_by_switch_serial_number
from .v1.endpoints.lan_fabric.rest.control.switches.overview import v1_lan_fabric_rest_control_switches_overview_by_fabric_name
from .v1.endpoints.login import post_login
from .v2.endpoints.fabric import v2_delete_fabric, v2_get_fabric_by_fabric_name, v2_get_fabrics, v2_post_fabric, v2_put_fabric

app.include_router(fabric_delete.router, tags=["Fabrics (v1)"])
app.include_router(fabric_get.router, tags=["Fabrics (v1)"])
app.include_router(fabrics_get.router, tags=["Fabrics (v1)"])
app.include_router(roles.router, tags=["Inventory (v1)"])
app.include_router(fabric_name.router, tags=["Switches (v1)"])
app.include_router(overview.router, tags=["Switches (v1)"])
app.include_router(config_template_by_name.router, tags=["Templates (v1)"])
