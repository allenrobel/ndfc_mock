#!/usr/bin/env python

from datetime import datetime, timedelta
from time import sleep

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from .db import get_session
from .main import app
from .models import Fabric


def get_timestamp_from_tz_aware_datetime_string(date_str):
    """
    # Summary

    Convert a timezone aware date to a unix timestamp.

    ## Example input (type: str)

    2025-02-13T18:31:41.162512

    ## Example output (type: float)

    1739507501.162512
    """
    print(f"type(date_str): {type(date_str)} date_str: {date_str}")
    date_format = "%Y-%m-%dT%H:%M:%S.%f"
    dt = datetime.strptime(date_str, date_format)
    dt = dt.replace(tzinfo=None)
    return dt.timestamp()


def get_timestamp_from_datetime(dt):
    """
    # Summary

    Given a datetime object, return a timestamp.
    """
    return dt.timestamp()


def convert_model_date_to_timestamp(date_obj):
    """
    # Summary

    Given a datetime object, return a unix timestamp.
    """
    return get_timestamp_from_datetime(date_obj)


def convert_db_date_to_timestamp(date_str):
    """
    # Summary

    Given a datetime string in timezone-aware format, return
    a unix timestamp.
    """
    return get_timestamp_from_tz_aware_datetime_string(date_str)


def timestamps_within_delta(ts1, ts2, delta=900000):
    """
    # Summary

    Compare two unix timestamps by converting them
    to datetime objects and using timedelta to verify
    if ts2 - ts1 <= delta microseconds.

    ## Examples

    ts1 = 1739508125.401565
    ts2 = 1739508125.403565
    delta = 403565 - 401565
    result = timestamps_within_delta(ts1, ts2, delta=delta) # True
    result = timestamps_within_delta(ts1, ts2, delta=delta-1) # False

    Return True if delta is <= delta microseconds.
    Return False otherwise.
    """
    print(f"timestamps_within_delta: ts1: {ts1}")
    print(f"timestamps_within_delta: ts2: {ts2}")
    dt1 = datetime.fromtimestamp(ts1)
    dt2 = datetime.fromtimestamp(ts2)
    print(f"dt2 - dt1: {dt2 - dt1}")
    return dt2 - dt1 <= timedelta(microseconds=delta)


@pytest.fixture(name="session")
def session_fixture():
    """
    # Summary

    Return a SQLModel Session() instance that interacts with an in-memory
    database.
    """
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """
    # Summary

    yield a FastAPI TestClient() instance.

    After the calling test case completes, execution continues
    after the yield statement to clear the SQLModel Session.
    """

    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_post_fabric(client: TestClient):
    """
    # Summary

    Verify a successful POST request.
    """
    response = client.post(
        "/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/f1/Easy_Fabric",
        json={"asn": "65001"},
    )
    data = response.json()

    assert response.status_code == 200
    assert data["fabricName"] == "f1"
    assert data["asn"] == "65001"
    assert data["created_at"] is not None
    assert data["updated_at"] is not None


def test_post_fabric_incomplete(client: TestClient):
    """
    # Summary

    Verify an unsuccessful POST request.

    A 422 status_code is returned when the asn is missing from the body
    of the POST request.
    """
    response = client.post(
        "/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/f1/Easy_Fabric",
        json={},
    )
    assert response.status_code == 422


def test_post_fabric_invalid(client: TestClient):
    """
    # Summary

    Verify an unsuccessful POST request.

    A 422 status_code is returned when the asn is an invalid type in the body
    of the POST request.
    """
    response = client.post(
        "/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/f1/Easy_Fabric",
        json={"asn": 65001},
    )
    assert response.status_code == 422


