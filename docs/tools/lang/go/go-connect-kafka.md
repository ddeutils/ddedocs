# GO Advance with Kafka

**Table of Contents**:

- [Setup Kafka](#setup-kafka)
- [Create Simple Consumer with GO]()
- [Create Simple Producer with GO]()

## Setup Kafka

```yaml
version: "3.9"
services:
  zookeeper:
    image: zookeeper
    container_name: zookeeper
    volumes:
      - ./zookeeper:/data

  kafka:
    image: bitnami/kafka
    container_name: kafka
    ports:
      - "9092:9092"
    volumes:
      - ./kafka:/bitnami/kafka/data
    environment:
      - ALLOW_PLAINTEXT_LISTENER=yes
      - KAFKA_CFG_LISTENERS=PLAINTEXT://:9092
      - KAFKA_CFG_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092
      - KAFKA_CFG_ZOOKEEPER_CONNECT=zookeeper:2181
    depends_on:
      - zookeeper
```

```shell
$ docker compose up -d
```

### Test Send some data to Kafka Server

- List topics on your Kafka server

```shell
$ kafka-topics --bootstrap-server=localhost:9092 --list
```

- Create `demo` topic on your Kafka server

```shell
$ kafka-topics --bootstrap-server=localhost:9092 --topic=demo --create
```

- Open consumer to `demo` topic

```shell
$ kafka-console-consumer --bootstrap-server=localhost:9092 --topic=demo
```

- Send some data by producer to `demo` topic

```shell
$ kafka-console-producer --bootstrap-server=localhost:9092 --topic=demo
>hello world
```

```shell
$ kafka-console-consumer ...
hello world
```

- Open consumer to `demo` topic with separate by groups

```shell
$ kafka-console-consumer --bootstrap-server=localhost:9092 \
  --topic=demo \
  --group=data
```

```shell
$ kafka-console-consumer --bootstrap-server=localhost:9092 \
  --topic=demo \
  --group=log
```

- Open consumer to `test`, and `demo` topics

```shell
$ kafka-console-consumer --bootstrap-server=localhost:9092 \
  --include="demo|test" \
  --group=log
```

- Send some data by producer to different topics

```shell
$ kafka-console-producer --bootstrap-server=localhost:9092 --topic=demo
>hello demo

$ kafka-console-producer --bootstrap-server=localhost:9092 --topic=demo
>hello test
```

```shell
$ kafka-console-consumer ... --include="demo|test" ...
hello demo
hello test
```

## Create Simple Consumer with GO

```shell
go mod init consumer
go get github.com/Shopify/sarama
```

See the partition of `demo` topic

```shell
$ kafka-topics --bootstrap-server=localhost:9092 --topic=demo --describe
```

```go
package main

func main() {
    servers := []string{"localhost:9092"}

    consumer, err := sarama.NewConsumer(servers, nil)
    if err != nil {
        panic(err)
    }
    defer consumer.Close()

    partitionConsumer, err := consumer.ConsumePartition("demo", 0, sarama.OffsetNewest)
    if err != nil {
        panic(err)
    }
    defer partitionConsumer.Close()

    for {
        select {
            case err := <- partitionConsumer.Errors():
                fmt.Println(err)
            case msg := <- partitionConsumer.Messages():
                fmt.Println(string(msg.Value))
        }
    }

}
```

```shell
$ go run .
```

### Test receive data from GO Consumer

```shell
$ kafka-console-producer --bootstrap-server=localhost:9092 --topic=demo
>hello Go Consumer
```

Response from Go Consumer will see:

```shell
$ go run .
hello Go Consumer
```

## Create Simple Producer with GO

```shell
go mod init producer
go get github.com/Shopify/sarama
```

```go
package main

func main() {
    servers := []string{"localhost:9092"}

    producer, err := sarama.NewSyncProducer(servers, nil)
    if err != nil {
        panic(err)
    }
    defer producer.Close()

    msg := sarama.ProducerMessage{
        Topic: "demo",
        Value: sarama.StringEncoder("Hello from Go Producer"),
    }

    p, o, err := produser.SendMessage(&msg)
    if err != nil {
        panic(err)
    }
    fmt.Println("partition=%v, offset=%v", p, o)
}
```

### Test send data from GO Producer

```shell
# producer
go run .
partition=0, offset=4%
```

```shell
# consumer
go run .
Hello from Go Producer
```

## Create Events with GO

```shell
go init events
```

```go
package events

import "reflect"

var Topics = []string{
    reflect.TypeOf(OpenAccountEvent{}).Name(),
    reflect.TypeOf(DepositFundEvent{}).Name(),
    reflect.TypeOf(WithdrawFundEvent{}).Name(),
    reflect.TypeOf(CloseAccountEvent{}).Name(),
}

type Event interface {

}

type OpenAccountEvent struct {
    ID              string
    AccountHolder   string
    AccountType     int
    OpeningBalance  float64
}

type DepositFundEvent struct {
    ID              string
    Amount          float64
}

type WithdrawFundEvent struct {
    ID              string
    Amount          float64
}

type CloseAccountEvent struct {
    ID              string
}
```

## Create Advance Consumer with GO

```yaml
## config.yaml
kafka:
  servers:
    - localhost:9092
  group: accountConsumer

db:
  driver: mysql
  host: localhost
  port: 3306
  username: root
  password: P@ssw0rd
  database: demo
```

- Import `events` module from local

```go
// go.mod
...
replace events => ../events
...
```

```shell
go get events
```

```go
// repositories/account.go
package repositories

...

type BankAccount struct {
    ID              string
    AccountHolder   string
    AccountType     int
    Balance         float64
}

type AccountRepository interface {
    Save(bankAccount BankAccount) error
    Delete(id string) error
    FindAll() (bankAccounts []BankAccount, err error)
    FindByID(id string) (bankAccount BankAccount, err error)
}

type accountRepository struct {
    db *gorm.DB
}

func NewAccountRepository(db *gorm.DB) AccountRepository {
    db.Table("demo_banks").AutoMigrate(&BankAccount{})
    return accountRepository{db}
}

func (obj accountRepository) Save(bankAccount BankAccount) error {
    return obj.db.Table("demo_banks").Save(bankAccount).Error
}

func (obj accountRepository) Save(id string) error {
    return obj.db.Table("demo_banks").Where("id=?", id).Delete(&BankAccount{}).Error
}

func (obj accountRepository) FindAll() (bankAccounts []BankAccount, err error) {
    err = obj.db.Table("demo_banks").Find(&bankAccounts).Error
    return bankAccounts, err
}

func (obj accountRepository) FindByID(id string) (bankAccount BankAccount, err error) {
    err = obj.db.Table("demo_banks").Where("id=?", id).First(&bankAccount).Error
    return bankAccount, err
}
```

```go
// services/account.go
package services

type EventHandler interface {
    Handle(topic string, eventBytes []byte)
}

type accountEventHandler struct {
    accountRepo repositories.AccountRepository
}

func NewAccountEventHandler(accountRepo repositories.AccountRepository) EventHandler {
    return accountEventHandler{accountRepo}
}

func (obj accountEventHandler) Handle(topic string, eventBytes []byte) {
    switch topic {
        case reflect.TypeOf(OpenAccountEvent{}).Name():
            event := events.OpenAccountEvent{}
            err := json.Unmarshal(eventBytes, event)
            if err != nil {
                log.Println(err)
                return
            }
            bankAccount := repositories.BankAccount {
                ID:             event.ID,
                AccountHolder:  event.AccountHolder,
                AccountType:    event.AccountType,
                Balance:        event.OpenBalance,
            }
            err = obj.accountRepo.Save(bankAccount)
            if err != nil {
                log.Println(err)
                return
            }
            log.Println(event)
        case reflect.TypeOf(DepositFundEvent{}).Name():
            event := events.DepositFundEvent{}
            err := json.Unmarshal(eventBytes, event)
            if err != nil {
                log.Println(err)
                return
            }
            bankAccount, err := obj.accountRepo.FindByID(event.ID)
            if err != nil {
                log.Println(err)
                return
            }
            bankAccount.Balance += event.Amount
            err = obj.accountRepo.Save(bankAccount)
            if err != nil {
                log.Println(err)
                return
            }
            log.Println(event)
        case reflect.TypeOf(WithdrawFundEvent{}).Name():
            event := events.WithdrawFundEvent{}
            err := json.Unmarshal(eventBytes, event)
            if err != nil {
                log.Println(err)
                return
            }
            bankAccount, err := obj.accountRepo.FindByID(event.ID)
            if err != nil {
                log.Println(err)
                return
            }
            bankAccount.Balance -= event.Amount
            err = obj.accountRepo.Save(bankAccount)
            if err != nil {
                log.Println(err)
                return
            }
            log.Println(event)
        case reflect.TypeOf(CloseAccountEvent{}).Name():
            event := events.CloseAccountEvent{}
            err := json.Unmarshal(eventBytes, event)
            if err != nil {
                log.Println(err)
                return
            }
            err = obj.accountRepo.Delete(event.ID)
            if err != nil {
                log.Println(err)
                return
            }
            log.Println(event)
        default:
            log.Println("no event handler")
    }
}
```

```go
// services/consumer.go
package services

type consumerHandler struct {
    eventHandler EventHandler
}

func NewConsumerHandler(eventHandler EventHandler) sarama.ConsumerGroupHandler {
    return consumerHandler{eventHandler}
}

func (obj consumerHandler) Setup(sarama.ConsumerGroupSession) error {
    return nil
}

func (obj consumerHandler) Cleanup(sarama.ConsumerGroupSession) error {
    return nil
}

func (obj consumerHandler) ConsumeClaim(session sarama.ConsumerGroupSession, claim sarama.ConsumerGroupClaim) error {
    for msg := range claim.Messages() {
        obj.eventHandler.Handle(msg.Topic, msg.Value)
        session.MarkMessage(msg, "")
    }

    return nil
}
```

```go
// main.go
package main

func init() {
    viper.SetConfigName("config")
    viper.SetConfigType("yaml")
    viper.AddConfigPath(".")
    viper.AutomaticEnv()
    viper.SetEnvKeyReplacer(strings.NewReplacer(".", "_"))
    if err := viper.ReadConfig(); err != nil {
        panic(err)
    }
}

func initDatabase() *gorm.DB {
    dsn := fmt.Sprintf(%v:%v@tcp(%v:%v)/%v,
        viper.GetString("db.username"),
        viper.GetString("db.password"),
        viper.GetString("db.host"),
        viper.GetInt("db.port"),
        viper.GetString("db.database"),
    )

    dial := mysql.Open(dsn)
    db, err := gorm.Open(dial, &gorm.Config{
        Logger: logger.Default.LogMode(logger.Silent),
    })
    if err != nil {
        panic(err)
    }

    return db
}

func main() {
    consumer, err := sarama.NewConsumerGruop(viper.GetStringSlice("kafka.servers"), viper.GetString("kafka.group"), nil)
    if err != nil {
        panic(err)
    }
    defer consumer.Close()

    db := initDatabase()
    accountRepo := repositories.NewAccountRepository(db)
    accountEventHandler := services.NewAccountEventHandler(accountRepo)
    accountConsumerHandler := services.NewConsumerHandler(accountEventHandler)

    fmt.Println("Account consumer started ...")
    for {
        consumer.Consume(context.Backgroud(), event.Topics, accountConsumerHandler)
    }
}
```

```shell
$ go run .
Account consumer started ...
```

- List groups

```shell
$ kafka-consumer-groups --bootstrap-server=localhost:9092 --list
accountConsumer
...
```

- Test receive data from manual producer

```shell
$ kafka-console-producer --bootstrap-server=localhost:9092 --topic=OpenAccountEvent
>{"ID": "1","AccountHolder":"Admin","AccountType":1,"OpeningBalance":1000}
```

```shell
$ go run .
Account consumer started ...
20**/**/01 00:00:00 &{1 Admin 1 1000}
```

```shell
$ kafka-console-consumer --bootstrap-server=localhost:9092 \
  --include="OpenAccountEvent|DepositFundEvent|WithdrawFundEvent|CloseAccountEvent" \
  --group=log
{"ID": "1","AccountHolder":"Admin","AccountType":1,"OpeningBalance":1000}
```

## Create Advance Consumer with GO

```yaml
## config.yaml
kafka:
  servers:
    - localhost:9092
```

- Import `events` module from local

```go
// go.mod
...
replace events => ../events
...
```

```go
// commands/command.go
package commands

type OpenAccountCommand struct {
    AccountHolder   string
    AccountType     int
    OpeningBalance  float64
}

type DepositFundCommand struct {
    ID              string
    Amount          float64
}

type WithdrawFundCommand struct {
    ID              string
    Amount          float64
}

type CloseAccountCommand struct {
    ID              string
}
```

```go
//services/producer.go
package services

type EventProducer interface {
    Produce(event events.Event) error
}

type eventProducer struct {
    producer sarama.SyncProducer
}

func NewEventProducer(producer sarama.SyncProducer) EventProducer {
    return eventProducer{producer}
}

func (obj eventProducer) Produce(event events.Event) error {
    topic := reflect.TypeOf(event).Name()

    value, err := json.Marshal(event)
    if err != nil {
        return err
    }

    msg := sarama.ProducerMessage{
        Topic: topic,
        Value: sarama.ByteEncoder(value),
    }

    _, _, err = obj.producer.SendMessage(&msg)
    if err != nil {
        return err
    }
    return nil
}
```

```shell
$ go get github.com/google/uuid
```

```go
// services/account.go
package services

type AccountService interface {
    OpenAccount(command commands.OpenAccountCommand) (id string, err error)
    DepositFund(command commands.DepositFundCommand) error
    WithdrawFund(command commands.WithdrawFundCommand) error
    CloseAccount(command commands.CloseAccountCommand) error
}

type accountService struct {
    eventProducer EventProducer
}

func NewAccountService(eventProducer EventProducer) AccountService {
    return accountService{eventProducer}
}

func (obj accountService) OpenAccount(command commands.OpenAccountCommand) (id string, err error) {

    if command.AccountHolder == "" || command.AccountType == 0 || command.OpeningBalance == 0 {
        return "", errors.New("bad request")
    }

    event := events.OpenAccountEvent {
        ID:             uuid.NewString(),
        AccountHolder:  command.AccountHolder,
        AccountType:    command.AccountType,
        OpeningBalance: command.OpeningBalance,
    }
    log.Println("%#v", event)
    return event.ID, obj.eventProducer.Produce(event)
}

func (obj accountService) DepositFund(command commands.DepositFundCommand) error {
    if command.ID == "" || command.Amount == 0 {
        return errors.New("bad request")
    }

    event := events.DepositFundEvent{
        ID:     command.ID,
        Amount  command.Amount,
    }
    log.Println("%#v", event)
    return obj.eventProducer.Produce(event)
}

func (obj accountService) WithdrawFund(command commands.WithdrawFundCommand) error {
    if command.ID == "" || command.Amount == 0 {
        return errors.New("bad request")
    }

    event := events.WithdrawFundEvent{
        ID:     command.ID,
        Amount  command.Amount,
    }
    log.Println("%#v", event)
    return obj.eventProducer.Produce(event)
}

func (obj accountService) CloseAccount(command commands.CloseAccountCommand) error {
    if command.ID == "" {
        return errors.New("bad request")
    }

    event := event.CloseAccountEvent{
        ID: command.ID,
    }
    log.Println("%#v", event)
    return obj.eventProducer.Produce(event)
}
```

```shell
$ go get github.com/gofiber/fiber/v2
```

```go
// controllers/account.go
package controllers

type AccountController interface {
    OpenAccount(c *fiber.Ctx) error
    DepositAccount(c *fiber.Ctx) error
    WithdrawAccount(c *fiber.Ctx) error
    CloseAccount(c *fiber.Ctx) error
}

type accountController struct {
    accountService services.AccountService
}

func NewAccountController(accountService services.AccountService) AccountController {
    return accountController{accountService}
}

func (obj accountController) OpenAccount(c *fiber.Ctx) error {
    command := command.OpenAccountCommand{}

    err := c.BodyParser(&command)
    if err != nil {
        return err
    }

    id, err := obj.accountService.OpenAccount(command)
    if err != nil {
        return err
    }

    c.Status(fiber.StatusCreated)
    return c.JSON(fiber.Map{
        "message":  "open account success",
        "id":       id,
    })
}

func (obj accountController) DepositAccount(c *fiber.Ctx) error {
    command := command.DepositFundCommand{}
    err := c.BodyParser(&command)
    if err != nil {
        return err
    }

    err := obj.accountService.DepositFund(command)
    if err != nil {
        return err
    }
    return c.JSON(fiber.Map{
        "message": "deposit fund success",
    })
}

func (obj accountController) WithdrawAccount(c *fiber.Ctx) error {
    command := command.WithdrawFundCommand{}
    err := c.BodyParser(&command)
    if err != nil {
        return err
    }

    err := obj.accountService.WithdrawFund(command)
    if err != nil {
        return err
    }
    return c.JSON(fiber.Map{
        "message": "withdraw fund success",
    })
}

func (obj accountController) CloseAccount(c *fiber.Ctx) error {
    command := command.CloseAccountCommand{}
    err := c.BodyParser(&command)
    if err != nil {
        return err
    }

    err := obj.accountService.CloseAccount(command)
    if err != nil {
        return err
    }
    return c.JSON(fiber.Map{
        "message": "close account success",
    })
}
```

```go
// main.go
package main

def main() {
    producer, err := sarama.NewSyncProducer(viper.GetStringSlice("kafka.servers"), nil)
    if err != nil {
        panic(err)
    }
    defer producer.Close()

    eventProducer := services.NewEventProducer(producer)
    accountService := services.NewAccountService(eventProducer)
    accountController := controllers.NewAccountController(accountService)

    app := fiber.New()

    app.Post("/openAccount", accountController.OpenAccount)
    app.Post("/depositFund", accountController.DepositFund)
    app.Post("/withdrawFund", accountController.WithdrawFund)
    app.Post("/closeAccount", accountController.CloseAccount)

    app.Liten(":8000")
}
```

```shell
$ curl -H 'content-type:application/json' localhost:8000/openaccount \
  -d '{"AccountHolder": "Admin", "AccountType": 1, "OpeningBalance": 1000}' \
  -i
```

## References

-
