#!/usr/bin/env python
import copy
import datetime
from typing import List

from fastapi import Depends, HTTPException, Query
from sqlmodel import Session, select

from ..app import app
from ..db import get_session
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


@app.post(
    "/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{fabric_name}/{template_name}",
    response_model=FabricResponseModel,
)
def post_fabric(
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
    if db_fabric.SITE_ID is None:
        setattr(db_fabric, "SITE_ID", db_fabric.BGP_AS)

    session.add(db_fabric)
    try:
        session.commit()
    except Exception as error:
        raise HTTPException(status_code=404, detail=error) from error
    session.refresh(db_fabric)
    response = build_response(db_fabric)
    return response


@app.get(
    "/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/",
    response_model=List[FabricResponseModel],
)
def get_fabrics(
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
def get_fabric_by_fabric_name(*, session: Session = Depends(get_session), fabric_name: str):
    """
    # Summary

    GET request handler with fabric_name as path parameter.
    """
    fabric = session.get(Fabric, fabric_name)
    if not fabric:
        raise HTTPException(status_code=404, detail=f"Fabric {fabric_name} not found")
    response = build_response(fabric)
    return response


@app.put(
    "/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{fabric_name}/{template_name}",
    response_model=FabricResponseModel,
)
def put_fabric(
    *,
    session: Session = Depends(get_session),
    fabric_name: str,
    fabric: FabricUpdate,
):
    """
    # Summary

    PUT request handler
    """
    db_fabric = session.get(Fabric, fabric_name)
    if not db_fabric:
        raise HTTPException(status_code=404, detail=f"Fabric {fabric_name} not found")
    fabric_data = fabric.model_dump(exclude_unset=True)

    keys = fabric_data.keys()
    for key, value in fabric_data.items():
        setattr(db_fabric, key, value)
        # For now, update SITE_ID to equal BGP_AS if the user is not
        # explicitely setting SITE_ID.  This is not ideal since the user
        # may have already intentionally set SITE_ID != BGP_AS in the database,
        # and the code below will reset it.  But, for now, this serves our
        # immediate purpose.  TODO: Revisit later.
        if key == "BGP_AS" and "SITE_ID" not in keys:
            setattr(db_fabric, "SITE_ID", value)

    session.add(db_fabric)
    session.commit()
    session.refresh(db_fabric)
    response = build_response(db_fabric)
    return response


@app.delete("/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{fabric_name}")
def delete_fabric(*, session: Session = Depends(get_session), fabric_name: str):
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
    fabric = session.get(Fabric, fabric_name)
    if not fabric:
        detail = {"timestamp": int(datetime.datetime.now().timestamp()), "status": 404, "error": "Not Found", "path": f"/rest/control/fabrics/{fabric_name}"}
        raise HTTPException(status_code=404, detail=detail)
    session.delete(fabric)
    session.commit()
    return {f"Fabric '{fabric_name}' is deleted successfully!"}
