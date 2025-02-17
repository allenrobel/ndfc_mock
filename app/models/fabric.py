#!/usr/bin/env python
import uuid
from datetime import datetime
from enum import Enum
from typing import Optional

from sqlmodel import Field, SQLModel

from .common import get_datetime


class ReplicationModeEnum(str, Enum):
    """
    # Summary

    Defines choices for REPLICATION_MODE
    """
    Ingress = "Ingress"
    Multicast = "Multicast"


class FFEnum(str, Enum):
    """
    # Summary

    Defines choices for FF
    """
    Easy_Fabric = "Easy_Fabric"


class NvPairs(SQLModel):
    """
    # Summary

    Not currently used
    """
    REPLICATION_MODE: ReplicationModeEnum
    BGP_AS: str


class FabricBase(SQLModel):
    """
    # Summary

    Base class for all other fabric classes.
    """

    FABRIC_NAME: Optional[str] = Field(default="BAD_FABRIC", primary_key=True)
    BGP_AS: str = Field(index=True)
    REPLICATION_MODE: ReplicationModeEnum = Field(default="Multicast")
    FF: FFEnum = Field(default="Easy_Fabric")

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

    FABRIC_NAME: Optional[str] = None
    BGP_AS: Optional[str] = None
    REPLICATION_MODE: Optional[str] = None
    FF: Optional[str] = None
