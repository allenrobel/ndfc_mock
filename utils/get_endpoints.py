#!/usr/bin/env python
"""
# Summary

Retrieve all endpoints from an OpenAPI schema and format them for
use in the README.md file.
"""
import requests


def get_endpoints(url: str) -> dict:
    """
    # Summary

    Issue a GET request for the url and return the JSON response.
    """
    response = requests.get(url, timeout=5)
    return response.json()


def main():
    """
    # Summary

    Retrieve all endpoints from an OpenAPI schema, and print them to the
    console; formatted for use in the README.md file in this repository.
    """
    url = "http://localhost:8000/openapi.json"

    data = get_endpoints(url)
    endpoints = data["paths"]

    for path, info in endpoints.items():
        print(f"- `{path}`")
        for method, method_info in info.items():
            print(f"  - `{method}`")
            print(f"    - {method_info.get('summary')}")


if __name__ == "__main__":
    main()
