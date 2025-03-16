import copy
from typing import Any, List

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select

from .....db import get_session
from ....models.fabric import FabricDbModel, FabricResponseModel

router = APIRouter(
    prefix="/api/v1/manage",
)


def build_response(fabric) -> dict:
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
    fabrics = session.exec(select(FabricDbModel).offset(offset).limit(limit)).all()
    response = []
    response_fabric: dict[Any, Any] = {}
    for fabric in fabrics:
        response_fabric = FabricResponseModel(**build_response(fabric))
        response.append(copy.deepcopy(response_fabric))
    return response
