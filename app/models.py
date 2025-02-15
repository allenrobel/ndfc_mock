#!/usr/bin/env python
import uuid

from datetime import datetime
from sqlmodel import Field, SQLModel
from typing import Optional


def get_datetime():
    """
    We specifically do NOT want to store timezone info
    in the datetime object since we don't need it.  Rather,
    we are treating datetime like a timestamp.
    """
    return datetime.now().replace(tzinfo=None)

class FabricBase(SQLModel):
    fabricName: Optional[str] = Field(default="BAD_FABRIC", primary_key=True)
    asn: Optional[str] = Field(default=None, index=True)
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