def test_get_fabrics(session: Session, client: TestClient):
    """
    # Summary

    Verify GET request for all fabrics.

    1. Create two fabrics.
    2. Store their created_at and updated_at fields for later comparison
    3. Commit the fabrics.
    4. Send a GET request to retrieve all fabrics.
    5. Verify response
        -   status_code == 200
        -   asn == expected asn
        -   fabricName == expected fabricName
    6. Convert the created_at and updated_at fields to timestamps.
    7. Verify the created_at field
        -   created_at field has 0 delta between step 2 version
            and retrieved version.
    8. Verify the updadted_at field
        -   updated_at field is present and the step 2 version
            timestamp differs from the retrieved version timestamp.
    """
    f1 = Fabric(fabricName="f1", asn="65001")
    f2 = Fabric(fabricName="f2", asn="65002")

    # Convert naive (timezone unaware) data model dates to
    # unix timestamps for comparison with dates in the database
    model_created_at_ts_f1 = convert_model_date_to_timestamp(f1.created_at)
    model_created_at_ts_f2 = convert_model_date_to_timestamp(f2.created_at)
    model_updated_at_ts_f1 = convert_model_date_to_timestamp(f1.updated_at)
    model_updated_at_ts_f2 = convert_model_date_to_timestamp(f2.updated_at)

    # commit the two fabrics
    for fabric in [f1, f2]:
        session.add(fabric)
        session.commit()

    response = client.get(
        "/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics"
    )
    data = response.json()

    # Compare the easy stuff first
    assert response.status_code == 200
    assert len(data) == 2
    assert data[0]["fabricName"] == f1.fabricName
    assert data[0]["asn"] == f1.asn

    assert data[1]["fabricName"] == f2.fabricName
    assert data[1]["asn"] == f2.asn

    # Convert timezone aware dates from the database to
    # unix timestamps for comparison with data model dates
    db_created_at_ts_f1 = convert_db_date_to_timestamp(data[0]["created_at"])
    db_created_at_ts_f2 = convert_db_date_to_timestamp(data[1]["created_at"])
    db_updated_at_ts_f1 = convert_db_date_to_timestamp(data[0]["updated_at"])
    db_updated_at_ts_f2 = convert_db_date_to_timestamp(data[1]["updated_at"])

    # Compare the model timestamps with the database timestamps
    assert timestamps_within_delta(model_created_at_ts_f1, db_created_at_ts_f1, delta=0)
    assert timestamps_within_delta(model_created_at_ts_f2, db_created_at_ts_f2, delta=0)
    assert timestamps_within_delta(model_updated_at_ts_f1, db_updated_at_ts_f1)
    assert timestamps_within_delta(model_updated_at_ts_f2, db_updated_at_ts_f2)


def test_get_fabric_by_name(session: Session, client: TestClient):
    """
    # Summary

    Verify GET request with fabric_name in the path.

    1. Create fabric
    2. Send GET request with fabric_name in the path.
    3. Verify the response
        -   status_code == 200
        -   asn == expected asn
        -   created_at field is present and not None
        -   updated_at field is present and not None
    """
    f1 = Fabric(fabricName="f1", asn="65001")
    session.add(f1)
    session.commit()

    response = client.get(
        f"/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{f1.fabricName}"
    )
    data = response.json()

    assert response.status_code == 200
    assert data["fabricName"] == f1.fabricName
    assert data["asn"] == f1.asn
    assert data["created_at"] is not None
    assert data["updated_at"] is not None


def test_put_fabric(session: Session, client: TestClient):
    """
    # Summary

    Verify PUT request.

    1. asn is updated
    2. updated_at is updated with new timestamp
       2a. updated_at pre-update is not identical to post-update (delta=0)
       2b. updated_at post-update is <= 2 seconds later than pre-update
    """
    f1 = Fabric(fabricName="f1", asn="65001")
    session.add(f1)
    model_updated_at_ts = convert_model_date_to_timestamp(f1.updated_at)
    session.commit()
    sleep(1)

    response = client.put(
        "/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/f1/Easy_Fabric",
        json={"asn": "65111"},
    )
    data = response.json()

    assert response.status_code == 200
    assert data["fabricName"] == "f1"
    assert data["asn"] == "65111"
    assert data["created_at"] is not None
    assert data["updated_at"] is not None
    db_updated_at_ts = convert_db_date_to_timestamp(data["updated_at"])

    assert (
        timestamps_within_delta(model_updated_at_ts, db_updated_at_ts, delta=0) is False
    )
    assert (
        timestamps_within_delta(model_updated_at_ts, db_updated_at_ts, delta=2000000)
        is True
    )


def test_delete_fabric(session: Session, client: TestClient):
    """
    # Summary

    1. Create fabric
    2. Delete fabric

    Verify that fabric is deleted with 200 status_code.
    """
    f1 = Fabric(fabricName="f1", asn="65001")
    session.add(f1)
    session.commit()

    response = client.delete(
        f"/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{f1.fabricName}"
    )
    fabric_in_db = session.get(Fabric, f1.fabricName)

    assert response.status_code == 200

    assert fabric_in_db is None
