#!/usr/bin/env python
from .app import app
from .db import create_db_and_tables
from .endpoints.fabric import *


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
