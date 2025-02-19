#!/usr/bin/env python
import copy
import json

from ..app import app
from ..models.v1_configtemplate_easy_fabric import V1ConfigtemplateEasyFabricResponseModel


def build_bgp_as():
    """
    # Summary

    Build the template BGP_AS object
    """
    d = {}
    d["name"] = "BGP_AS"
    d["description"] = None
    d["parameterType"] = "string"
    d["metaProperties"] = {}
    d["metaProperties"]["minLength"] = "1"
    d["metaProperties"]["minLength"] = "11"
    regularExpr = "^(((\\+)?[1-9]{1}[0-9]{0,8}|(\\+)?[1-3]{1}[0-9]{1,9}"
    regularExpr += "|(\\+)?[4]{1}([0-1]{1}[0-9]{8}|[2]{1}([0-8]{1}[0-9]{7}|"
    regularExpr += "[9]{1}([0-3]{1}[0-9]{6}|[4]{1}([0-8]{1}[0-9]{5}"
    regularExpr += "|[9]{1}([0-5]{1}[0-9]{4}|[6]{1}([0-6]{1}[0-9]{3}"
    regularExpr += "|[7]{1}([0-1]{1}[0-9]{2}|[2]{1}([0-8]{1}[0-9]{1}"
    regularExpr += "|[9]{1}[0-5]{1})))))))))|([1-5]\\d{4}|[1-9]\\d{0,3}"
    regularExpr += "|6[0-4]\\d{3}|65[0-4]\\d{2}|655[0-2]\\d|6553[0-5])"
    regularExpr += "(\\.([1-5]\\d{4}|[1-9]\\d{0,3}|6[0-4]\\d{3}|65[0-4]\\d{2}|"
    regularExpr += "655[0-2]\\d|6553[0-5]|0))?)$"
    d["metaProperties"]["regularExpr"] = regularExpr
    d["annotations"] = {}
    d["annotations"]["DisplayName"] = "BGP ASN"
    d["annotations"]["Description"] = "1-4294967295 | 1-65535[.0-65535]<br />It is a good practice to have a unique ASN for each Fabric."
    d["annotations"]["IsAsn"] = True
    d["annotations"]["IsMandatory"] = True
    d["structureParameters"] = {}
    d["parameterTypeStructure"] = False
    d["defaultValue"] = None
    d["optional"] = False
    return copy.deepcopy(d)


def build_fabric_name():
    """
    # Summary

    Build the template FABRIC_NAME object
    """
    d = {}
    d["name"] = "FABRIC_NAME"
    d["description"] = None
    d["parameterType"] = "string"
    d["metaProperties"] = {}
    d["metaProperties"]["minLength"] = "1"
    d["metaProperties"]["minLength"] = "32"
    d["annotations"] = {}
    d["annotations"]["DisplayName"] = "Fabric Name"
    d["annotations"]["Description"] = "Please provide the fabric name to create it (Max Size 32)"
    d["annotations"]["IsMandatory"] = True
    d["annotations"]["IsFabricName"] = True
    d["structureParameters"] = {}
    d["parameterTypeStructure"] = False
    d["defaultValue"] = None
    d["optional"] = False
    return copy.deepcopy(d)


def build_fabric_type():
    """
    # Summary

    Build the template FABRIC_TYPE object
    """
    d = {}
    d["name"] = "FABRIC_TYPE"
    d["description"] = None
    d["parameterType"] = "string"
    d["metaProperties"] = {}
    d["metaProperties"]["defaultValue"] = "Switch_Fabric"
    d["annotations"] = {}
    d["annotations"]["ReadOnly"] = True
    d["annotations"]["DisplayName"] = "Fabric Type"
    d["annotations"]["IsFabricType"] = True
    d["annotations"]["IsMandatory"] = True
    d["annotations"]["Section"] = '"Hidden"'
    d["structureParameters"] = {}
    d["parameterTypeStructure"] = False
    d["defaultValue"] = None
    d["optional"] = False
    return copy.deepcopy(d)


def build_replication_mode():
    """
    # Summary

    Build the template REPLICATION_MODE object
    """
    d = {}
    d["name"] = "REPLICATION_MODE"
    d["description"] = None
    d["parameterType"] = "string"
    d["metaProperties"] = {}
    d["metaProperties"]["defaultValue"] = "Multicast"
    d["annotations"] = {}
    d["annotations"]["Enum"] = "Multicast,Ingress"
    d["annotations"]["Description"] = "Replication Mode for BUM Traffic"
    d["annotations"]["IsMandatory"] = True
    d["annotations"]["DisplayName"] = "Replication Mode"
    d["annotations"]["IsShow"] = '"UNDERLAY_IS_V6!=true"'
    d["annotations"]["IsReplicationMode"] = True
    d["annotations"]["Section"] = '"Replication"'
    d["structureParameters"] = {}
    d["parameterTypeStructure"] = False
    d["defaultValue"] = None
    d["optional"] = False
    return copy.deepcopy(d)


def build_response():
    """
    # Summary

    Build a response that aligns with the ResponseModel

    ## Notes

    1. If V1FmAboutVersionResponseModel is changed, this function must also be updated
    """
    response = {}
    response["instanceClassId"] = 1000
    response["assignedInstanceClassId"] = 0
    response["instanceName"] = "com.cisco.dcbu.dcm.model.cfgtemplate.ConfigTemplate:name=Easy_Fabric:type=true"
    response["name"] = "Easy_Fabric"
    response["description"] = "Fabric for a VXLAN EVPN deployment with Nexus 9000 and 3000 switches."
    response["userDefined"] = True
    response["parameters"] = []
    response["parameters"].append(build_bgp_as())
    response["parameters"].append(build_fabric_name())
    response["parameters"].append(build_fabric_type())
    response["parameters"].append(build_replication_mode())
    response["content"] = "##template ..."
    return copy.deepcopy(response)


@app.get(
    "/appcenter/cisco/ndfc/api/v1/configtemplate/rest/config/templates/Easy_Fabric",
    response_model=V1ConfigtemplateEasyFabricResponseModel,
)
def get_v1_configtemplate_easy_fabric():
    """
    # Summary

    GET request handler.
    """
    response = build_response()
    print(f"get_v1_configtemplate_easy_fabric: response: {json.dumps(response, indent=4, sort_keys=True)}")
    return response
