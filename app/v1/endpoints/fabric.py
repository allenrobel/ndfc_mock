#!/usr/bin/env python
import copy

from fastapi import Depends, HTTPException
from sqlmodel import Session, select

from ...app import app
from ...db import get_session
from ..models.fabric import Fabric, FabricResponseModel, FabricUpdate


def build_response(fabric):
    """
    # Summary

    Build a fabric response that aligns with FabricResponseModel

    ## Notes

    1. If FabricResponseModel is changed, this function must also be updated
    """
    response = {}
    response["id"] = fabric.id
    response["nvPairs"] = build_nv_pairs(fabric)
    return copy.deepcopy(response)


def build_nv_pairs(fabric):
    """
    # Summary

    Build the nvPairs object in a fabric response.
    """
    return fabric.model_dump()


@app.put(
    "/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{fabric_name}/{template_name}",
    response_model=FabricResponseModel,
)
def v1_put_fabric(
    *,
    session: Session = Depends(get_session),
    fabric_name: str,
    fabric: FabricUpdate,
):
    """
    # Summary

    PUT request handler
    """
    db_fabric = session.exec(select(Fabric).where(Fabric.FABRIC_NAME == fabric_name)).first()
    if not db_fabric:
        raise HTTPException(status_code=404, detail=f"Fabric {fabric_name} not found")
    fabric_data = fabric.model_dump(exclude_unset=True)

    for key, value in fabric_data.items():
        setattr(db_fabric, key, value)

    session.add(db_fabric)
    session.commit()
    session.refresh(db_fabric)
    response = build_response(db_fabric)
    return response
