#!/usr/bin/env python

from datetime import datetime, timedelta
import pytest
from time import sleep

from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from .db import get_session
from .main import app
from .models import Hero

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
    date_format = f"%Y-%m-%dT%H:%M:%S.%f"
    dt = datetime.strptime(date_str, date_format)
    dt = dt.replace(tzinfo=None)
    return dt.timestamp()

def get_timestamp_from_datetime(dt):
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
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_create_hero(client: TestClient):
    response = client.post(
        "/heroes/", json={"name": "Deadpond", "secret_name": "Dive Wilson"}
    )
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "Deadpond"
    assert data["secret_name"] == "Dive Wilson"
    assert data["age"] is None
    assert data["id"] is not None
    assert data["created_at"] is not None
    assert data["updated_at"] is not None


def test_create_hero_incomplete(client: TestClient):
    # No secret_name
    response = client.post("/heroes/", json={"name": "Deadpond"})
    assert response.status_code == 422


def test_create_hero_invalid(client: TestClient):
    # secret_name has an invalid type
    response = client.post(
        "/heroes/",
        json={
            "name": "Deadpond",
            "secret_name": {"message": "Do you wanna know my secret identity?"},
        },
    )
    assert response.status_code == 422


def test_read_heroes(session: Session, client: TestClient):
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    hero_2 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)

    # Convert naive (timezone unaware) data model dates to
    # unix timestamps for comparison with dates in the database
    model_created_at_ts_hero_1 = convert_model_date_to_timestamp(hero_1.created_at)
    model_created_at_ts_hero_2 = convert_model_date_to_timestamp(hero_2.created_at)
    model_updated_at_ts_hero_1 = convert_model_date_to_timestamp(hero_1.updated_at)
    model_updated_at_ts_hero_2 = convert_model_date_to_timestamp(hero_2.updated_at)

    # commit the two heros
    session.add(hero_1)
    session.add(hero_2)
    session.commit()

    response = client.get("/heroes/")
    data = response.json()

    # Compare the easy stuff first
    assert response.status_code == 200
    assert len(data) == 2
    assert data[0]["name"] == hero_1.name
    assert data[0]["secret_name"] == hero_1.secret_name
    assert data[0]["age"] == hero_1.age
    assert data[0]["id"] == f"{hero_1.id}"

    assert data[1]["name"] == hero_2.name
    assert data[1]["secret_name"] == hero_2.secret_name
    assert data[1]["age"] == hero_2.age
    assert data[1]["id"] == f"{hero_2.id}"

    # Convert timezone aware dates from the database to
    # unix timestamps for comparison with data model dates
    db_created_at_ts_hero_1 = convert_db_date_to_timestamp(data[0]['created_at'])
    db_created_at_ts_hero_2 = convert_db_date_to_timestamp(data[1]['created_at'])
    db_updated_at_ts_hero_1 = convert_db_date_to_timestamp(data[0]['updated_at'])
    db_updated_at_ts_hero_2 = convert_db_date_to_timestamp(data[1]['updated_at'])

    # Compare the model timestamps with the database timestamps
    assert timestamps_within_delta(model_created_at_ts_hero_1, db_created_at_ts_hero_1, delta=0)
    assert timestamps_within_delta(model_created_at_ts_hero_2, db_created_at_ts_hero_2)
    assert timestamps_within_delta(model_updated_at_ts_hero_1, db_updated_at_ts_hero_1)
    assert timestamps_within_delta(model_updated_at_ts_hero_2, db_updated_at_ts_hero_2)


def test_read_hero(session: Session, client: TestClient):
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    session.add(hero_1)
    session.commit()

    response = client.get(f"/heroes/{hero_1.id}")
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == hero_1.name
    assert data["secret_name"] == hero_1.secret_name
    assert data["age"] == hero_1.age
    assert data["id"] == f"{hero_1.id}"
    assert data["created_at"] is not None
    assert data["updated_at"] is not None


def test_update_hero(session: Session, client: TestClient):
    """
    Verify that an update works.

    1. name is updated
    2. updated_at is updated with new timestamp
       2a. updated_at pre-update is not identical to post-update (delta=0)
       2b. updated_at post-update is <= 2 seconds later than pre-update
    """
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    session.add(hero_1)
    model_updated_at_ts = convert_model_date_to_timestamp(hero_1.updated_at)
    session.commit()
    sleep(1)

    response = client.patch(f"/heroes/{hero_1.id}", json={"name": "Deadpuddle"})
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "Deadpuddle"
    assert data["secret_name"] == "Dive Wilson"
    assert data["age"] is None
    assert data["id"] == f"{hero_1.id}"
    assert data["created_at"] is not None
    assert data["updated_at"] is not None
    db_updated_at_ts = convert_db_date_to_timestamp(data["updated_at"])

    assert timestamps_within_delta(model_updated_at_ts, db_updated_at_ts, delta=0) is False
    assert timestamps_within_delta(model_updated_at_ts, db_updated_at_ts, delta=2000000) is True


def test_delete_hero(session: Session, client: TestClient):
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    session.add(hero_1)
    session.commit()

    response = client.delete(f"/heroes/{hero_1.id}")

    hero_in_db = session.get(Hero, hero_1.id)

    assert response.status_code == 200

    assert hero_in_db is None
