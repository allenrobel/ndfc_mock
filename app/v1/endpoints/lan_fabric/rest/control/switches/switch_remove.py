from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from .......db import get_session
from ......models.fabric import FabricDbModelV1
from ......models.inventory import SwitchDbModel
from ..fabrics.common import build_404_response
from ..switches.models.switch_overview import SwitchOverviewHealth, SwitchOverviewHw, SwitchOverviewRoles, SwitchOverviewSw, SwitchOverviewSync

router = APIRouter(
    prefix="/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics",
)


def update_health(db_session: Session, fabric_name: str, health: str):
    """
    # Summary

    Update the switch health information associated with SwitchOverview.
    """
    if health == "":
        return
    instance = SwitchOverviewHealth()
    instance.session = db_session
    instance.fabric = fabric_name
    instance.health = health
    instance.remove()


def update_hw(db_session: Session, fabric_name: str, model: str):
    """
    # Summary

    Update the switch hardware information associated with SwitchOverview.
    """
    if model == "":
        return
    instance = SwitchOverviewHw()
    instance.session = db_session
    instance.fabric = fabric_name
    instance.model = model
    instance.remove()


def update_role(db_session: Session, fabric_name: str, role: str):
    """
    # Summary

    Update the switch role information associated with SwitchOverview.
    """
    if role == "":
        return
    instance = SwitchOverviewRoles()
    instance.session = db_session
    instance.fabric = fabric_name
    instance.role = role
    instance.remove()


def update_sw(db_session: Session, fabric_name: str, release: str):
    """
    # Summary

    Update the switch software information associated with SwitchOverview.
    """
    if release == "":
        return
    instance = SwitchOverviewSw()
    instance.session = db_session
    instance.fabric = fabric_name
    instance.version = release
    instance.remove()


def update_sync(db_session: Session, fabric_name: str, sync: str):
    """
    # Summary

    Update the switch sync information associated with SwitchOverview.
    """
    if sync == "":
        return
    instance = SwitchOverviewSync()
    instance.session = db_session
    instance.fabric = fabric_name
    instance.sync = sync.lower().replace("-", "_")
    instance.remove()


description = "(v1) Remove the Switch from the given Fabric."


@router.delete("/{fabric_name}/switches/{serial_number}", description=description)
def v1_remove_switch_from_fabric(*, session: Session = Depends(get_session), fabric_name: str, serial_number: str):
    """
    # Summary

    Switch DELETE request handler

    ## Path

    /appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{fabricName}/switches/{serialNumber}
    """
    db_fabric = session.exec(select(FabricDbModelV1).where(FabricDbModelV1.FABRIC_NAME == fabric_name)).first()
    if not db_fabric:
        path = f"{router.prefix}/{fabric_name}/switches/{serial_number}"
        raise HTTPException(status_code=404, detail=build_404_response(path))
    fabric_id = db_fabric.id
    db_switch = session.exec(select(SwitchDbModel).where(SwitchDbModel.fabricId == fabric_id).where(SwitchDbModel.serialNumber == serial_number)).first()
    if db_switch is None:
        # NDFC returns 200 as if the switch was actually removed.  We emulate that here.
        msg = f"The switch(es)={serial_number} have been removed from the fabric={fabric_name}"
        return msg

    health = db_switch.operStatus
    model = db_switch.model
    release = db_switch.release
    role = db_switch.switchRole
    sync = db_switch.ccStatus

    update_health(session, fabric_name, health)
    update_hw(session, fabric_name, model)
    update_role(session, fabric_name, role)
    update_sw(session, fabric_name, release)
    update_sync(session, fabric_name, sync)

    session.delete(db_switch)
    session.commit()
    # NDFC response
    # The switch(es)=FOX2109PGCS have been removed from the fabric=F1
    msg = f"The switch(es)={serial_number} have been removed from the fabric={fabric_name}"
    return msg
