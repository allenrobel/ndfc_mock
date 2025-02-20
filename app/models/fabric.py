#!/usr/bin/env python
# TODO: If SQLModel is ever fixed, remove the mypy directive below.
# https://github.com/fastapi/sqlmodel/discussions/732
# mypy: disable-error-code=call-arg
import uuid
from datetime import datetime
from enum import Enum

from pydantic import BaseModel
from sqlmodel import Field, SQLModel

from .common import get_datetime


class AgentIntfEnum(str, Enum):
    """
    # Summary

    Defines choices for AGENT_INTF
    """

    eth0 = "eth0"
    eth1 = "eth1"


class BgpAuthKeyTypeEnum(str, Enum):
    """
    # Summary

    Defines choices for BGP_AUTH_KEY_TYPE
    """

    Three = "3"
    Seven = "7"


class CoppPolicyEnum(str, Enum):
    """
    # Summary

    Defines choices for COPP_POLICY
    """

    dense = "dense"
    lenient = "lenient"
    moderate = "moderate"
    strict = "strict"
    manual = "manual"


class DhcpIpv6EnableEnum(str, Enum):
    """
    # Summary

    Defines choices for DHCP_IPV6_ENABLE
    """

    DHCPv4 = "DHCPv4"
    DHCPv6 = "DHCPv6"


class FabricInterfaceTypeEnum(str, Enum):
    """
    # Summary

    Defines choices for FABRIC_INTERFACE_TYPE
    """

    p2p = "p2p"
    unnumbered = "unnumbered"


class FFEnum(str, Enum):
    """
    # Summary

    Defines choices for FF
    """

    Easy_Fabric = "Easy_Fabric"


class EnableDisableEnum(str, Enum):
    """
    # Summary

    Defines choices for any properties with values constrained to
    "Enable" and "Disable".
    """

    Enable = "Enable"
    Disable = "Disable"


class IsisLevelEnum(str, Enum):
    """
    # Summary

    Defines choices for ISIS_LEVEL
    """

    level_1 = "level-1"
    level_2 = "level-2"


class MacsecAlgorithmEnum(str, Enum):
    """
    # Summary

    Defines choices for MACSEC_ALGORITHM
    """

    AES_128_CMAC = "AES_128_CMAC"
    AES_256_CMAC = "AES_256_CMAC"


class ReplicationModeEnum(str, Enum):
    """
    # Summary

    Defines choices for REPLICATION_MODE
    """

    Ingress = "Ingress"
    Multicast = "Multicast"


class VrfLiteAutoconfigEnum(str, Enum):
    """
    # Summary

    Defines choices for VRF_LITE_AUTOCONFIG
    """

    Manual = "Manual"
    Back2BackAndToExternal = "Back2Back&ToExternal"


