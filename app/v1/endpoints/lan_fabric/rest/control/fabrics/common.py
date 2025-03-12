import copy


def build_nv_pairs(fabric):
    """
    # Summary

    Build the nvPairs object in a fabric response.
    """
    return fabric.model_dump()


def build_response(fabric):
    """
    # Summary

    Build a fabric response that aligns with FabricResponseModel

    ## Notes

    1. If FabricResponseModel is changed, this function must also be updated
    """
    response = {}
    response["id"] = fabric.id
    response["nvPairs"] = build_nv_pairs(fabric)
    return copy.deepcopy(response)
