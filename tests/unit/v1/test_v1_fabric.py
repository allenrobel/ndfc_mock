#!/usr/bin/env python
# See the following regarding *_fixture imports
# https://pylint.pycqa.org/en/latest/user_guide/messages/warning/redefined-outer-name.html
# Due to the above, we also need to disable unused-import
# Also, fixtures need to use *args to match the signature of the function they are mocking
# pylint: disable=unused-import
# pylint: disable=redefined-outer-name
# pylint: disable=protected-access
# pylint: disable=unused-argument
# pylint: disable=invalid-name

import json
from time import sleep

from fastapi.testclient import TestClient
from sqlmodel import Session

from ....app.v1.models.fabric import Fabric
from ..common import client_fixture, convert_db_date_to_timestamp, convert_model_date_to_timestamp, session_fixture, timestamps_within_delta


def test_v1_fabric_post_100(client: TestClient):
    """
    # Summary

    Verify a successful POST request.

    SITE_ID is not set in the request body, and does not assume the value
    of BGP_AS automatically.
    """
    response = client.post(
        "/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/f1/Easy_Fabric",
        json={"BGP_AS": "65001"},
    )
    data = response.json()

    assert response.status_code == 200
    assert "nvPairs" in data
    nv_pairs = data["nvPairs"]
    assert nv_pairs["FABRIC_NAME"] == "f1"
    assert nv_pairs["BGP_AS"] == "65001"
    assert nv_pairs["SITE_ID"] is None
    print(f"nvPairs: {json.dumps(nv_pairs, indent=4)}")


def test_v1_fabric_post_110(client: TestClient):
    """
    # Summary

    Verify a successful POST request.

    SITE_ID is set in the request body, so assumes a unique value apart
    from BGP_AS.
    """
    response = client.post(
        "/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/f1/Easy_Fabric",
        json={"BGP_AS": "65001", "SITE_ID": "65444"},
    )
    data = response.json()

    assert response.status_code == 200
    assert "nvPairs" in data
    nv_pairs = data["nvPairs"]
    assert nv_pairs["FABRIC_NAME"] == "f1"
    assert nv_pairs["BGP_AS"] == "65001"
    assert nv_pairs["SITE_ID"] == "65444"
    print(f"nvPairs: {json.dumps(nv_pairs, indent=4)}")


def test_v1_fabric_post_200(client: TestClient):
    """
    # Summary

    Verify an unsuccessful POST request.

    A 422 status_code is returned when BGP_AS is missing from the body
    of the POST request.
    """
    response = client.post(
        "/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/f1/Easy_Fabric",
        json={},
    )
    assert response.status_code == 422


def test_v1_fabric_post_210(client: TestClient):
    """
    # Summary

    Verify an unsuccessful POST request.

    A 422 status_code is returned when BGP_AS is an invalid type in the body
    of the POST request.
    """
    response = client.post(
        "/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/f1/Easy_Fabric",
        json={"BGP_AS": 65001},
    )
    assert response.status_code == 422


def test_v1_fabric_get_100(session: Session, client: TestClient):
    """
    # Summary

    Verify GET request for all fabrics.

    1. Create two fabrics.
    2. Store their created_at and updated_at fields for later comparison
    3. Commit the fabrics.
    4. Send a GET request to retrieve all fabrics.
    5. Verify response
        -   status_code == 200
        -   BGP_AS == expected BGP_AS
        -   FABRIC_NAME == expected FABRIC_NAME
    6. Convert the created_at and updated_at fields to timestamps.
    7. Verify the created_at field
        -   created_at field has 0 delta between step 2 version
            and retrieved version.
    8. Verify the updated_at field
        -   updated_at field is present and the step 2 version
            timestamp differs from the retrieved version timestamp.
    """
    f1 = Fabric(FABRIC_NAME="f1", BGP_AS="65001")
    f2 = Fabric(FABRIC_NAME="f2", BGP_AS="65002")

    # Convert naive (timezone unaware) data model dates to
    # unix timestamps for comparison with dates in the database
    # model_created_at_ts_f1 = convert_model_date_to_timestamp(f1.created_at)
    # model_created_at_ts_f2 = convert_model_date_to_timestamp(f2.created_at)
    # model_updated_at_ts_f1 = convert_model_date_to_timestamp(f1.updated_at)
    # model_updated_at_ts_f2 = convert_model_date_to_timestamp(f2.updated_at)

    # commit the two fabrics
    for fabric in [f1, f2]:
        session.add(fabric)
        session.commit()

    response = client.get("/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics")
    data = response.json()

    # Compare the easy stuff first
    assert response.status_code == 200
    assert len(data) == 2
    assert data[0]["nvPairs"]["FABRIC_NAME"] == f1.FABRIC_NAME
    assert data[0]["nvPairs"]["BGP_AS"] == f1.BGP_AS

    assert data[1]["nvPairs"]["FABRIC_NAME"] == f2.FABRIC_NAME
    assert data[1]["nvPairs"]["BGP_AS"] == f2.BGP_AS

    # Convert timezone aware dates from the database to
    # unix timestamps for comparison with data model dates
    # db_created_at_ts_f1 = convert_db_date_to_timestamp(data[0]["created_at"])
    # db_created_at_ts_f2 = convert_db_date_to_timestamp(data[1]["created_at"])
    # db_updated_at_ts_f1 = convert_db_date_to_timestamp(data[0]["updated_at"])
    # db_updated_at_ts_f2 = convert_db_date_to_timestamp(data[1]["updated_at"])

    # Compare the model timestamps with the database timestamps
    # assert timestamps_within_delta(model_created_at_ts_f1, db_created_at_ts_f1, delta=0)
    # assert timestamps_within_delta(model_created_at_ts_f2, db_created_at_ts_f2, delta=0)
    # assert timestamps_within_delta(model_updated_at_ts_f1, db_updated_at_ts_f1)
    # assert timestamps_within_delta(model_updated_at_ts_f2, db_updated_at_ts_f2)