class Descriptions:
    """
    # Summary

    Property descriptions.
    """

    # pylint: disable=missing-function-docstring
    def __init__(self):
        pass

    @property
    def aaa_remote_ip_enabled(self):
        """
        AAA_REMOTE_IP_ENABLED
        """
        desc = "Enable AAA IP Authorization. "
        desc += "Enable only when IP Authorization is enabled in the AAA Server."
        return desc

    @property
    def aaa_server_conf(self):
        """
        AAA_REMOTE_IP_ENABLED
        """
        return "AAA Freeform Config"

    @property
    def agent_intf(self):
        return "Agent Interface. Interface to connect to Agent."

    @property
    def anycast_bgw_advertise_pip(self):
        desc = "Anycast Border Gateway advertise-pip. "
        desc += "To advertise Anycast Border Gateway PIP as VTEP. "
        desc += "Effective on MSD fabric after 'Recalculate Config'."
        return desc

    @property
    def anycast_gw_mac(self):
        desc = "Anycast Gateway MAC Address. "
        desc += "Shared MAC address for all leafs (xxxx.xxxx.xxxx)."
        return desc

    @property
    def anycast_lb_id(self):
        desc = "Underlay Anycast Loopback Id. "
        desc += "Used for vPC Peering in VXLANv6 Fabrics (Min:0, Max:1023)."
        return desc

    @property
    def anycast_rp_ip_range(self):
        desc = "Underlay RP Loopback IP Range. "
        desc += "Anycast or Phantom RP IP Address Range."
        return desc

    @property
    def auto_vrflite_ifc_default_vrf(self):
        desc = "Auto Deploy Default VRF. "
        desc += "Whether to auto generate Default VRF interface and BGP "
        desc += "peering configuration on VRF LITE IFC auto deployment. "
        desc += "If set, auto created VRF Lite IFC links will have "
        desc += "'Auto Deploy Default' enabled."
        return desc

    @property
    def bfd_auth_key_id(self):
        return "BFD Authentication Key ID. "

    @property
    def bfd_auth_key(self):
        return "BFD Authentication Key. Encrypted SHA1 secret value."

    @property
    def bfd_enable(self):
        return "Enable BFD. Valid for IPv4 Underlay only."

    @property
    def bfd_ibgp_enable(self):
        return "Enable BFD For iBGP."

    @property
    def bfd_ospf_enable(self):
        return "Enable BFD For OSPF."

    @property
    def bgp_as(self):
        desc = "BGP ASN. "
        desc += "1-4294967295 | 1-65535[.0-65535]. "
        desc += "It is a good practice to have a unique ASN for each Fabric."
        return desc

    @property
    def bgp_auth_enable(self):
        return "Enable BGP Authentication"

    @property
    def bgp_auth_key(self):
        return "Encrypted BGP Authentication Key based on BGP_AUTH_KEY_TYPE."

    @property
    def bgp_auth_key_type(self):
        return "BGP Key Encryption Type: 3 - 3DES, 7 - Cisco."

    @property
    def bootstrap_conf(self):
        desc = "Bootstrap Freeform Config. "
        desc += "Additional CLIs required during device bootup/login "
        desc += "e.g. AAA/Radius."
        return desc

    @property
    def bootstrap_enable(self):
        desc = "Enable Bootstrap. "
        desc += "Automatic IP Assignment For POAP."
        return desc

    @property
    def bootstrap_multisubnet(self):
        desc = "DHCPv4 Multi Subnet Scope. "
        desc += "lines with # prefix are ignored here."
        return desc

    @property
    def brfield_debug_flag(self):
        desc = "!!! Only for brf debugging purpose !!! "
        desc += "Dont' use until you are aware about it."
        return desc

    @property
    def brownfield_skip_overlay_network_attachments(self):
        desc = "Skip Overlay Network Interface Attachments. "
        desc += "Enable to skip overlay network interface attachments "
        desc += "for Brownfield and Host Port Resync cases."
        return desc

    @property
    def cdp_enable(self):
        desc = "Enable CDP for Bootstrapped Switch. "
        desc += "Enable CDP on management interface."
        return desc

    @property
    def copp_policy(self):
        desc = "Fabric Wide CoPP Policy. Customized CoPP policy should be "
        desc += "provided when 'manual' is selected."
        return desc

    @property
    def dci_subnet_range(self):
        return "Address range to assign P2P Interfabric Connections."

    @property
    def default_network(self):
        desc = "Default Overlay Network Template For Leafs."
        return desc

    @property
    def default_pvlan_sec_network(self):
        desc = "Default PVLAN Secondary Network Template."
        return desc

    @property
    def default_queuing_policy_cloudscale(self):
        desc = "N9K Cloud Scale Platform Queuing Policy. "
        desc += "Queuing Policy for all 92xx, -EX, -FX, -FX2, -FX3, -GX "
        desc += "series switches in the fabric."
        return desc

    @property
    def default_queuing_policy_other(self):
        desc = "Other N9K Platform Queuing Policy. "
        desc += "Queuing Policy for all other switches in the fabric."
        return desc

    @property
    def default_queuing_policy_r_series(self):
        desc = "N9K R-Series Platform Queuing Policy. "
        desc += "Queuing Policy for all R-Series switches in the fabric."
        return desc

    @property
    def default_vrf(self):
        return "Default Overlay VRF Template For Leafs."

    @property
    def default_vrf_redis_bgp_rmap(self):
        desc = "Redistribute BGP Route-map Name. "
        desc += "Route Map used to redistribute BGP routes to IGP in default "
        desc += "vrf in auto created VRF Lite IFC links."
        return desc

    @property
    def deployment_freeze(self):
        return "Disable all deployments in this fabric."

    @property
    def dhcp_enable(self):
        desc = "Enable Local DHCP Server. "
        desc += "Automatic IP Assignment For POAP From Local DHCP Server."
        return desc

    @property
    def dhcp_end(self):
        desc = "DHCP Scope End Address. "
        desc += "End Address For Switch POAP."
        return desc

    @property
    def dhcp_ipv6_enable(self):
        desc = "DHCP Version. "
        desc += "One of DHCPv4 or DHCPv6."
        return desc

    @property
    def dhcp_start(self):
        desc = "DHCP Scope Start Address. "
        desc += "Start Address For Switch POAP."
        return desc

    @property
    def dns_server_ip_list(self):
        desc = "DNS Server IPs. "
        desc += "Comma separated list of IP Addresses(v4/v6)."
        return desc

    @property
    def dns_server_vrf(self):
        desc = "DNS Server VRFs. "
        desc += "One VRF for all DNS servers or a comma separated list of VRFs, one per DNS server."
        return desc

    @property
    def enable_aaa(self):
        desc = "Include AAA configs from Manageability tab during device bootup."
        return desc

    @property
    def enable_agent(self):
        return "Enable Agent (developmet purpose only)."

    @property
    def enable_default_queuing_policy(self):
        return "Enable Default Queuing Policies."

    @property
    def enable_evpn(self):
        return "Enable EVPN (extensible virtual private network)."

    @property
    def enable_fabric_vpc_domain_id(self):
        desc = "Enable the same vPC Domain Id <br />for all vPC Pairs. "
        desc += "(Not Recommended)."
        return desc

    @property
    def enable_macsec(self):
        return "Enable MACsec in the fabric."

    @property
    def enable_netflow(self):
        return "Enable Netflow on VTEPs."

    @property
    def enable_ngoam(self):
        desc = "Enable VXLAN OAM. "
        desc += "Enable the Next Generation (NG) OAM feature for all switches "
        desc += "in the fabric to aid in trouble-shooting VXLAN EVPN fabrics."
        return desc

    @property
    def enable_nxapi(self):
        return "Enable HTTPS NX-API"

    @property
    def enable_nxapi_http(self):
        return "Enable HTTP NX-API."

    @property
    def enable_pvlan(self):
        desc = "Enable Private VLAN (PVLAN). "
        desc += "Enable PVLAN on switches except spines and super spines."
        return desc

    @property
    def enable_tenant_dhcp(self):
        return "Enable Tenant DHCP."

    @property
    def enable_trm(self):
        desc = "Enable Tenant Routed Multicast (TRM). "
        desc += "For Overlay Multicast Support In VXLAN Fabrics."
        return desc

    @property
    def enable_vpc_peer_link_native_vlan(self):
        desc = "Make vPC Peer Link VLAN as Native VLAN."
        return desc

    @property
    def extra_conf_intra_links(self):
        return "Additional CLIs For All Intra-Fabric Links."

    @property
    def extra_conf_leaf(self):
        desc = "Leaf Freeform Config. "
        desc += "Additional CLIs For All Leafs As Captured From "
        desc += "Show Running Configuration."
        return desc

    @property
    def extra_conf_spine(self):
        desc = "Spine Freeform Config. "
        desc += "Additional CLIs For All Spines As Captured From "
        desc += "Show Running Configuration."
        return desc

    @property
    def extra_conf_tor(self):
        desc = "ToR Freeform Config. "
        desc += "Additional CLIs For All ToRs As Captured From "
        desc += "Show Running Configuration."
        return desc

    @property
    def fabric_interface_type(self):
        desc = "Fabric Interface Numbering. "
        desc += "ptp (Numbered Point-to-Point) or unnumbered."
        return desc

    @property
    def fabric_mtu(self):
        desc = "Intra Fabric Interface MTU. "
        desc += "(Min:576, Max:9216). Must be an even number."
        return desc

    @property
    def fabric_name(self):
        desc = "Fabric Name. "
        desc += "Maximum length, 32 characters."
        return desc

    @property
    def fabric_vpc_domain_id(self):
        return "vPC Domain Id to be used on all vPC pairs in the fabric."

    @property
    def fabric_vpc_domain_id_prev(self):
        return "Internal Fabric Wide vPC Domain Id."

    @property
    def fabric_vpc_qos(self):
        desc = "Enable Qos for Fabric vPC-Peering. "
        desc += "Qos on spines for guaranteed delivery of vPC Fabric Peering "
        desc += "communication."
        return desc

    @property
    def feature_ptp(self):
        return "Enable Precision Time Protocol (PTP)."

    @property
    def ff(self):
        return "Template Family."

    @property
    def grfield_debug_flag(self):
        desc = "Enable to clean switch configuration without reload when "
        desc += "PreserveConfig=no."
        return desc

    @property
    def hd_time(self):
        desc = "NVE Source Inteface HoldDown Time (Min:1, Max:1500) in seconds."
        return desc

    @property
    def ibgp_peer_template(self):
        desc = "Specifies the iBGP Peer-Template config used for RR and "
        desc += "spines with border role."
        return desc

    @property
    def ibgp_peer_template_leaf(self):
        desc = "Specifies the config used for leaf, border or border gateway. "
        desc += "If this field is empty, the peer template defined in iBGP "
        desc += "Peer-Template Config is used on all BGP enabled devices "
        desc += "(RRs, leafs, border or border gateway roles)."
        return desc

    @property
    def isis_auth_keychain_name(self):
        return "IS-IS Authentication Keychain Name."

    @property
    def isis_level(self):
        return "Supported IS levels: level-1, level-2."

    @property
    def loopback1_ip_range(self):
        desc = "Underlay VTEP Loopback IP Range. "
        desc += "Typically Loopback1 IP Address Range."
        return desc

    @property
    def loopback1_ipv6_range(self):
        desc = "Underlay VTEP Loopback IPv6 Range. "
        desc += "Typically Loopback1 and Anycast Loopback IPv6 Address Range."
        return desc

    @property
    def macsec_algorithm(self):
        desc = "MACsec Primary Cryptographic Algorithm. AES_128_CMAC or "
        desc += "AES_256_CMAC."
        return desc

    @property
    def pim_hello_auth_enable(self):
        return "Enable PIM Hello Authentication."

    @property
    def router_id_range(self):
        desc = "BGP Router ID Range for IPv6 Underlay."
        return desc

    @property
    def seed_switch_core_interfaces(self):
        return "Seed Switch Fabric Interfaces."

    @property
    def service_network_vlan_range(self):
        desc = "Per Switch Overlay Service Network VLAN Range "
        desc += "(Min:2, Max:4094)."
        return desc

    @property
    def sspine_add_del_debug_flag(self):
        desc = "Allow First Super Spine Add or Last Super Spine Delete "
        desc += "From Topology."

    @property
    def subnet_target_mask(self):
        return "Underlay Subnet IP Mask."

    @property
    def tcam_allocation(self):
        desc = "TCAM commands are automatically generated for VxLAN and vPC "
        desc += "Fabric Peering when Enabled."
        return desc

    @property
    def vpc_peer_link_po(self):
        return 'vPC Peer Link Port Channel ID. example: "1-40".'

    @property
    def vrf_lite_autoconfig(self):
        desc = "VRF Lite Inter-Fabric Connection Deployment Options. "
        desc += "If Back2Back&ToExternal is selected, VRF Lite IFCs "
        desc += "are auto created between border devices of two Easy Fabrics, "
        desc += "and between border devices in Easy Fabric and edge routers in "
        desc += "External Fabric. The IP address is taken from the "
        desc += "VRF Lite Subnet IP Range pool."
        return desc

    @property
    def vrf_vlan_range(self):
        return "Per Switch Overlay VRF VLAN Range (Min:2, Max:4094)."


