#!/usr/bin/env python
import copy
import json

from ...app import app
from ..models.login import LoginResponseModel


def build_rbac():
    """
    # Summary

    Build the RBAC portion of the response
    """
    rbac = {}
    rbac["domain"] = "local"
    rbac["rolesR"] = 16777216
    rbac["rolesW"] = 1
    rbac["roles"] = []
    rbac["roles"].append(["admin", "WritePriv"])
    rbac["roles"].append(["app-user", "ReadPriv"])
    return rbac


def build_response():
    """
    # Summary

    Build a login response that aligns with LoginResponseModel

    ## Notes

    1. If LoginResponseModel is changed, this function must also be updated
    """
    response = {}
    response["jwttoken"] = "asdlfkjasdf"
    response["username"] = "admin"
    response["usertype"] = "local"
    response["rbac"] = [build_rbac()]
    response["statusCode"] = 200
    response["token"] = "asdlfkjasdf"
    return copy.deepcopy(response)


@app.post(
    "/login",
    response_model=LoginResponseModel,
)
def post_login():
    """
    # Summary

    POST request handler
    """
    response = build_response()
    print(f"post_login: {json.dumps(response, indent=4, sort_keys=True)}")
    return response
