import copy
from typing import List

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select

from .......db import get_session
from ......models.fabric import Fabric, FabricResponseModel
from .common import build_response

router = APIRouter(
    prefix="/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics",
)


@router.get("/", response_model=List[FabricResponseModel], description="(v1) Get all fabrics.")
def v1_fabrics_get(
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
