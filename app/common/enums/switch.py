from enum import Enum


class platform(Enum):
    """
    Choices for switch platform
    """

    aci: str = "aci"
    nxos: str = "nx-os"


class switchConfigSyncStatus(Enum):
    """
    Choices for switch configuration sync status
    """

    inSync: str = "inSync"
    outOfSync: str = "outOfSync"
    inProgress: str = "inProgress"
    notApplicable: str = "notApplicable"


class SwitchRole(Enum):
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


class vpcRole(Enum):
    """
    Choices for vpc role
    """

    operationalPrimary: str = "operationalPrimary"
    operationalSecondary: str = "operationalSecondary"
    primary: str = "primary"
    secondary: str = "secondary"