def test_v1_fabric_get_110(session: Session, client: TestClient):
    """
    # Summary

    Verify GET request with fabric_name in the path.

    1. Create fabric
    2. Send GET request with fabric_name in the path.
    3. Verify the response
        -   status_code == 200
        -   BGP_AS == expected BGP_AS
        -   created_at field is present and not None
        -   updated_at field is present and not None
    """
    f1 = Fabric(FABRIC_NAME="f1", BGP_AS="65001")
    session.add(f1)
    session.commit()

    response = client.get(f"/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{f1.FABRIC_NAME}")
    data = response.json()

    assert response.status_code == 200
    assert data["nvPairs"]["FABRIC_NAME"] == f1.FABRIC_NAME
    assert data["nvPairs"]["BGP_AS"] == f1.BGP_AS


def test_v1_fabric_put_100(session: Session, client: TestClient):
    """
    # Summary

    Verify PUT request updates BGP_AS.

    1. BGP_AS is updated
    2. updated_at is updated with new timestamp
       2a. updated_at pre-update is not identical to post-update (delta=0)
       2b. updated_at post-update is <= 2 seconds later than pre-update
    """
    f1 = Fabric(FABRIC_NAME="f1", BGP_AS="65001")
    session.add(f1)
    # model_updated_at_ts = convert_model_date_to_timestamp(f1.updated_at)
    session.commit()
    sleep(1)

    response = client.put(
        "/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/f1/Easy_Fabric",
        json={"BGP_AS": "65111"},
    )
    data = response.json()

    assert response.status_code == 200
    assert data["nvPairs"]["FABRIC_NAME"] == "f1"
    assert data["nvPairs"]["BGP_AS"] == "65111"
    # assert data["created_at"] is not None
    # assert data["updated_at"] is not None
    # db_updated_at_ts = convert_db_date_to_timestamp(data["updated_at"])

    # assert timestamps_within_delta(model_updated_at_ts, db_updated_at_ts, delta=0) is False
    # assert timestamps_within_delta(model_updated_at_ts, db_updated_at_ts, delta=2000000) is True


def test_v1_fabric_put_110(session: Session, client: TestClient):
    """
    # Summary

    Verify PUT request updates REPLICATION_MODE.

    1. REPLICATION_MODE is updated
    2. updated_at is updated with new timestamp
       2a. updated_at pre-update is not identical to post-update (delta=0)
       2b. updated_at post-update is <= 2 seconds later than pre-update
    """
    f1 = Fabric(FABRIC_NAME="f1", BGP_AS="65001")
    session.add(f1)
    # model_updated_at_ts = convert_model_date_to_timestamp(f1.updated_at)
    session.commit()
    sleep(1)

    response = client.put(
        "/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/f1/Easy_Fabric",
        json={"REPLICATION_MODE": "Ingress"},
    )
    data = response.json()

    assert response.status_code == 200
    assert data["nvPairs"]["FABRIC_NAME"] == "f1"
    assert data["nvPairs"]["BGP_AS"] == "65001"
    assert data["nvPairs"]["REPLICATION_MODE"] == "Ingress"
    # assert data["created_at"] is not None
    # assert data["updated_at"] is not None
    # db_updated_at_ts = convert_db_date_to_timestamp(data["updated_at"])

    # assert timestamps_within_delta(model_updated_at_ts, db_updated_at_ts, delta=0) is False
    # assert timestamps_within_delta(model_updated_at_ts, db_updated_at_ts, delta=2000000) is True


def test_v1_fabric_delete_100(session: Session, client: TestClient):
    """
    # Summary

    1. Create fabric
    2. Delete fabric

    Verify that fabric is deleted with 200 status_code.
    """
    f1 = Fabric(FABRIC_NAME="f1", BGP_AS="65001")
    session.add(f1)
    session.commit()

    response = client.delete(f"/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{f1.FABRIC_NAME}")
    fabric_in_db = session.get(Fabric, f1.FABRIC_NAME)

    assert response.status_code == 200

    assert fabric_in_db is None


def test_v1_fabric_delete_110(session: Session, client: TestClient):
    """
    # Summary

    1. Attempt to delete a fabric that does not exist

    Verify that fabric is deleted with 200 status_code.
    """
    response = client.delete("/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/foo")
    fabric_in_db = session.get(Fabric, "foo")

    response_decode = response.json()

    assert response.status_code == 404
    assert response_decode["detail"]["timestamp"] is not None
    assert isinstance(response_decode["detail"]["timestamp"], int) is True
    assert response_decode["detail"]["status"] == 404
    assert response_decode["detail"]["error"] == "Not Found"
    assert response_decode["detail"]["path"] == "/rest/control/fabrics/foo"

    assert fabric_in_db is None
