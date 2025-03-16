import copy
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlmodel import Session, select

from .....db import get_session
from ....models.fabric import FabricDbModel, FabricResponseModel

router = APIRouter(
    prefix="/api/v1/manage",
)


class FabricLocationModel(BaseModel):
    """
    # Summary

    The location of the fabric, represented by latitude and longitude.
    """

    latitude: float
    longitude: float


class FabricManagementModel(BaseModel):
    """
    # Summary

    The management information for the fabric.

    TODO: This model should be moved to a shared location and
    include all parameters.  For now, we're supporting only
    mandatory parameters for testing.
    """

    bgpAsn: str
    type: str


def build_response(fabric: FabricDbModel) -> FabricResponseModel:
    """
    # Summary

    Build the representation of the fabric in the response.
    """
    location = FabricLocationModel(
        latitude=fabric.latitude,
        longitude=fabric.longitude,
    )
    management = FabricManagementModel(
        bgpAsn=fabric.bgpAsn,
        type=fabric.type,
    )
    response: FabricResponseModel = FabricResponseModel(
        name=fabric.name,
        category=fabric.category,
        licenseTier=fabric.licenseTier,
        location=location.model_dump(),
        management=management.model_dump(),
        securityDomain=fabric.securityDomain,
        telemetryCollectionType=fabric.telemetryCollectionType,
        telemetryStreamingProtocol=fabric.telemetryStreamingProtocol,
        telemetrySourceInterface=fabric.telemetrySourceInterface,
        telemetrySourceVrf=fabric.telemetrySourceVrf,
    )
    return response


@router.get(
    "/fabrics",
    response_model=List[dict[Any, Any]],
)
def v2_fabrics_get(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
) -> List[dict[Any, Any]]:
    """
    # Summary

    Endpoint handler for GET /api/v1/manage/fabrics
    """
    try:
        fabrics = session.exec(select(FabricDbModel).offset(offset).limit(limit)).all()
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error
    response = []
    response_fabric: dict[Any, Any] = {}
    try:
        for fabric in fabrics:
            response_fabric = FabricResponseModel.model_dump(build_response(fabric))
            response.append(copy.deepcopy(response_fabric))
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error
    try:
        return response
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error
