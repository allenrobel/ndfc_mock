#!/usr/bin/env python
from typing import List

from fastapi import Depends, HTTPException, Query
from sqlmodel import Session, select

from ..app import app
from ..db import get_session
from ..models.fabric import Fabric, FabricCreate, FabricPublic, FabricUpdate


@app.post(
    "/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{fabric_name}/{template_name}",
    response_model=FabricPublic,
)
def post_fabric(
    *,
    session: Session = Depends(get_session),
    fabric_name: str,
    template_name: str,
    fabric: FabricCreate,
):
    """
    # Summary

    POST request handler
    """
    db_fabric = Fabric.model_validate(fabric)
    print(f"db_fabric: {db_fabric}")
    setattr(db_fabric, "FABRIC_NAME", fabric_name)
    setattr(db_fabric, "FF", template_name)
    session.add(db_fabric)
    try:
        session.commit()
    except Exception as error:
        raise HTTPException(status_code=404, detail=error) from error
    session.refresh(db_fabric)
    return db_fabric


@app.get(
    "/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/",
    response_model=List[FabricPublic],
)
def get_fabrics(
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
    return fabrics


@app.get(
    "/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{fabric_name}",
    response_model=FabricPublic,
)
def get_fabric_by_fabric_name(*, session: Session = Depends(get_session), fabric_name: str):
    """
    # Summary

    GET request handler with fabric_name as path parameter.
    """
    fabric = session.get(Fabric, fabric_name)
    if not fabric:
        raise HTTPException(status_code=404, detail=f"Fabric {fabric_name} not found")
    return fabric


@app.put(
    "/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{fabric_name}/{template_name}",
    response_model=FabricPublic,
)
def put_fabric(
    *,
    session: Session = Depends(get_session),
    fabric_name: str,
    fabric: FabricUpdate,
):
    """
    # Summary

    PUT request handler
    """
    db_fabric = session.get(Fabric, fabric_name)
    if not db_fabric:
        raise HTTPException(status_code=404, detail=f"Fabric {fabric_name} not found")
    fabric_data = fabric.model_dump(exclude_unset=True)
    for key, value in fabric_data.items():
        setattr(db_fabric, key, value)
    session.add(db_fabric)
    session.commit()
    session.refresh(db_fabric)
    return db_fabric


@app.delete("/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{fabric_name}")
def delete_fabric(*, session: Session = Depends(get_session), fabric_name: str):
    """
    # Summary

    DELETE request handler
    """
    fabric = session.get(Fabric, fabric_name)
    if not fabric:
        raise HTTPException(status_code=404, detail=f"Fabric {fabric_name} not found")
    session.delete(fabric)
    session.commit()
    return {"ok": True}
