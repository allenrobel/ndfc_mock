# Summary

Work in progress!

This is not complete and in no way emulates NDFC currently.

When finished, this will (hopefully) allow for minor development 
and testing of ansible-dcnm modules (and other REST API-based 
applications) without requiring a real ND/NDFC instance.

Basically, it will accept GET/POST/PUT/DELETE requests to
endpoints supported by NDFC and will return mock responses.

## Podman

This is being built to run in a container using Podman,
but Docker should also work (though I'm not using Docker 
so no guarantees).

You can also run it outside the container if you install the dependencies
(described in `Installation - No Container` below.)

## Installation - Container

To run ndfc_mock within a container.

```bash
git clone https://github.com/allenrobel/ndfc_mock.git
cd ndfc_mock
podman build -t ndfc_mock .
podman run --detach -p 8080:80 ndfc_mock
```

After the container starts, point your browser at 
[http://localhost:8080/docs](http://localhost:8080/docs)
for the API documentation.  You can use e.g. Postman for
sending requests to the mock NDFC instance.

## Installation - No Container

To run run ndfc_mock outside of a container.

```bash
git clone https://github.com/allenrobel/ndfc_mock.git
cd ndfc_mock
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd app
fastapi run main.py
```

You'll see the uvicorn server startup.  The last two lines will look like:

```bash
      INFO   Application startup complete.
      INFO   Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

Point your browser at 
[http://localhost:8000/docs](http://localhost:8000/docs)
for the API documentation.  You can use e.g. Postman for
sending requests to the uvicorn site.

Note: Running outside of a container will result in
database.db being created in the ./app directory.
