from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from .......db import get_session
from ......models.fabric import Fabric
from ......models.inventory import SwitchDbModel
from .common import build_404_response

router = APIRouter(
    prefix="/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics",
)


@router.delete("/{fabric_name}", description="(v1) Delete a fabric by name.")
def v1_fabric_delete(*, session: Session = Depends(get_session), fabric_name: str):
    """
    # Summary

    Fabric DELETE request handler

    ## Path

    /appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{fabric_name}
    """
    db_fabric = session.exec(select(Fabric).where(Fabric.FABRIC_NAME == fabric_name)).first()
    if not db_fabric:
        path = f"{router.prefix}/{fabric_name}"
        raise HTTPException(status_code=404, detail=build_404_response(path))
    fabric_id = db_fabric.id
    db_switches = session.exec(select(SwitchDbModel).where(SwitchDbModel.fabricId == fabric_id)).all()
    if len(db_switches) != 0:
        msg = "Failed to delete the fabric. Please check Events for possible reasons."
        raise HTTPException(status_code=500, detail=msg)

    session.delete(db_fabric)
    session.commit()
    return {f"Fabric '{fabric_name}' is deleted successfully!"}
