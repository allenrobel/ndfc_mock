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

## Installation

```bash
git clone https://github.com/allenrobel/ndfc_mock.git
cd ndfc_mock
podman build -t ndfc .
podman run --detach -p 8080:80 ndfc_mock
```

After the container starts, point your browser at 
[http://localhost:8080/docs](http://localhost:8080/docs)
for the API documentation.  You can use e.g. Postman for
sending requests to the mock NDFC instance.