class Defaults:
    """
    # Summary

    Property default values.
    """

    # pylint: disable=missing-function-docstring
    @property
    def bootstrap_multisubnet(self):
        return "#Scope_Start_IP, Scope_End_IP, Scope_Default_Gateway, Scope_Subnet_Prefix"


class FabricBase(SQLModel):
    """
    # Summary

    Base class for all other fabric classes.
    """

    abstract_anycast_rp: str | None = Field(default="anycast_rp")
    abstract_bgp_neighbor: str | None = Field(default="evpn_bgp_rr_neighbor")
    abstract_bgp_rr: str | None = Field(default="evpn_bgp_rr")
    abstract_bgp: str | None = Field(default="base_bgp")
    abstract_dhcp: str | None = Field(default="base_dhcp")

    abstract_extra_config_bootstrap: str | None = Field(default="extra_config_bootstrap_11_1")
    abstract_extra_config_leaf: str | None = Field(default="extra_config_leaf")
    abstract_extra_config_spine: str | None = Field(default="extra_config_spine")
    abstract_extra_config_tor: str | None = Field(default="extra_config_tor")

    abstract_feature_leaf: str | None = Field(default="base_feature_leaf_upg")
    abstract_feature_spine: str | None = Field(default="base_feature_spine_upg")

    abstract_isis: str | None = Field(default="base_isis_level2")
    abstract_isis_interface: str | None = Field(default="isis_interface")

    abstract_loopback_interface: str | None = Field(default="int_fabric_loopback_11_1")
    abstract_multicast: str | None = Field(default="base_multicast_11_1")

    abstract_ospf: str | None = Field(default="base_ospf")
    abstract_ospf_interface: str | None = Field(default="ospf_interface_11_1")
    abstract_pim_interface: str | None = Field(default="pim_interface")

    abstract_route_map: str | None = Field(default="route_map")
    abstract_routed_host: str | None = Field(default="int_routed_host")
    abstract_trunk_host: str | None = Field(default="int_trunk_host")
    abstract_vlan_interface: str | None = Field(default="int_fabric_vlan_11_1")
    abstract_vpc_domain: str | None = Field(default="base_vpc_domain_11_1")

    default_network: str | None = Field(default="Default_Network_Universal", description=Descriptions().default_network)
    default_pvlan_sec_network: str | None = Field(default="Pvlan_Secondary_Network", description=Descriptions().default_pvlan_sec_network)
    default_vrf: str | None = Field(default="Default_VRF_Universal", description=Descriptions().default_vrf)

    temp_vpc_peer_link: str | None = Field(default="int_vpc_peer_link_po")

    AAA_REMOTE_IP_ENABLED: bool | None = Field(default=False, description=Descriptions().aaa_remote_ip_enabled)
    AAA_SERVER_CONF: str | None = Field(default=None, description=Descriptions().aaa_server_conf)
    ACTIVE_MIGRATION: bool | None = Field(default=False)
    ADVERTISE_PIP_BGP: bool | None = Field(default=False)
    AGENT_INTF: AgentIntfEnum | None = Field(default=None, description=Descriptions().agent_intf)

    ANYCAST_BGW_ADVERTISE_PIP: bool | None = Field(default=False, description=Descriptions().anycast_bgw_advertise_pip)
    ANYCAST_GW_MAC: str | None = Field(default="2020.0000.00aa", description=Descriptions().anycast_gw_mac)
    ANYCAST_LB_ID: int | None = Field(default=10, ge=0, le=1023, description=Descriptions().anycast_lb_id)

    ANYCAST_RP_IP_RANGE: str | None = Field(default="10.254.254.0/24", description=Descriptions().anycast_rp_ip_range)
    ANYCAST_RP_IP_RANGE_INTERNAL: str | None = Field(default=None)

    AUTO_SYMMETRIC_DEFAULT_VRF: bool | None = Field(default=False)
    AUTO_SYMMETRIC_VRF_LITE: bool | None = Field(default=False)
    AUTO_VRFLITE_IFC_DEFAULT_VRF: bool | None = Field(default=False, description=Descriptions().auto_vrflite_ifc_default_vrf)

    BFD_AUTH_ENABLE: bool | None = Field(default=False)
    BFD_AUTH_KEY_ID: int | None = Field(default=100, ge=1, le=255, description=Descriptions().bfd_auth_key_id)
    BFD_AUTH_KEY: str | None = Field(default=None, min_length=1, max_length=40, description=Descriptions().bfd_auth_key)
    BFD_ENABLE: bool | None = Field(default=False, description=Descriptions().bfd_enable)
    BFD_IBGP_ENABLE: bool | None = Field(default=False, description=Descriptions().bfd_ibgp_enable)
    BFD_OSPF_ENABLE: bool | None = Field(default=False, description=Descriptions().bfd_ospf_enable)
    BFD_ISIS_ENABLE: bool | None = Field(default=False)
    BFD_PIM_ENABLE: bool | None = Field(default=False)

    BGP_AS: str = Field(index=True, description=Descriptions().bgp_as)
    BGP_AS_PREV: str | None = Field(default=None)
    BGP_AUTH_ENABLE: bool | None = Field(default=False, description=Descriptions().bgp_auth_enable)
    BGP_AUTH_KEY_TYPE: BgpAuthKeyTypeEnum | None = Field(default=BgpAuthKeyTypeEnum("3"), description=Descriptions().bgp_auth_key_type)
    BGP_AUTH_KEY: str | None = Field(default=None, min_length=1, max_length=256, description=Descriptions().bgp_auth_key)
    BGP_LB_ID: int | None = Field(default=0, ge=0, le=1023)

    BOOTSTRAP_CONF: str | None = Field(default=None, description=Descriptions().bootstrap_conf)
    BOOTSTRAP_ENABLE_PREV: bool | None = Field(default=False)
    BOOTSTRAP_ENABLE: bool | None = Field(default=False, description=Descriptions().bootstrap_enable)
    BOOTSTRAP_MULTISUBNET_INTERNAL: str | None = Field(default=None)
    BOOTSTRAP_MULTISUBNET: str | None = Field(default=Defaults().bootstrap_multisubnet, description=Descriptions().bootstrap_multisubnet)

    BRFIELD_DEBUG_FLAG: EnableDisableEnum | None = Field(default=EnableDisableEnum("Disable"), description=Descriptions().brfield_debug_flag)
    BROWNFIELD_NETWORK_NAME_FORMAT: str | None = Field(default="Auto_Net_VNI$$VNI$$_VLAN$$VLAN_ID$$")
    BROWNFIELD_SKIP_OVERLAY_NETWORK_ATTACHMENTS: bool | None = Field(default=False, description=Descriptions().brownfield_skip_overlay_network_attachments)

    CDP_ENABLE: bool | None = Field(default=False, description=Descriptions().cdp_enable)

    COPP_POLICY: CoppPolicyEnum | None = Field(default=CoppPolicyEnum("strict"), description=Descriptions().copp_policy)

    DCI_SUBNET_RANGE: str | None = Field(default="10.33.0.0/16")
    DCI_SUBNET_TARGET_MASK: int | None = Field(default=30, ge=8, le=31)

    # Yes, NDFC mispells these.
    DEAFULT_QUEUING_POLICY_CLOUDSCALE: str | None = Field(default="queuing_policy_default_8q_cloudscale", description=Descriptions().default_queuing_policy_cloudscale)
    DEAFULT_QUEUING_POLICY_OTHER: str | None = Field(default="queuing_policy_default_other", description=Descriptions().default_queuing_policy_other)
    DEAFULT_QUEUING_POLICY_R_SERIES: str | None = Field(default="queuing_policy_default_r_series", description=Descriptions().default_queuing_policy_r_series)
    DEFAULT_VRF_REDIS_BGP_RMAP: str | None = Field(default="extcon-rmap-filter", description=Descriptions().default_vrf_redis_bgp_rmap)

    DEPLOYMENT_FREEZE: bool | None = Field(default=False, description=Descriptions().deployment_freeze)

    DHCP_ENABLE: bool | None = Field(default=False, description=Descriptions().dhcp_enable)
    DHCP_END: str | None = Field(default=None, description=Descriptions().dhcp_end)
    DHCP_END_INTERNAL: str | None = Field(default=None)
    DHCP_IPV6_ENABLE_INTERNAL: str | None = Field(default=None)
    DHCP_IPV6_ENABLE: DhcpIpv6EnableEnum | None = Field(default=DhcpIpv6EnableEnum("DHCPv4"), description=Descriptions().dhcp_ipv6_enable)
    DHCP_START: str | None = Field(default=None, description=Descriptions().dhcp_start)
    DHCP_START_INTERNAL: str | None = Field(default=None)

    DNS_SERVER_IP_LIST: str | None = Field(default=None, description=Descriptions().dns_server_ip_list)
    DNS_SERVER_VRF: str | None = Field(default=None, description=Descriptions().dns_server_vrf)

    ENABLE_AAA: bool | None = Field(default=False, description=Descriptions().enable_aaa)
    ENABLE_AGENT: bool | None = Field(default=False, description=Descriptions().enable_agent)
    ENABLE_DEFAULT_QUEUING_POLICY: bool | None = Field(default=False, description=Descriptions().enable_default_queuing_policy)
    ENABLE_EVPN: bool | None = Field(default=True, description=Descriptions().enable_evpn)
    ENABLE_FABRIC_VPC_DOMAIN_ID: bool | None = Field(default=False, description=Descriptions().enable_fabric_vpc_domain_id)
    ENABLE_FABRIC_VPC_DOMAIN_ID_PREV: bool | None = Field(default=False)

    ENABLE_MACSEC: bool | None = Field(default=False, description=Descriptions().enable_macsec)
    ENABLE_NETFLOW: bool | None = Field(default=False, description=Descriptions().enable_netflow)
    ENABLE_NETFLOW_PREV: bool | None = Field(default=False)
    ENABLE_NGOAM: bool | None = Field(default=True, description=Descriptions().enable_ngoam)
    ENABLE_NXAPI_HTTP: bool | None = Field(default=True, description=Descriptions().enable_nxapi_http)
    ENABLE_NXAPI: bool | None = Field(default=True, description=Descriptions().enable_nxapi)

    ENABLE_PBR: bool | None = Field(default=False)
    ENABLE_PVLAN_PREV: bool | None = Field(default=False)
    ENABLE_PVLAN: bool | None = Field(default=False, description=Descriptions().enable_pvlan)
    ENABLE_TENANT_DHCP: bool | None = Field(default=True, description=Descriptions().enable_tenant_dhcp)
    ENABLE_TRM: bool | None = Field(default=False, description=Descriptions().enable_trm)
    ENABLE_VPC_PEER_LINK_NATIVE_VLAN: bool | None = Field(default=False, description=Descriptions().enable_vpc_peer_link_native_vlan)

    EXTRA_CONF_INTRA_LINKS: str | None = Field(default=None, description=Descriptions().extra_conf_intra_links)
    EXTRA_CONF_LEAF: str | None = Field(default=None, description=Descriptions().extra_conf_leaf)
    EXTRA_CONF_SPINE: str | None = Field(default=None, description=Descriptions().extra_conf_spine)
    EXTRA_CONF_TOR: str | None = Field(default=None, description=Descriptions().extra_conf_tor)

    FABRIC_INTERFACE_TYPE: FabricInterfaceTypeEnum | None = Field(default=FabricInterfaceTypeEnum("p2p"), description=Descriptions().fabric_interface_type)
    FABRIC_NAME: str | None = Field(default=None, primary_key=True, min_length=1, max_length=32, description=Descriptions().fabric_name)
    FABRIC_MTU: int | None = Field(default=9216, ge=576, le=9216, description=Descriptions().fabric_mtu)
    FABRIC_MTU_PREV: int | None = Field(default=9216, ge=576, le=9216)
    FABRIC_TYPE: str | None = Field(default="Switch_Fabric")
    FABRIC_VPC_QOS: bool | None = Field(default=False, description=Descriptions().fabric_vpc_qos)
    FABRIC_VPC_DOMAIN_ID: int | None = Field(default=1, ge=1, le=1000, description=Descriptions().fabric_vpc_domain_id)
    FABRIC_VPC_DOMAIN_ID_PREV: int | None = Field(default=1, ge=1, le=1000, description=Descriptions().fabric_vpc_domain_id_prev)
    FABRIC_VPC_QOS_POLICY_NAME: str | None = Field(default="spine_qos_for_fabric_vpc_peering")

    FEATURE_PTP: bool | None = Field(default=False, description=Descriptions().feature_ptp)
    FEATURE_PTP_INTERNAL: bool | None = Field(default=False)
    FF: FFEnum = Field(default="Easy_Fabric", description=Descriptions().ff)

    GRFIELD_DEBUG_FLAG: EnableDisableEnum | None = Field(default=EnableDisableEnum("Disable"), description=Descriptions().grfield_debug_flag)
    HD_TIME: int | None = Field(default=180, ge=1, le=1500, description=Descriptions().hd_time)
    IBGP_PEER_TEMPLATE: str | None = Field(default=None, description=Descriptions().ibgp_peer_template)
    IBGP_PEER_TEMPLATE_LEAF: str | None = Field(default=None, description=Descriptions().ibgp_peer_template_leaf)
    ISIS_AUTH_ENABLE: bool | None = Field(default=False)
    ISIS_AUTH_KEYCHAIN_NAME: str | None = Field(default=None, description=Descriptions().isis_auth_keychain_name)
    ISIS_LEVEL: IsisLevelEnum | None = Field(default=IsisLevelEnum("level-2"), description=Descriptions().isis_level)
    L3_PARTITION_ID_RANGE: str | None = Field(default="50000-59000")
    LOOPBACK1_IP_RANGE: str | None = Field(default="10.3.0.0/22", description=Descriptions().loopback1_ip_range)
    LOOPBACK1_IPV6_RANGE: str | None = Field(default="fd00::a03:0/118", description=Descriptions().loopback1_ipv6_range)
    MACSEC_ALGORITHM: MacsecAlgorithmEnum | None = Field(default=MacsecAlgorithmEnum("AES_128_CMAC"), description=Descriptions().macsec_algorithm)
    MACSEC_REPORT_TIMER: int | None = Field(default=5, ge=5, le=60)
    MGMT_GW_INTERNAL: str | None = Field(default=None)
    MSO_CONNECTIVITY_DEPLOYED: str | None = Field(default=None)
    MSO_SITE_ID: str | None = Field(default=None)
    OSPF_AUTH_ENABLE: bool | None = Field(default=False)
    OSPF_AUTH_KEY_ID: str | None = Field(default=None)
    PHANTOM_RP_LB_ID1: str | None = Field(default=None)
    PHANTOM_RP_LB_ID2: str | None = Field(default=None)
    PHANTOM_RP_LB_ID3: str | None = Field(default=None)
    PHANTOM_RP_LB_ID4: str | None = Field(default=None)
    PIM_HELLO_AUTH_ENABLE: bool | None = Field(default=False, description=Descriptions().pim_hello_auth_enable)
    PREMSO_PARENT_FABRIC: str | None = Field(default=None)
    PTP_DOMAIN_ID: int | None = Field(default=0, ge=0, le=127)
    REPLICATION_MODE: ReplicationModeEnum | None = Field(default="Multicast")
    ROUTER_ID_RANGE: str | None = Field(default=None, description=Descriptions().router_id_range)
    SEED_SWITCH_CORE_INTERFACES: str | None = Field(default=None, description=Descriptions().seed_switch_core_interfaces)
    SERVICE_NETWORK_VLAN_RANGE: str | None = Field(default="3000-3199", description=Descriptions().service_network_vlan_range)
    SSPINE_COUNT: int | None = Field(default=0)
    SSPINE_ADD_DEL_DEBUG_FLAG: EnableDisableEnum | None = Field(default=EnableDisableEnum("Disable"), description=Descriptions().sspine_add_del_debug_flag)
    SUBNET_TARGET_MASK: int | None = Field(default=30, ge=30, le=31, description=Descriptions().subnet_target_mask)
    TCAM_ALLOCATION: bool | None = Field(default=True, description=Descriptions().tcam_allocation)
    UNDERLAY_IS_V6: bool | None = Field(default=False)
    UNNUM_DHCP_START_INTERNAL: str | None = Field(default=None)
    UNNUM_DHCP_END_INTERNAL: str | None = Field(default=None)
    USE_LINK_LOCAL: bool | None = Field(default=False)
    VPC_ENABLE_IPv6_ND_SYNC: bool | None = Field(default=True)
    VRF_LITE_AUTOCONFIG: VrfLiteAutoconfigEnum | None = Field(default=VrfLiteAutoconfigEnum("Manual"), description=Descriptions().vrf_lite_autoconfig)
    VPC_PEER_LINK_PO: str | None = Field(default="500", description=Descriptions().vpc_peer_link_po)
    VRF_VLAN_RANGE: str | None = Field(default="2000-2299", description=Descriptions().vrf_vlan_range)


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


class NvPairs(FabricBase):
    """
    # Summary

    Defines the contents of the nvPairs object within a fabric
    response.
    """

    # id: uuid.UUID | None
    # created_at: datetime | None
    # updated_at: datetime | None


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
