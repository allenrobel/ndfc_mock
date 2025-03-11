#!/usr/bin/env python
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select

from .......db import get_session
from ......models.inventory import SwitchDbModel

router = APIRouter(
    prefix="/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/switches",
)


class SwitchRoleUpdate(BaseModel):
    """
    # Summary

    POST request body for updating switch roles.
    """

    serialNumber: str
    role: str


def build_200_response(success_list):
    """
    # Summary

    Build a response for a 200 success.
    """
    return {"successList": ",".join(success_list), "errorList": []}


def build_400_response(success_list, failure_list):
    """
    # Summary

    Build a response for a 400 error.
    """
    error_list = []
    for failure in failure_list:
        fail_dict = {}
        fail_dict["serialNumber"] = failure
        fail_dict["Reason"] = "Invalid Switch (or) Switch not in inventory"
        error_list.append(fail_dict)
    return {
        "successList": ",".join(success_list),
        "errorList": error_list,
    }


@router.post("/roles")
def v1_post_switch_roles(*, session: Session = Depends(get_session), switch_roles: list[SwitchRoleUpdate]):
    """
    # Summary

    POST request handler for updating switch roles.
    """
    success_list = []
    failure_list = []
    result_code = 200
    for switch_role in switch_roles:
        db_switch = session.exec(select(SwitchDbModel).where(SwitchDbModel.serialNumber == switch_role.serialNumber)).first()
        if not db_switch:
            failure_list.append(switch_role.serialNumber)
            result_code = 400
        else:
            db_switch.role = switch_role.role
            db_switch.switchRoleEnum = switch_role.role
            session.add(db_switch)
            success_list.append(switch_role.serialNumber)
    if result_code == 400:
        detail = build_400_response(success_list, failure_list)
        raise HTTPException(status_code=result_code, detail=detail)
    session.commit()
    return build_200_response(success_list)
