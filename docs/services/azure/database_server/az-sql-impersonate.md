# Azure SQL Server use Impersonate

For use `EXECUTE AS [<user@mail.com>]`

```sql
GRANT IMPERSONATE ON USER::[<user@mail.com>] TO [<target@mail.com>];
```

```sql
REVOKE IMPERSONATE ON USER::[<user@mail.com>] TO [<target@mail.com>];
```
