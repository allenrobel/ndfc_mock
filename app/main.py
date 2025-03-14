#!/usr/bin/env python
# pylint: disable=unused-import
from .app import app
from .v1.endpoints.cisco.ndfc.api.about import version_get_internal
from .v1.endpoints.configtemplate.rest.config.templates import config_template_by_name
from .v1.endpoints.fm.about import version_get
from .v1.endpoints.fm.features import features_get
from .v1.endpoints.lan_fabric.rest.control.fabrics import fabric_delete, fabric_get, fabric_post, fabric_put, fabrics_get
from .v1.endpoints.lan_fabric.rest.control.fabrics.inventory import discover_post, internal_inventory_get, switches_by_fabric_get, test_reachability_post
from .v1.endpoints.lan_fabric.rest.control.switches import fabric_name_get, overview
from .v1.endpoints.lan_fabric.rest.control.switches.overview import v1_lan_fabric_rest_control_switches_overview_by_fabric_name
from .v1.endpoints.lan_fabric.rest.control.switches.roles import roles_get, roles_post
from .v1.endpoints.login import post_login
from .v2.endpoints.fabric import v2_delete_fabric, v2_get_fabric_by_fabric_name, v2_get_fabrics, v2_post_fabric, v2_put_fabric

app.include_router(fabric_delete.router, tags=["Fabrics (v1)"])
app.include_router(fabric_get.router, tags=["Fabrics (v1)"])
app.include_router(fabric_post.router, tags=["Fabrics (v1)"])
app.include_router(fabric_put.router, tags=["Fabrics (v1)"])
app.include_router(fabrics_get.router, tags=["Fabrics (v1)"])
app.include_router(features_get.router, tags=["Feature Manager (v1)"])
app.include_router(version_get.router, tags=["Feature Manager (v1)"])
app.include_router(version_get_internal.router, tags=["Internal (v1)"])
app.include_router(internal_inventory_get.router, tags=["Internal (v1)"])
app.include_router(discover_post.router, tags=["Inventory (v1)"])
app.include_router(switches_by_fabric_get.router, tags=["Inventory (v1)"])
app.include_router(roles_get.router, tags=["Inventory (v1)"])
app.include_router(roles_post.router, tags=["Inventory (v1)"])
app.include_router(test_reachability_post.router, tags=["Inventory (v1)"])
app.include_router(fabric_name_get.router, tags=["Switches (v1)"])
app.include_router(overview.router, tags=["Switches (v1)"])
app.include_router(config_template_by_name.router, tags=["Templates (v1)"])
