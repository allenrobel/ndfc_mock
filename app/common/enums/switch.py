from enum import Enum


class PlatformEnum(Enum):
    """
    Choices for switch platform
    """

    aci: str = "aci"
    nxos: str = "nx-os"


class SwitchConfigSyncStatusEnum(Enum):
    """
    Choices for switch configuration sync status
    """

    inSync: str = "inSync"
    outOfSync: str = "outOfSync"
    inProgress: str = "inProgress"
    notApplicable: str = "notApplicable"


class SwitchRoleEnum(Enum):
    """
    Choices for switch role
    """

    access: str = "access"
    aggregation: str = "aggregation"
    border: str = "border"
    borderGateway: str = "borderGateway"
    borderGatewaySpine: str = "borderGatewaySpine"
    borderGatewaySuperSpine: str = "borderGatewaySuperSpine"
    borderSpine: str = "borderSpine"
    borderSuperSpine: str = "borderSuperSpine"
    coreRouter: str = "coreRouter"
    edgeRouter: str = "edgeRouter"
    leaf: str = "leaf"
    spine: str = "spine"
    superSpine: str = "superSpine"
    tier2Leaf: str = "tier2Leaf"
    tor: str = "tor"


class SwitchRoleFriendlyEnum(Enum):
    """
    Switch role friendly names
    """

    access: str = "access"
    aggregation: str = "aggregation"
    border: str = "border"
    borderGateway: str = "border gateway"
    borderGatewaySpine: str = "border gateway spine"
    borderGatewaySuperSpine: str = "border gateway super spine"
    borderSpine: str = "border spine"
    borderSuperSpine: str = "border super spine"
    coreRouter: str = "core router"
    edgeRouter: str = "edge router"
    leaf: str = "leaf"
    spine: str = "spine"
    superSpine: str = "super spine"
    tier2Leaf: str = "tier2 leaf"
    tor: str = "tor"


class SwitchUnmanageableCauseEnum(Enum):
    """
    Choices for unmanageableCause field in Switch model.
    """

    none = ""
    Unreachable = "Unreachable"


class VpcRoleEnum(Enum):
    """
    Choices for vpc role
    """

    operationalPrimary: str = "operationalPrimary"
    operationalSecondary: str = "operationalSecondary"
    primary: str = "primary"
    secondary: str = "secondary"
