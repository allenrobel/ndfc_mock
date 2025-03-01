#!/usr/bin/env python
import copy

from fastapi import Depends, HTTPException
from sqlmodel import Session

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


@app.post("/api/v1/manage/fabrics", response_model=FabricResponseModel)
async def post_fabric(*, session: Session = Depends(get_session), fabric: FabricResponseModel):
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
