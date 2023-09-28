# GO Hexagonal Architecture

**Update**: `2023-05-04` |
**Tag**: `GO` `Architecture` `RestAPI`

Hexagonal Architecture or Ports & Adapters is an architectural pattern that guilds
you in structuring a component/service/application and managing dependencies.

> **Warning**: \
> This is not a best practice!

**Layer of Architecture**:

```text
Presentation --> Business --> Database
```

**Table of Contents**:

- [Get Started]()
- []()

## Get Started

```text
bank
|--> repository
|    |--> customer_db.go
|    |--> customer_mock.go
|    |--> customer.go
|--> service
|    |--> customer.go
|--> go.mod
|--> main.go
```

### Create Customer Ports

```go
// repository/customer.go
package repository

type Customer struct {
    CustomerID  int     `db:"customer_id"`
    Name        string  `db:"name"`
    DateOfBirth string  `db:"date_of_birth"`  // or time.Time
    City        string  `db:"city"`
    ZipCode     string  `db:"zipcode"`
    Status      int     `db:"status"`
}

type CustomerRepository interface {
    GetAll() ([]Customer, error)
    GetById(int) (*Customer, error)
}
```

```go
// service/customer.go
package service

type CustomerResponse struct {
    CustomerID  int     `json:"customer_id"`  // If you want xml, `xml:"..."`
    Name        string  `json:"name"`
    Status      string  `json:"status"`
}

type CustomerService interface {
    GetCustomers() ([]CustomerResponse, error)
    GetCustomer(int) (*CustomerResponse, error)
}
```

### Create Database Adapters

```shell
go get github.com/jmoiron/sqlx
```

```go
// repository/customer_db.go
package repository

import "github.com/jmoiron/sqlx"

type customerRepositoryDB struct {
    db *sqlx.DB
}

func NewCustomerRepositoryDB(db *sqlx.DB) customerRepositoryDB {
    return customerRepositoryDB{db: db}
}

func (r customerRepositoryDB) GetAll() ([]Customer, error) {
    customers := []Customer{}
    query := "select ... from customers"
    err := r.db.Select(&customers, query)
    if err != nil {
        return nil, err
    }
    return customers, nil
}

func (r customerRepositoryDB) GetById(id int) (*Customer, error) {
    customer := Customer{}
    query := "select ... from customers where customer_id=?"
    err := r.db.Get(&customer, query, id)
    if err != nil {
        return nil, err
    }
    return &customer, nil
}
```

> **Note**: \
> If you want to implement create function, you can use:
> ```go
> query = "insert into ... values(?, ?, ?)"
> result, err := r.db.Exec(
>     query,
>     <obj>.Param01,
>     <obj>.Param02,
>     <obj>.Param03,
> )
> id, err := result.LastInsertId()
> if err != nil {
>     return nil, err
> }
> <obj>.ID = int(id)
> retunr &<obj>, nil
> ```

```shell
go get -u github.com/go-sql-driver/mysql
```

```go
// main.go
package main

import (
    _ "github.com/go-sql-driver/mysql"
    "github.com/jmoiron/sqlx"
)

func main() {
    db, err := sqlx.Open("mysql", "root:<password>@tcp(<host>:<port>)/<database>"
    if err != nil {
        panic(err)
    }

    customerRepository := repository.NewCustomerRepositoryDB(db)
    _ = customerRepository

    custoers, err := customerRepository.GetAll()
    if err != nil {
        panic(err)
    }
    fmt.Println(customers)

    customer, err := customerRepository.GetById(2000)
    if err != nil {
        panic(err)
    }
    fmt.Println(customer)  // &{200 Steve ...}
}
```

## Create Service Adapters

```go
// service/customer_service.go
package service

type customerService struct {
    custRepo repository.CustomerRepository  // ref interface only
}

func NewCustomerService(custRepo repository.CustomerRepository) customerService {
    return customerService{custRepo: custRepo}
}

func (s customerService) GerCustomers() ([]CustomerResponse, error) {
    customers, err := s.custRepo.GetAll()
    if err != nil {
        log.Println(err)
        return nil, err
    }
    custResponses := []CustomerResponse{}
    for _, customer := range customers {
        custResponse := CustomerResponse{
            CustomerID: customer.CustomerID,
            Name:       customer.Name,
            Status:     customer.Status,
        }
        custResponses = append(custResponses, custResponse)
    }
    return custResponses, nil
}

func (s customerService) GerCustomer(id int) (*CustomerResponse, error) {
    customer, err := s.custRepo.GetById(id)
    if err != nil {

        if err == sql.ErrNoRows {
            return nil, errors.New("customer not found")
        }

        log.Println(err)
        return nil, err
    }
    custResponse := CustomerResponse{
        CustomerID: customer.CustomerID,
        Name:       customer.Name,
        Status:     customer.Status,
    }
    return &custResponse, nil
}
```

