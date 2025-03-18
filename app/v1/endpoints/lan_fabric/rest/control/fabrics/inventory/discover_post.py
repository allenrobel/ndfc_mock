#!/usr/bin/env python

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ........db import get_session
from .......models.fabric import FabricDbModelV1
from .......models.inventory import SwitchDbModel, SwitchDiscoverBodyModel
from .common import build_db_switch

router = APIRouter(
    prefix="/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics",
)


def build_success_response():
    """
    # Summary

    Build a 200 response body for a successful operation.

    ## Notes

    """
    return {"status": "Success"}


@router.post("/{fabric_name}/inventory/discover")
def v1_inventory_discover_post(*, session: Session = Depends(get_session), fabric_name: str, switch_discovery_body: SwitchDiscoverBodyModel):
    """
    # Summary

    Discover switches for a given fabric_name.

    ## Endpoint

    ### Verb

    POST

    ### Path

    /appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{fabric_name}/inventory/discover
    """
    db_fabric = session.exec(select(FabricDbModelV1).where(FabricDbModelV1.FABRIC_NAME == fabric_name)).first()
    if not db_fabric:
        raise HTTPException(status_code=404, detail=f"Fabric {fabric_name} not found")
    fabric_id = db_fabric.id
    # Get all switches in the fabric
    db_switches = session.exec(select(SwitchDbModel).where(SwitchDbModel.fabricId == fabric_id)).all()
    # Raise an error if any switches in the discovery body already exist in the fabric
    for db_switch in db_switches:
        if db_switch.serialNumber in [discovery_body.serialNumber for discovery_body in switch_discovery_body.switches]:
            raise HTTPException(status_code=500, detail=f"Switch {db_switch.serialNumber} already exists in fabric {fabric_name}")
        if db_switch.ipAddress in [discovery_body.ipaddr for discovery_body in switch_discovery_body.switches]:
            raise HTTPException(status_code=500, detail=f"Switch {db_switch.ipAddress} already exists in fabric {fabric_name}")
    # Add all switches in the discovery body to the fabric
    for discovery_body in switch_discovery_body.switches:
        db_switch = build_db_switch(discovery_body, db_fabric)
        session.add(db_switch)
    session.commit()
    response = build_success_response()
    return response
