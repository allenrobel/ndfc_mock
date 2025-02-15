# Summary

Work in progress!

This is not complete and in no way emulates NDFC currently.

When finished, this will (hopefully) allow for minor development and testing
of ansible-dcnm modules (and other REST API-based applicatioins) without
having to interact with a real ND/NDFC instance.

Basically, it will accept GET/POST/PUT/DELETE requests to endpoints
supported by NDFC and will return mock responses.

## Podman

This is being built using Podman, but Docker should also work
(though I'm not using Docker so no guarantees).