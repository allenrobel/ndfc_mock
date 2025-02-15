#!/usr/bin/env python
from typing import List
import uuid

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Session, select
from .db import create_db_and_tables, get_session
from .models import Fabric, FabricCreate, FabricPublic, FabricUpdate


app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{fabric_name}/{template_name}", response_model=FabricPublic)
def create_fabric(*, session: Session = Depends(get_session), fabric_name: str, template_name: str, fabric: FabricCreate):
    db_fabric = Fabric.model_validate(fabric)
    print(f"db_fabric: {db_fabric}")
    setattr(db_fabric, "fabricName", fabric_name)
    setattr(db_fabric, "templateName", template_name)
    session.add(db_fabric)
    try:
        session.commit()
    except Exception as error:
        raise HTTPException(status_code=404, detail=error)
    session.refresh(db_fabric)
    return db_fabric

# @app.post("/fabrics/", response_model=FabricPublic)
# def create_fabric(*, session: Session = Depends(get_session), fabric: FabricCreate):
#     db_fabric = Fabric.model_validate(fabric)
#     print(f"db_fabric: {db_fabric}")
#     print(f"db_fabric.fabricName: {db_fabric.fabricName}")
#     session.add(db_fabric)
#     try:
#         session.commit()
#     except Exception as error:
#         raise HTTPException(status_code=404, detail=error)
#     session.refresh(db_fabric)
#     return db_fabric


@app.get("/fabrics/", response_model=List[FabricPublic])
def read_fabrics(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    fabrics = session.exec(select(Fabric).offset(offset).limit(limit)).all()
    return fabrics


@app.get("/fabrics/{fabric_id}", response_model=FabricPublic)
def read_fabric(*, session: Session = Depends(get_session), fabric_id: uuid.UUID):
    fabric = session.get(Fabric, fabric_id)
    if not fabric:
        raise HTTPException(status_code=404, detail="Fabric not found")
    return fabric


@app.put("/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{fabric_name}/{template_name}", response_model=FabricPublic)
def update_fabric(
    *, session: Session = Depends(get_session), fabric_name: str, template_name: str, fabric: FabricUpdate
):
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


@app.patch("/fabrics/{fabric_id}", response_model=FabricPublic)
def update_fabric(
    *, session: Session = Depends(get_session), fabric_id: uuid.UUID, fabric: FabricUpdate
):
    db_fabric = session.get(Fabric, fabric_id)
    if not db_fabric:
        raise HTTPException(status_code=404, detail="Fabric not found")
    fabric_data = fabric.model_dump(exclude_unset=True)
    for key, value in fabric_data.items():
        setattr(db_fabric, key, value)
    session.add(db_fabric)
    session.commit()
    session.refresh(db_fabric)
    return db_fabric


@app.delete("/fabrics/{fabric_id}")
def delete_fabric(*, session: Session = Depends(get_session), fabric_id: uuid.UUID):
    fabric = session.get(Fabric, fabric_id)
    if not fabric:
        raise HTTPException(status_code=404, detail=f"ID {fabric_id} not found")
    session.delete(fabric)
    session.commit()
    return {"ok": True}
