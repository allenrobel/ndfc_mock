#!/usr/bin/env python
from fastapi import Depends, HTTPException
from sqlmodel import Field, Session, SQLModel, select

from .......app import app
from .......db import get_session
from ......models.inventory import SwitchDbModel


class SwitchFabricNameResponseModel(SQLModel):
    """
    Response model for endpoint v1_get_fabric_name_by_switch_serial_number().
    """

    fabricName: str = Field(min_length=1, max_length=32)


def build_response_fabric_name(db_switch: SwitchDbModel) -> SwitchFabricNameResponseModel:
    """
    # Summary

    Return response for v1_get_fabric_name_by_switch_serial_number()
    """
    return SwitchFabricNameResponseModel(
        fabricName=db_switch.fabricName,
    )


@app.get(
    "/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/switches/{switch_serial_number}/fabric-name",
    response_model=SwitchFabricNameResponseModel,
)
def v1_get_fabric_name_by_switch_serial_number(*, session: Session = Depends(get_session), switch_serial_number: str):
    """
    # Summary

    Return fabric name assocated with switch_serial_number, if it exists.
    """
    db_switch = session.exec(select(SwitchDbModel).where(SwitchDbModel.serialNumber == switch_serial_number)).first()
    if db_switch is None:
        raise HTTPException(status_code=404, detail=f"Switch {switch_serial_number} not found")
    print(f"ZZZ: Switch {switch_serial_number} found")
    print(f"ZZZ: db_switch: {db_switch}")
    return build_response_fabric_name(db_switch)
