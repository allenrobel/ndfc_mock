FROM python:3.12

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --upgrade pip

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

# Disable requirement for HEALTHCHECK since this is not a critical app.
# checkov:skip=CKV_DOCKER_2: required

# Disable requirement for non-root user, since we are running under rootless 
# podman.  See:
#
# https://github.com/containers/podman/blob/main/docs/tutorials/rootless_tutorial.md
# 
# And:
# https://github.com/containers/podman/blob/main/rootless.md
#
# checkov:skip=CKV_DOCKER_3: required

CMD ["fastapi", "run", "app/main.py", "--port", "8080"]
