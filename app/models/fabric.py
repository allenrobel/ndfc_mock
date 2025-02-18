#!/usr/bin/env python
import uuid
from datetime import datetime
from enum import Enum

from pydantic import BaseModel
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

    BGP_AS: str
    FABRIC_NAME: str
    FF: str
    REPLICATION_MODE: str
    # id: uuid.UUID | None
    # created_at: datetime | None
    # updated_at: datetime | None


class FabricBase(SQLModel):
    """
    # Summary

    Base class for all other fabric classes.
    """

    BGP_AS: str = Field(index=True)
    FABRIC_NAME: str | None = Field(default=None, primary_key=True)
    FF: FFEnum = Field(default="Easy_Fabric")
    REPLICATION_MODE: ReplicationModeEnum | None = Field(default="Multicast")


class Fabric(FabricBase, table=True):
    """
    # Summary

    Define the fabric table in the database.
    """

    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    created_at: datetime | None = Field(default_factory=get_datetime)

    updated_at: datetime | None = Field(
        default_factory=get_datetime,
        sa_column_kwargs={"onupdate": get_datetime},
    )


class FabricCreate(FabricBase):
    """
    # Summary

    Used to validate POST request content.
    """


class FabricResponseModel(BaseModel):
    """
    # Summary

    Describes what is returned to clients.
    """

    id: uuid.UUID
    nvPairs: NvPairs


class FabricUpdate(SQLModel):
    """
    # Summary

    Used to validate PUT requests.
    """

    FABRIC_NAME: str | None = None
    BGP_AS: str | None = None
    REPLICATION_MODE: str | None = None
    FF: str | None = None