```go
// main.go
package main

import (
    "back/repository"
    "back/service"

    _ "github.com/go-sql-driver/mysql"
    "github.com/jmoiron/sqlx"
)

func main() {
    db, err := sqlx.Open("mysql", "root:<password>@tcp(<host>:<port>)/<database>"
    if err != nil {
        panic(err)
    }

    customerRepository := repository.NewCustomerRepositoryDB(db)
    customerService := service.NewCustomerService(customerRepository)

    customers, err := customerService.GetCustomers()
    if err != nil {
        panic(err)
    }
    fmt.Println(customers)

    customer, err := customerService.GetCustomer(2000)
    if err != nil {
        panic(err)
    }
    fmt.Println(customer)  // &{200 Steve ...}
}
```

## Create Customer Handler

```text
bank
|--> handler
|    |--> customer.go
|--> repository
|    |--> customer_db.go
|    |--> customer.go
|--> service
|    |--> customer.go
|--> go.mod
|--> main.go
```

```shell
go get -u github.com/gorilla/mux
```

```go
package handler

import (
    "bank/service"
    "net/http"
)

type customerHandler struct {
    custSrv service.CustomerService
}

func NewCustomerHandler(custSrv service.CustomerService) customerHandler {
    return customerHandler{custSrv: custSrv}
}

func (h customerHandler) GetCustomers(w http.ResponseWriter, r *http.Request) {
    customers, err := h.custSrv.GetCustomers()
    if err != nil {
        w.WritHeader(http.StatusInternalServerError)
        fmt.Fprintln(w, err)
        return
    }

    w.Header().Set("content-type", "application/json")
    json.NewEncoder(w).Encode(customers)
}

func (h customerHandler) GetCustomer(w http.ResponseWriter, r *http.Request) {
    customerID, _ := strconv.Atoi(mux.Vars(r)["customerID"])
    customer, err := h.custSrv.GetCustomer(customerID)
    if err != nil {
        w.WritHeader(http.StatusInternalServerError)
        fmt.Fprintln(w, err)
        return
    }
    w.Header().Set("content-type", "application/json")
    json.NewEncoder(w).Encode(customer)
}
```

```go
// main.go
package main

import (
    "back/repository"
    "back/service"
    "back/handler"
    "net/http"

    _ "github.com/go-sql-driver/mysql"
    "github.com/jmoiron/sqlx"
)

func main() {
    db, err := sqlx.Open("mysql", "root:<password>@tcp(<host>:<port>)/<database>"
    if err != nil {
        panic(err)
    }

    customerRepository := repository.NewCustomerRepositoryDB(db)
    customerService := service.NewCustomerService(customerRepository)
    customerHandler := handler.NewCustomerHandler(customerService)

    router := mux.NewRouter()

    router.HandleFunc("/customers", customerHandler.GetCustomers).Methods(http.MethodGet)
    router.HandleFunc("/customers/{customerID:[0-9]+}", customerHandler.GetCustomer).Methods(http.MethodGet)

    http.ListenAndServe(":8000", router)
}
```

## Create Mock Repository


```text
bank
|--> repository
|    |--> ...
|    |--> customer_mock.go
|    |--> ...
|--> ...
```

```go
// repository/customer_mock.go
package repository

type customerRepositoryMock struct {
    customers []Customer
}

func NewCustomerRepositoryMock() CustomerRepositoryMock {
    customers := []Customer{
        {CustomerID: 1001, Name: "Sara", ...},
        {CustomerID: 1002, Name: "Tom", ...},
    }
    return CustomerRepositoryMock{customers: customers}
}

func (r customerRepositoryMock) GetAll() ([]Customer, error) {
    return r.cusomers, nil
}

func (r customerRepositoryMock) GetById(id int) (*Customer, error) {
    for _, customer := range r.cusomers {
        if customer.CustomerID == id {
            return &customer, nil
        }
    }
    return nil, errors.New("customer not found")
}
```

```go
...
customerRepository := repository.NewCustomerRepositoryDB(db)
---> Change to ...
customerRepository := repository.NewCustomerRepositoryMock()
...
```

## Configuration

```shell
go get github.com/spf13/viper
```

