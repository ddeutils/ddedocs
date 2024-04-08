# RBAC

!!! quote

    Users are mapped to roles, roles are mapped to set of permissions that allow
    access to resource(s).

When K8s receives a new request K8s API server performs the following steps:

- Authenticate the user, if validation fails return `401 unauthorised`
- Authorise the request, if it fails return `403 Forbidden`

## References

- [K8s for Data Engineers — RBAC](https://blog.devgenius.io/k8s-for-data-engineers-rbac-a6a231207569)
