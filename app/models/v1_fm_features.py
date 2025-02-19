#!/usr/bin/env python
# TODO: If SQLModel is ever fixed, remove the mypy directive below.
# https://github.com/fastapi/sqlmodel/discussions/732
# mypy: disable-error-code=call-arg

from pydantic import BaseModel
from sqlmodel import Field


class V1FmFeaturesBase(BaseModel):
    """
    # Summary

    Base class for all other classes in this file.
    """

    status: str = Field(default="success")
    data: dict


class V1FmFeaturesResponseModel(V1FmFeaturesBase):
    """
    # Summary

    Describes what is returned to clients.
    """
