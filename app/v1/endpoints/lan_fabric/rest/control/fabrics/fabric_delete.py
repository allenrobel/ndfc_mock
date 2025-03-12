import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from .......db import get_session
from ......models.fabric import Fabric

router = APIRouter(
    prefix="/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics",
)


@router.delete("/{fabric_name}", description="(v1) Delete a fabric by name.")
def v1_fabric_delete(*, session: Session = Depends(get_session), fabric_name: str):
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