```text
bank
|--> repository
|    |--> ...
|--> ...
|--> config.yaml
|--> main.go
```

```go
// main.go

func main() {
    initConfig()

    dsn := fmt.Sprintf("%v:%v@tcp(%v:%v)/%v?parseTime=true",
        viper.GetString("db.username"),
        viper.GetString("db.password"),
        viper.GetString("db.host"),
        viper.GetInt("db.port"),
        viper.GetString("db.database"),
    )
    db, err := sqlx.Open(viper.GetString("db.driver"), dns)
    if err != nil {
        panic(err)
    }

    ...

    http.ListenAddServe(fmt.Sprintf(":%v", viper.GetInt("app.port")), router)
}


func initConfig() {
    viper.SetConfigName("config")
    viper.SetConfigType("yaml")
    viper.AddConfigPath(".")

    // Read Environment variable after and override value
    viper.AutonaticEnv()
    viper.SetEnvKeyReplacer(string.NewReplacer(".", "_"))

    err := viper.ReadInConfig()
    if err != nil {
        panic(err)
    }
}
```

```yaml
app:
    port: 8000

db:
    driver: "mysql"
    host: "13.00.000.00"
    port: 3306
    username: root
    password: P@ssw0rd
    database: banking
```

### Change Database Setup

```go
// main.go

def main() {
    ...
    db := initDatabase()
    ...
}

def initDatabase() *sqlxDB {
    dsn := fmt.Sprintf("%v:%v@tcp(%v:%v)/%v?parseTime=true",
        viper.GetString("db.username"),
        viper.GetString("db.password"),
        viper.GetString("db.host"),
        viper.GetInt("db.port"),
        viper.GetString("db.database"),
    )
    db, err := sqlx.Open(viper.GetString("db.driver"), dns)
    if err != nil {
        panic(err)
    }

    // Database configuration
    db.SetConnMaxLifetime(3 * time.Minute)
    db.SetMaxOpenConns(10)
    db.SetMaxIdleConns(10)

    return db
}
```

## TimeZone

```go
// main.go

func main() {
    initTimeZone()
}

func initTimeZone() {
    ict, err := time.LoadLocation("Asia/Bangkok")
    if err != nil {
        panic(err)
    }

    time.Local = ict
}
```

## Logging

```shell
go get -u go.uber.org/zap
```

```text
bank
|--> logs
|    |--> logs.go
|--> repository
|    |--> ...
|--> ...
|--> main.go
```

```go
// logs/logs.go
package logs

import "go.uber.org/zap"

var log *zap.Logger

func init() {
    var err error

    log, _ = zap.NewProduction()  // production use json, but development use console

    // Or, ddit Production configuration
    config := zap.NewProductionConfig()
    config.EncoderConfig.TimeKey = "timestamp"
    config.EncoderConfig.EncodeTime = zapcore.ISO8601TimeEncoder

    // If you want to close strack trace,
    config.EncoderConfig.StacktraceKey = ""

    log, err = config.Build(zap.AddCallerSkip(1))  // Skip caller 1 step
    if err != nil {
        panic(err)
    }
}

func Info(message string, fields ...zap.Field) {
    log.Info(message, fields...)
}

func Debug(message string, fields ...zap.Field) {
    log.Debug(message, fields...)
}

func Error(message interface{}, fields ...zap.Field) {
    switch y := message.(type) {
        case error:
            log.Error(v.Error(), fields...)
        case string:
            log.Error(v, fields...)
    }
}
```

> **Note**: \
> In GO, it has init function that will run before main function. You can use it by
> `func init() { ... }`

```go
// main.go

func main() {
    ...
    logs.Log.Info("Banking service started Info Level log")
    ...
}
```

### Change Log in Service

```go
...
log.Println(err)
---> Change to ...
logs.Error(err.Error())  // Or, logs.Error(err)
...
```

## Error

```text
bank
|--> errs
|    |--> errs.go
|--> ...
|--> repository
|    |--> ...
|--> ...
|--> main.go
```

```go
// errs/errs.go
package errs

type AppError struct {
    Code    int
    Message string
}

func (e AppError) Error() string {
    return e.Message
}

func NewNotFoundError(message string) error {
    return AppError{
        Code:    http.StatusNotFound,
        Message: message,
    }
}

func NewUnexpectedError(message string) error {
    return AppError{
        Code:    http.StatusInternalServerError,
        Message: "unexpected error",
    }
}
```

