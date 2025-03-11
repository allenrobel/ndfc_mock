#!/usr/bin/env python
import copy

from fastapi import APIRouter

from ......models.lan_fabric_rest_control_switches_overview import V1LanFabricRestControlSwitchesOverviewResponseModel

router = APIRouter(
    prefix="/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/switches",
)


def build_response():
    """
    # Summary

    Build a response that aligns with the ResponseModel.

    This is a temporary stub so that ansible-dcnm Fabric().Deleted()
    will work.

    For now, we're only interested in the switchRoles field, which is
    accessed by ansible-dcnm Fabric().Deleted() to determine if any switches
    are present in the fabric.

    TODO: Need to reference switch tables for this info.
    TODO: Need to raise HTTPException if fabric does not exist.
    """
    response = {
        "switchSWVersions": {"10.2(5)": 7, "10.3(1)": 2},
        "switchHealth": {"Healthy": 2, "Minor": 7},
        "switchHWVersions": {"N9K-C93180YC-EX": 4, "N9K-C9504": 5},
        "switchConfig": {"Out-of-Sync": 5, "In-Sync": 4},
        "switchRoles": {"leaf": 0, "spine": 0, "border gateway": 0},
    }
    return copy.deepcopy(response)


@router.get(
    "/{fabric_name}/overview",
    response_model=V1LanFabricRestControlSwitchesOverviewResponseModel,
    description="Return summary of fabric inventory.",
)
def v1_lan_fabric_rest_control_switches_overview_by_fabric_name():
    """
    # Summary

    GET request handler
    """
    print(f"response: {build_response()}")
    return build_response()
