#!/usr/bin/env python
import json

from fastapi import HTTPException

from ..app import app
from ..models.v1_configtemplate_easy_fabric import V1ConfigtemplateEasyFabricResponseModel


@app.get(
    "/appcenter/cisco/ndfc/api/v1/configtemplate/rest/config/templates/{template_name}",
    response_model=V1ConfigtemplateEasyFabricResponseModel,
)
def get_v1_configtemplate_by_name(template_name: str):
    """
    # Summary

    GET request handler.
    """
    try:
        with open(f"./templates/{template_name}.json", "r", encoding="utf-8") as template:
            response = json.load(template)
    except FileNotFoundError as error:
        raise HTTPException(status_code=404, detail=f"Template {template_name} not found.") from error
    return response
