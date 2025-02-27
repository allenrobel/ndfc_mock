#!/usr/bin/env python
import copy
import json
import uuid

from ...app import app
from ..models.fm_about_version import V1FmAboutVersionResponseModel


def build_response():
    """
    # Summary

    Build a response that aligns with the ResponseModel

    ## Notes

    1. If V1FmAboutVersionResponseModel is changed, this function must also be updated
    """
    response = {}
    response["version"] = "12.1.2e"
    response["mode"] = "LAN"
    response["isMediaController"] = False
    response["dev"] = False
    response["isHaEnabled"] = False
    response["install"] = "EASYFABRIC"
    response["uuid"] = f"{uuid.uuid4()}"
    response["is_upgrade_inprogress"] = False
    return copy.deepcopy(response)


@app.get(
    "/appcenter/cisco/ndfc/api/v1/fm/about/version",
    response_model=V1FmAboutVersionResponseModel,
)
def get_v1_fm_about_version():
    """
    # Summary

    GET request handler.
    """
    response = build_response()
    print(f"v1_fm_about_version: response: {json.dumps(response, indent=4, sort_keys=True)}")
    return response
