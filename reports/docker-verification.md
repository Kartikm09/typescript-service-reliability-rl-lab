# Docker verification

Verified locally on 2026-07-23 with Docker Engine 29.5.2 on an ARM64 Linux virtual
machine. The image was rebuilt from the final lockfile and source tree.

```console
$ docker compose up -d --build --wait
Container typescript-service Healthy
$ curl --fail --silent http://127.0.0.1:8084/health
{"status":"ok"}
$ docker compose ps
typescript-service   Up (healthy)   0.0.0.0:8084->8084/tcp
$ docker compose down
```

This verifies the documented local container workflow and health endpoint. It is not
a production deployment or a multi-architecture compatibility claim.
