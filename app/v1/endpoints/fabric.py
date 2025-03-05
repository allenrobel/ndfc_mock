#!/usr/bin/env python
import copy
import datetime
from typing import List

from fastapi import Depends, HTTPException, Query
from sqlmodel import Session, select

from ...app import app
from ...db import get_session
from ..models.fabric import Fabric, FabricCreate, FabricResponseModel, FabricUpdate


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


@app.delete("/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{fabric_name}")
def v1_delete_fabric(*, session: Session = Depends(get_session), fabric_name: str):
    """
    # Summary

    DELETE request handler

    ## NDFC Response

    {
        "timestamp": 1739842602937,
        "status": 404,
        "error": "Not Found",
        "path": "/rest/control/fabrics/f2"
    }
    """
    db_fabric = session.exec(select(Fabric).where(Fabric.FABRIC_NAME == fabric_name)).first()
    if not db_fabric:
        detail = {}
        detail["timestamp"] = int(datetime.datetime.now().timestamp())
        detail["status"] = 404
        detail["error"] = "Not Found"
        detail["path"] = f"/rest/control/fabrics/{fabric_name}"
        raise HTTPException(status_code=404, detail=detail)
    session.delete(db_fabric)
    session.commit()
    return {f"Fabric '{fabric_name}' is deleted successfully!"}


@app.get(
    "/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/",
    response_model=List[FabricResponseModel],
)
def v1_get_fabrics(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    """
    # Summary

    GET request handler with limit and offset query parameters.
    """
    fabrics = session.exec(select(Fabric).offset(offset).limit(limit)).all()
    response = []
    response_fabric = {}
    for fabric in fabrics:
        response_fabric = build_response(fabric)
        response.append(copy.deepcopy(response_fabric))
    return response


@app.get(
    "/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{fabric_name}",
    response_model=FabricResponseModel,
)
def v1_get_fabric_by_fabric_name(*, session: Session = Depends(get_session), fabric_name: str):
    """
    # Summary

    GET request handler with fabric_name as path parameter.
    """
    db_fabric = session.exec(select(Fabric).where(Fabric.FABRIC_NAME == fabric_name)).first()
    if not db_fabric:
        raise HTTPException(status_code=404, detail=f"Fabric {fabric_name} not found")
    response = build_response(db_fabric)
    return response


@app.post(
    "/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{fabric_name}/{template_name}",
    response_model=FabricResponseModel,
)
def v1_post_fabric(
    *,
    session: Session = Depends(get_session),
    fabric_name: str,
    template_name: str,
    fabric: FabricCreate,
):
    """
    # Summary

    POST request handler
    """
    db_fabric = Fabric.model_validate(fabric)
    setattr(db_fabric, "FABRIC_NAME", fabric_name)
    setattr(db_fabric, "FF", template_name)

    session.add(db_fabric)
    try:
        session.commit()
    except Exception as error:
        # print(f"Error: {error}")
        session.rollback()
        msg = f"ND Site with name {fabric_name} already exists."
        raise HTTPException(status_code=500, detail=msg) from error
    session.refresh(db_fabric)
    response = build_response(db_fabric)
    return response


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
