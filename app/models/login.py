#!/usr/bin/env python
# TODO: If SQLModel is ever fixed, remove the mypy directive below.
# https://github.com/fastapi/sqlmodel/discussions/732
# mypy: disable-error-code=call-arg
from typing import Any, List

from pydantic import BaseModel
from sqlmodel import Field


class LoginRBAC(BaseModel):
    """
    # Summary

    Validator for the RBAC portion of the login response.
    """

    domain: str = Field(default="all")
    rolesR: int = Field(default=16777216)
    rolesW: int = Field(default=1)
    roles: List[List[Any]]


class LoginResponseModel(BaseModel):
    """
    # Summary

    Describes what is returned to clients.
    """

    jwttoken: str
    username: str
    usertype: str
    rbac: List[LoginRBAC]
    statusCode: int
    token: str
