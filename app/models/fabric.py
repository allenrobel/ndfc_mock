#!/usr/bin/env python
import uuid
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel

from .common import get_datetime


class FabricBase(SQLModel):
    """
    # Summary

    Base class for all other fabric classes.
    """

    fabricName: Optional[str] = Field(default="BAD_FABRIC", primary_key=True)
    asn: str = Field(index=True)
    templateName: Optional[str] = Field(default=None)

    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    created_at: Optional[datetime] = Field(default_factory=get_datetime)

    updated_at: Optional[datetime] = Field(
        default_factory=get_datetime,
        sa_column_kwargs={"onupdate": get_datetime},
    )


class Fabric(FabricBase, table=True):
    """
    # Summary

    Import to pick up all FabricBase behaviors.
    """


class FabricCreate(FabricBase):
    """
    # Summary

    Used to validate POST request content.
    """


class FabricPublic(FabricBase):
    """
    # Summary

    Returned to clients.
    """

    id: uuid.UUID


class FabricUpdate(SQLModel):
    """
    # Summary

    Used to validate PUT requests.
    """

    fabricName: Optional[str] = None
    asn: Optional[str] = None
    templateName: Optional[str] = None
