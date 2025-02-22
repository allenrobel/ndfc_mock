# Summary

This is a work in progress with limited functionality.

When finished, this will allow for minor development and testing of
[ansible-dcnm](https://github.com/CiscoDevNet/ansible-dcnm)
modules (and other REST API-based applications) without requiring a
real ND/NDFC instance.

Basically, it will accept GET/POST/PUT/DELETE requests to
endpoints supported by NDFC and will return mock responses.

## Current status

Running basic merged,query,deleted-state dcnm_fabric playbook tasks against
the mock instance is working (to create, modify, query, and delete fabrics)
per the example playbook below.

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
    tasks:
    - name: Query VXLAN Fabric
      cisco.dcnm.dcnm_fabric:
        state: query
        config:
        -   FABRIC_NAME: f1
      register: result
    - debug:
        var: result
    - name: Delete VXLAN Fabric
      cisco.dcnm.dcnm_fabric:
        state: deleted
        config:
        -   FABRIC_NAME: f1
      register: result
    - debug:
        var: result
```

For the deleted-state `dcnm_fabric` playbook task to return success, the fabric
cannot contain any switches.  The `dcnm_fabric` Ansible module uses the
following GET request to determine the number of switches in the fabric.

`/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/switches/<fabric_name>/overview`

For now, a stub handler is implemented which returns zero switches to
allow the deleted-state playbook task to work.  This will be replaced
soon with appropriate inventory handlers and database tables to support
fabric switch addition/deletion.

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

## Uninstall - Container

To delete the container and image afterwards, do the following.

```bash
podman ps
```

From the above output, use the randomly-assigned name in the NAMES column
for the next couple commands to stop and remove the container.

```bash
podman stop randomly_assigned_container_name
podman rm randomly_assigned_container_name
```

Then delete the image.

```bash
podman rmi ndfc_mock
```

### Example

```bash
(py312) AROBEL-M-G793% podman ps
CONTAINER ID  IMAGE                       COMMAND               CREATED         STATUS         PORTS                   NAMES
6ef724456379  localhost/ndfc_mock:latest  fastapi run app/m...  19 minutes ago  Up 19 minutes  0.0.0.0:8080->8080/tcp  inspiring_villani
(py312) AROBEL-M-G793% podman stop inspiring_villani
inspiring_villani
(py312) AROBEL-M-G793% podman rm inspiring_villani
inspiring_villani
(py312) AROBEL-M-G793% podman rmi ndfc_mock
Untagged: localhost/ndfc_mock:latest
Deleted: c4d64f101f97baa2a9ebe5984ffae3eab15f8477ee72817cea5ff499c1caa554
Deleted: bbad8f9629050572ebdf128bb851d433ddc50d8585444fe380bba7c9170c72a5
(py312) AROBEL-M-G793%
```

### Usage

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

To run outside of a container, you must start fastapi in the directory immediately
above `app`.  This is because the endpoint handler that retrieves templates needs
to use the container path to the template files (`./app/templates/*`).  To match
this when running out-of-container, fastapi needs to be run one directory
level above `app` (per the example below).

```bash
git clone https://github.com/allenrobel/ndfc_mock.git
cd ndfc_mock
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
fastapi run app/main.py
# Comment out 'fastapi run main.py' above
# and uncomment 'fastapi dev main.py' below
# to run fastapi in debug mode.
#fastapi dev app/main.py
```

You'll see the uvicorn server startup.  The last two lines will look like:

```bash
      INFO   Application startup complete.
      INFO   Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

Point your browser at [http://localhost:8000/docs](http://localhost:8000/docs)
for the API documentation.  You can use e.g. Postman for sending requests to
the uvicorn site.

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
