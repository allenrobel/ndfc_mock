# TODO: If SQLModel is ever fixed, remove the mypy directive below.
# https://github.com/fastapi/sqlmodel/discussions/732
# mypy: disable-error-code=call-arg
from enum import Enum

from pydantic import BaseModel, ConfigDict
from sqlmodel import Field, SQLModel

from ...common.validators.fabric import BgpValue
from ..validators.fabric import FabricManagementType


class FabricCategoryEnum(Enum):
    """
    Choices for fabric category parameter.
    """

    fabric = "fabric"
    fabricGroup = "fabricGroup"
    multiClusterFabricGroup = "multiClusterFabricGroup"


class LicenseTier(str, Enum):
    """
    Choices for the fabric licenseTier parameter.
    """

    advantage = "advantage"
    essentials = "essentials"
    premier = "premier"


class TelemetryCollectionType(Enum):
    """
    Choices for the fabric telemetryCollectionType parameter.
    """

    inBand = "inBand"
    outOfBand = "outOfBand"


class TelemetryStreamingProtocol(Enum):
    """
    Choices for the fabric telemetryStreamingProtocol parameter.
    """

    ipv4 = "ipv4"
    ipv6 = "ipv6"


class FabricManagement(SQLModel):
    """
    Contents of the fabric management object.
    TODO: Add remaining parameters.
    """

    model_config = ConfigDict(coerce_numbers_to_str=True)

    bgpAsn: str | int
    type: str


class FabricLocation(BaseModel):
    """
    Contents of the fabric location object.
    """

    latitude: float
    longitude: float


class FabricResponseModel(SQLModel):
    """
    Representation of the fabric in a response.
    """

    model_config = ConfigDict(use_enum_values=True, coerce_numbers_to_str=True)

    category: str = Field(FabricCategoryEnum)
    licenseTier: str = Field(LicenseTier)
    location: dict = Field(FabricLocation)
    management: FabricManagementType = Field(FabricManagement)
    name: str
    securityDomain: str | None = "all"
    telemetryCollectionType: str = Field(TelemetryCollectionType)
    telemetryStreamingProtocol: str = Field(TelemetryStreamingProtocol)
    telemetrySourceInterface: str | None = None
    telemetrySourceVrf: str | None = None


class FabricDbModelV2(SQLModel, table=True):
    """
    Representation of the fabric in the database.

    TODO: Need to add remaining parameters.
    """

    model_config = ConfigDict(use_enum_values=True)

    bgpAsn: BgpValue = Field(BgpValue)
    type: str
    latitude: float
    longitude: float
    category: str = Field(FabricCategoryEnum)
    licenseTier: str = Field(LicenseTier)
    name: str = Field(primary_key=True)
    securityDomain: str = Field(default="all")
    telemetryCollectionType: str = Field(TelemetryCollectionType)
    telemetryStreamingProtocol: str = Field(TelemetryStreamingProtocol)
    telemetrySourceInterface: str | None = Field(default="")
    telemetrySourceVrf: str | None = Field(default="")
