#!/usr/bin/env python
import uuid

from datetime import datetime
from sqlmodel import Field, SQLModel
from typing import Optional
from .common import get_datetime


class FabricBase(SQLModel):
    fabricName: Optional[str] = Field(default="BAD_FABRIC", primary_key=True)
    asn: str = Field(index=True)
    templateName: Optional[str] = Field(default=None)

    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    created_at: Optional[datetime] = Field(
        default_factory=get_datetime
    )

    updated_at: Optional[datetime] = Field(
        default_factory=get_datetime,
        sa_column_kwargs={"onupdate": get_datetime},
    )


class Fabric(FabricBase, table=True):
    pass


class FabricCreate(FabricBase):
    pass


class FabricPublic(FabricBase):
    id: uuid.UUID


class FabricUpdate(SQLModel):
    fabricName: Optional[str] = None
    asn: Optional[str] = None
    templateName: Optional[str] = None