```go
// service/customer_service.go

func (s customerService) GetCustomer(id int) ... {
    ...
    if err != nil {
        if err == sql.ErrNoRows {
            return nil, errs.NewNotFoundError("customer not found")
        }
        logs.Error(err)
        return nil, errs.NewUnexpectedError()
    }
    ...
}
```

```go
// handler/customer.go

func (h customerHandler) GetCustomer(w http.ResponseWriter, ...) {
    ...
    if err != nil {

        appErr, ok := err.(errs.AppError)
        if ok {
            w.WriteHeader(appErr.Code)
            fmt.Fprintln(w, appErr.Message)
            return
        }

        w.WritHeader(http.StatusInternalServerError)
        fmt.Fprintln(w, err)
        return
    }
    ...
}
```

### Change Code to helper

```text
bank
|--> errs
|    |--> errs.go
|--> handler
|    |--> customer.go
|    |--> handler.go
|--> ...
|--> main.go
```

```go
// handler/handler.go
package handler

import "net/http"

func handleError(w http.ResponseWriter, err error) {
    switch e := err.(type) {
        case errs.AppError:
            w.WriteHeader(e.Code)
            fmt.Fprintln(w, e)
        case error:
            w.WriteHeader(http.StatusInternalServerError)
            fmt.Fprintln(w, e)
    }
}
```

```go
...
appErr, ok := err.(errs.AppError)
if ok {
    w.WriteHeader(appErr.Code)
    fmt.Fprintln(w, appErr.Message)
    return
}
w.WritHeader(http.StatusInternalServerError)
fmt.Fprintln(w, err)

---> Change to ...

handleError(w, err)
...
```

## Add More

### Account

```go
// reposirory/account.go

type Account struct {
    AccountID       int     `json:"account_id"`
    CustomerID      int     `json:"customer_id"`
    OpeningDate     string  `json:"opening_date"`
    AccountType     string  `json:"account_type"`
    Amount          float64 `json:"amount"`
    Status          int     `json:"status"`
}

type AccountRepository interface {
    Create(Account) (*Account, error)
    GetAll(int) ([]Account, error)
}
```

```go
// service/account.go
package serice

type NewAccountRequest struct {
    AccountType     string  `json:"account_type"`
    Amount          float64 `json:"amount"`
}

type NewAccountResponse struct {
    AccountID       int     `json:"account_id"`
    OpeningDate     string  `json:"opening_date"`
    AccountType     string  `json:"account_type"`
    Amount          float64 `json:"amount"`
    Status          int     `json:"status"`
}

type AccountService interface {
    NewAccount(int, NewAccountRequest) (*NewAccountResponse, error)
    GetAccounts(int) ([]NewAccountResponse, error)
}
```

```go
// service/account_service.go

...
func (s accountService) NewAccount(customerID int, request NewAccountRequest) (*AccountResponse, error) {
    // Validation
    if request.Amount < 5000 {
        return nil, errs.NewValidationError("amount at least 5,000")
    }
    if string.ToLower(requset.AccountType) != "saving" && string.ToLower(requset.AccountType) != "checking" {
        return nil, errs.NewValidationError("account type should be saving or checking only")
    }
    account := repository.Account{
        CustomerID:     customerID,
        OpeningDate:    time.New().Format("2006-1-2 15:00:00"),
        AccountType:    requset.AccountType,
        Amount:         requset.Amount,
        Status:         1,
    }

    newAcc, err := s.accRepo.Create(account)
    if err != nil {
        logs.Error(err)
        return nil, errs.NewUnexpectedError()
    }
    response := AccountResponse{
        AccountID:  newAcc.AccountID,
        ...
    }
    return response, nil
}
...
```

```go
// handler/account.go

...

func (h accountHandler) NewAccount(w http.ResponseWriter, r *http.Request) {
    customerID, _ := strconv.Atoi(mux.Vars(r)["customerID"])
    if r.Header.Get("content-type") != "application/json" {
        handlerError(w, errs.NewValidationError("request body incorrect format"))
        return
    }

    request := service.NewAccoutRequest{}
    err := json.NewDecoder(r.Body).Decode(&request)
    if err != nil {
        handlerError(w, errs.NewValidationError("request body incorrect format"))
        return
    }

    response, err := h.accSrv.NewAccount(customerID, request)
    if err != nil {
        handlerError(w, err)
        return
    }

    w.WriteHeader(http.StatusCreated)
    w.Header().Set("content-type", "application/json")
    json.NewEncoder(w).Encode(response)
}

...
```

## References

- https://www.youtube.com/watch?v=k3JZI-sQs2k
