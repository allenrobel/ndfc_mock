#!/usr/bin/env python
import copy
from typing import List

from fastapi import Depends, HTTPException, Query
from sqlmodel import Session, select

from ...app import app
from ...db import get_session
from ..models.fabric import FabricDbModel, FabricResponseModel


def build_response(fabric):
    """
    # Summary

    Build the representation of the fabric in the response.
    """
    response = {}
    response["name"] = fabric.name
    response["category"] = fabric.category
    response["licenseTier"] = fabric.licenseTier
    response["management"] = {}
    response["management"]["bgpAsn"] = fabric.bgpAsn
    response["management"]["type"] = fabric.type
    response["location"] = {}
    response["location"]["latitude"] = fabric.latitude
    response["location"]["longitude"] = fabric.longitude
    response["securityDomain"] = fabric.securityDomain
    response["telemetryCollectionType"] = fabric.telemetryCollectionType
    response["telemetryStreamingProtocol"] = fabric.telemetryStreamingProtocol
    response["telemetrySourceInterface"] = fabric.telemetrySourceInterface
    response["telemetrySourceVrf"] = fabric.telemetrySourceVrf
    return copy.deepcopy(response)


def build_db_fabric(fabric):
    """
    # Summary

    Build the representation of the fabric in the database.
    """
    fabric_dict = fabric.model_dump()
    db_fabric = FabricDbModel()
    db_fabric.name = fabric.name
    db_fabric.category = fabric.category
    db_fabric.licenseTier = fabric.licenseTier
    db_fabric.bgpAsn = fabric_dict.get("management", {}).get("bgpAsn")
    db_fabric.type = fabric_dict.get("management", {}).get("type")
    db_fabric.latitude = fabric_dict.get("location", {}).get("latitude")
    db_fabric.longitude = fabric_dict.get("location", {}).get("longitude")
    db_fabric.securityDomain = fabric.securityDomain
    db_fabric.telemetryCollectionType = fabric.telemetryCollectionType
    db_fabric.telemetryStreamingProtocol = fabric.telemetryStreamingProtocol
    db_fabric.telemetrySourceInterface = fabric.telemetrySourceInterface
    db_fabric.telemetrySourceVrf = fabric.telemetrySourceVrf
    return db_fabric


@app.delete("/api/v1/manage/fabrics/{fabric_name}", status_code=204)
async def v2_delete_fabric(*, session: Session = Depends(get_session), fabric_name: str):
    """
    # Summary

    DELETE request handler

    ## NDFC 404 Response (4.0 LA)

    ```json
    {
        "code": 404,
        "description": "",
        "message": f"Fabric f1 not found"
    }
    ```
    """
    fabric = session.get(FabricDbModel, fabric_name)
    if not fabric:
        detail = {"code": 404, "description": "", "message": f"Fabric {fabric_name} not found"}
        raise HTTPException(status_code=404, detail=detail)
    session.delete(fabric)
    session.commit()
    return {}


@app.get(
    "/api/v1/manage/fabrics",
    response_model=List[FabricResponseModel],
)
def v2_get_fabrics(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    """
    # Summary

    GET request handler with limit and offset query parameters.
    """
    fabrics = session.exec(select(FabricDbModel).offset(offset).limit(limit)).all()
    response = []
    response_fabric = {}
    for fabric in fabrics:
        response_fabric = build_response(fabric)
        response.append(copy.deepcopy(response_fabric))
    return response


@app.get(
    "/api/v1/manage/fabrics/{fabric_name}",
    response_model=FabricResponseModel,
)
def v2_get_fabric_by_fabric_name(*, session: Session = Depends(get_session), fabric_name: str):
    """
    # Summary

    GET request handler with fabric_name as path parameter.
    """
    fabric = session.get(FabricDbModel, fabric_name)
    if not fabric:
        raise HTTPException(status_code=404, detail=f"Fabric {fabric_name} not found")
    response = build_response(fabric)
    return response


@app.post("/api/v1/manage/fabrics", response_model=FabricResponseModel)
async def v2_post_fabric(*, session: Session = Depends(get_session), fabric: FabricResponseModel):
    """
    # Summary

    POST request handler
    """
    db_fabric = build_db_fabric(fabric)
    session.add(db_fabric)
    try:
        session.commit()
    except Exception as error:
        # print(f"Error: {error}")
        session.rollback()

        status_code = 400
        msg = f"[Fabric {db_fabric.name} is already present in the cluster "
        msg += f"A fabric with name {db_fabric.name} is already in use on "
        msg += "this cluster]"
        error_response = {}
        error_response["code"] = status_code
        error_response["description"] = ""
        error_response["message"] = msg
        raise HTTPException(status_code=status_code, detail=error_response) from error
    session.refresh(db_fabric)
    response = build_response(db_fabric)
    return response


@app.put(
    "/api/v1/manage/fabrics/{fabric_name}",
    response_model=FabricResponseModel,
)
def v2_put_fabric(
    *,
    session: Session = Depends(get_session),
    fabric_name: str,
    fabric: FabricResponseModel,
):
    """
    # Summary

    PUT request handler

    ## Notes to future self

    -   Nested key handling below will break when we add
        nested keys under management to the model, e.g.
        .netflowSettings, .leafTorVpcPortChannelIdRange, etc.
    """
    db_fabric = session.get(FabricDbModel, fabric_name)
    if not db_fabric:
        raise HTTPException(status_code=404, detail=f"Fabric {fabric_name} not found")
    fabric_data = fabric.model_dump(exclude_unset=True)

    nested_keys = ["management", "location"]
    for key, value in fabric_data.items():
        if key in nested_keys:
            for nested_key, nested_value in value.items():
                setattr(db_fabric, nested_key, nested_value)
        else:
            setattr(db_fabric, key, value)

    session.add(db_fabric)
    session.commit()
    session.refresh(db_fabric)
    response = build_response(db_fabric)
    return response
