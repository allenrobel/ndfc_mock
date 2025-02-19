# Summary

Work in progress!

When finished, this will (hopefully) allow for minor development 
and testing of [ansible-dcnm](https://github.com/CiscoDevNet/ansible-dcnm)
modules (and other REST API-based applications) without requiring a
real ND/NDFC instance.

Basically, it will accept GET/POST/PUT/DELETE requests to
endpoints supported by NDFC and will return mock responses.

## Current status

Running a basic merged-state dcnm_fabric playbook against the mock
instance is working (it creates a fabric with the following very
minimal configuration).

```yaml
---
-   hosts: ndfc
    check_mode: false
    gather_facts: false
    tasks:
    - name: Create VXLAN Fabric
      cisco.dcnm.dcnm_fabric:
        state: merged
        config:
        -   FABRIC_NAME: f1
            FABRIC_TYPE: VXLAN_EVPN
            BGP_AS: "65001"
      register: result
    - debug:
        var: result
```

## Configuration notes

In order for Ansible to send to http port 8080 (rather than https port 443),
the following needs to be added either to your ansible.cfg, or to your
inventory group_vars:

```yaml
ansible_httpapi_use_ssl: no
ansible_httpapi_port: 8080
```

## Podman

This is being built to run in a container using Podman, but Docker should
also work (though I'm not using Docker so no guarantees).

You can also run it outside the container if you install the dependencies
(described in `Installation - No Container` below.)

## Installation - Container

To run ndfc_mock within a container.

```bash
git clone https://github.com/allenrobel/ndfc_mock.git
cd ndfc_mock
podman build -t ndfc_mock .
podman run --detach -p 8080:8080 ndfc_mock
```

After the container starts, point your browser at 
[http://localhost:8080/docs](http://localhost:8080/docs)
for the API documentation.  You can use e.g. Postman for
sending requests to the mock NDFC instance.

## Installation - No Container

To run run ndfc_mock outside of a container.

By default, fastapi starts the uvicorn server to listen on http port 8000.
Hence, ansible.cfg, or inventory group_vars would need to be modified
to use:

```yaml
ansible_httpapi_use_ssl: no
ansible_httpapi_port: 8000
```

```bash
git clone https://github.com/allenrobel/ndfc_mock.git
cd ndfc_mock
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd app
fastapi run main.py
# Comment out 'fastapi run main.py' above
# and uncomment 'fastapi dev main.py' below
# to run fastapi in debug mode.
#fastapi dev main.py
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

- Note: Running outside of a container will result in database.db being created in the ./app directory.
- Note: When starting with `fastapi dev main.py` the last two lines will not
  contain the ouput shown above, since debugging output will appear after these
  lines. In this case, scroll back up about 25 or so lines to view:

```bash
      INFO   Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

## Acknowledgements

This work would not be possible without the following.

1. [FastApi](https://fastapi.tiangolo.com)
2. [SQLModel](https://sqlmodel.tiangolo.com)
3. [Pydantic](https://docs.pydantic.dev/latest/)
4. [Podman](https://podman.io)

