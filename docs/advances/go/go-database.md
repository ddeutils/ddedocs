# GO Connect to Database

**Table of Contents**:

- [Start to Connect Database]
- [Create Return Function]
- [Create CRUD]
- [Transaction]

## Start to Connect Database

```shell
go get -u github.com/denisenkom/go-mssqldb
```

```go
package main

import {
    "database/sql"

    // import driver that use in /sql package
    _ "github.com/denisenkom/go-mssqldb"
}

func main() {
    db, err := sql.Open("sqlserver", "sqlserver://<user>:<password>@<host>:1443/<database>")
    if err != nil {
        panic(err)
    }

    err = db.Ping()
    if err != nil {
        panic(err)
    }

    query := "select id, name from cover"
    row, err := db.Query(query)
    if err != nil {
        panic(err)
    }
    defer rows.Close()

    for rows.Next() {
        id := 0
        name := ""
        err = rows.Scan(&id, &name)
        if err := nil {
            panic(err)
        }
        println(id, name)
    }
}
```

## Create Struct for receive data

```go
type Cover struct {
    Id int
    Name string
}
```

```go
covers := []Cover{}

for rows.Next() {
    cover := Cover{}
    err = rows.Scan(&cover.Id, &cover.Name)
    if err != nil {
        panic(err)
    }
    covers = append(covers, cover)
}

fmt.Printf("%#v", covers)
```

```text
[]main.Cover{main.Cover{Id:1, Name:"cover-lion"}, main.Cover{Id:1, Name:"cover-zebra"}}%
```

## Create Return Function

```go
var db *sql.DB

func main() {
    var err error
    db, err = sql.Open("sqlserver", "sqlserver://<user>:<password>@<host>:1443/<database>")
    if err != nil {
        panic(err)
    }

    covers, err := GetCovers()
    if err != nil {
        fmt.Println(err)
        return
    }

    for _, cover := range covers {
        fmt.Println(cover)
    }
}

func GetCovers() ([]Cover, error) {
    err = db.Ping()
    if err != nil {
        return nil, err
    }

    query := "select id, name from cover"
    row, err := db.Query(query)
    if err != nil {
        return nil, err
    }
    defer rows.Close()

    covers := []Cover{}
    for rows.Next() {
        cover := Cover{}
        err = rows.Scan(&cover.Id, &cover.Name)
        if err != nil {
            return nil, err
        }
        covers = append(covers, cover)
    }
    return covers, nil
}
```

> **Note**: \
> You should not create error handler process in your err.

## Create CRUD

### Read

```go
func GetCover(id int) (*Cover, error) {
    err := db.Ping()
    if err != nil {
        return nil, err
    }

    // Use @id for SQL Server
    query := "select id, name from cover where id=@id"
    row := db.QueryRow(query, sql.Named("id", id))

    cover := Cover{}
    err = row.Scan(&cover.Id, &cover.Name)
    if err != nil {
        return nil, err
    }
    return &cover, nil
}
```

```go
cover, err := GetCover(1)
if err != nil {
    panic(err)
}
println(cover)
```

```text
&{1 cover-lion}
```

> **Note**: \
> If you use MySQL, the above query row syntax will change to
> ```go
> query := "select id, name from cover where id=?"
> row := db.QueryRow(query, id)
> ```

### Create

```go
func AddCover(cover Cover) error {
    query := "insert into cover (id, name) values (?, ?)"
    result, err := db.Exec(query, cover.Id, cover.Name)
    if err != nil {
        return err
    }
    affected, err := result.RowAffected()
    if err != nil {
        return err
    }
    if affected <= 0 {
        return errors.New("cannot insert to cover table")
    }
    return nil
}
```

```go
cover := Cover{9, "cover-Tom"}
err = AddCover(cover)
if err != nil {
    panic(err)
}
```

### Update

```go
func UpdateCover(cover Cover) error {
    query := "update cover set name=? where id=?"
    result, err := db.Exec(query, cover.Name, cover.Id)
    if err != nil {
        return err
    }
    affected, err := result.RowAffected()
    if err != nil {
        return err
    }
    if affected <= 0 {
        return errors.New("cannot update to cover table")
    }
    return nil
}
```

```go
cover := Cover{9, "cover-Sara"}
err = UpdateCover(cover)
if err != nil {
    panic(err)
}
```

### Delete

```go
func DeleteCover(id int) error {
    query := "delete from cover where id=?"
    result, err := db.Exec(query, id)
    if err != nil {
        return err
    }
    affected, err := result.RowAffected()
    if err != nil {
        return err
    }
    if affected <= 0 {
        return errors.New("cannot delete to cover table")
    }
    return nil
}
```

```go
err = DeleteCover(9)
if err != nil {
    panic(err)
}
```

## SQLX

```shell
go get github.com/jmoiron/sqlx
```

```go
package main

import {
    _ "github.com/go-sql-driver/mysql"
    "github.com/jmoiron/sqlx"
}

var db *sqlx.DB

func main() {
    var err error
    db, err = sqlx.Open("mysql", "root:<password>@tcp(<host>)/<database>")
    if err != {
        panic(err)
    }
}

func GetCoversX() ([]Cover, error) {
    query := "select id, name from cover"
    covers := []Cover{}
    err = db.Select(&covers, query)
    if err != nil {
        return nil, err
    }
    return covers, nil
}
```

### Change Read

```go
func GetCoverX(id int) (*Cover, error) {
    query := "select id, name from cover where id=?"
    cover := Cover{}
    err = db.Get(&cover, query, id)
    if err != nil {
        return nil, err
    }
    return &cover, nil
}
```

## Transaction

```go
tx, err := db.Begin()
if err != nil {
    return err
}

query := "..."
result, err := tx.Exec(query, ...)

...

affected, err := result.RowsAffected()
if err != nil {
    tx.Rollback()
    return err
}

...

err = tx.Commit()
if err != nil {
    return err
}
return nil

```
