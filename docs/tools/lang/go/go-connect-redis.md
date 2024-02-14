# GO Advance with Redis

Create project folder in your local,

```text
goredis
|--> docker-compose.yml
|--> go.mod
|--> main.go
```

**Table of Contents**:

- [Setup Redis](#setup-redis)
- []
- [Create API Server with GO](#create-api-server-with-go)

## Setup Redis

- Install Redis CLI, use `redis-cli`
- Install Redis Server from Docker Container

```yaml
version: "3.9"
services:
  redis:
    image: redis
    container_name: redis
    ports:
      - "6379:6379"
```

```shell
docker-compose up
```

```shell
$ redis-cli
127.0.0.1:6379$ ping
PONG
127.0.0.1:6379$ set name value
OK
127.0.0.1:6379$ get name
"value"
```

> **Note**: \
> If you want to delete value in redis with life-cycle, you can use `ex` such as delete value in 5 seconds:
> `set name hello ex 5`

### Persisted Data from Redis

We want to config redis server to persisted data (snapshot data) when it has some
problem take server down. First, we create data folder and file `config/redis.conf`:

```text
goredis
|--> config
|    |--> redis.conf
|--> data
|    |--> redis
|--> ...
```

Copy configuration data with your version from redis official
[redis.io/topics/config](https://redis.io/topics/config)
document to this file.

```text
# Allow other network to connect redis
bind 0.0.0.0

# Disable Snapshot and use empty value
save ""

# Enable Append-only mode
appendonly yes
appendfilename "appendonly.aof"
```

Edit the docker-compose file:

```yaml
# docker-compose.yml
version: "3.9"
services:
  redis:
    image: redis
    container_name: redis
    ports:
      - "6379:6379"
    volumes:
      - ./data/redis:/data
      - ./config/redis.conf:/redis.conf
    command: redis-server /redis.conf
```

## Create API Server with GO

We use `fiber` for API server.

```shell
go get github.com/gofiber/fiber/v2
```

```go
// main.go
package main

import github.com/gofiber/fiber/v2

func main() {
    app := fiber.New()
    app.Get("/hello", func(c *fiber.Ctx) error {
        return c.SendString("Hello World")
    })
    app.Listen(":8000")
}
```

## Load Test

We use `k6`.

```text
goredis
|--> ...
|--> scripts
|    |--> test.js
|--> ...
```

```yaml
# docker-compose.yml
version: '3.9'
services:

    ...

    k6:
        image: loadimpact/k6
        container_name: k6
        volumes:
            - ./scripts:/scripts
```

```js
import http from "k6/http";

export default function () {
  http.get("http://host.docker.internal:8000/hello");
}
```

- Load test with 5 users and 5 seconds

```shell
docker compose run --rm k6 run /scripts/test.js -u5 -d5s
```

### Edit configuration in test file

```js
import http from 'k6/http'

export let: options = {
    vus: 5,
    duration: '5s'
}

export default function() {
    http.get('http://host.docker.internal:8000/hello')
}
```

## Create TimeSeries Database and Grafana

We use `InfluxDB` for keep data from `k6` and use Grafana to visualize test dashboard.
If we use InfluxDB version >= 2.0.0, it will support build-in dashboard.

```yaml
# docker-compose.yml
version: '3.9'
services:

    ...

    k6:
        ...
        environment:
            - K6_OUT=influxdb=http://influxdb:8086/k6
        ...

    influxdb:
        image: influxdb:1.8.10  # Version 2.0.0 does not support for k6 yet
        container_name: influxdb
        environment:
            - INFLUXDB_DB=k6
            - INFLUXDB_HTTP_MAX_BODY_SIZE=0
        ports:
            - "8086:8086"
        volumes:
            - ./data/influxdb:/var/lib/influxdb

    grafana:
        image: grafana/grafana
        container_name: grafana
        environment:
            - GF_AUTH_ANONYMOUS_ENABLED=true
            - GF_AUTH_ANONYMOUS_ORG_ROLE=Admin  # This is bad practice!!!
        ports:
            - "3000:3000"
        volumes:
            - ./data/grafana:/var/lib/grafana
```

```shell
docker compose up influxdb grafana
```

After `Grafana` server run successful, we will go to `localhost:3000` and Add
`InfluxDB` data source with these configurations:

- URL: http://influxdb:8086
- Database: k6

Go to `grafana.com/grafana/dashboard` and search k6 dashboard. We will copy dashboard ID
from official to Local Grafana server in import menu.

## Use-case

```text
goredis
|--> ...
|--> handlers
|--> repositories
|    |--> product_redis.go
|    |--> product_db.go
|    |--> product.go
|--> services
|--> go.mod
|--> main.go
```

```shell
go get gorm.io/gorm
go get gorm.io/driver/mysql
go get github.com/go-redis/redis/v8
```

```yaml
# docker-compose.yml
version: '3.9'
services:

    ...

    mariadb:
        image: mariadb
        container_name: mariadb
        environment:
            - MARIADB_ROOT_PASSWORD=P@ssw0rd
            - MARIADB_DATABASE=product
        ports:
            - "3306:3306""
        volumes:
            - ./data/mariadb:/var/lib/mysql
```

### Repositories

```go
// repositories/product.go
package repositories

...

type product struct {
    ID          int
    Name        string
    Quantity    int
}

type ProductRepository interface {
    GetProducts() ([]product, error)
}

func mockData(db *gorm.DB) error {

    var count int64
    db.model(&product{}).Count(&count)
    if count > 0 {
        return nil
    }

    seed := rand.NewSource(time.Now().UnixNano())
    random := rand.New(seed)

    products := []product{}
    for i := 0; i < 5000; i++ {
        products = append(products, product{
            Name:       fmt.Sprintf("Product%v", i + 1),
            Quantity:   random.Intn(100),
        })
    }
    return db.Create(&products).Error
}
```

```go
// repositories/product_db.go
package repositories

...

type productRepositoryDB struct {
    db *gorm.DB
}

func NewProductRepositoryDB(db *gorm.DB) ProductRepository {
    db.AutoMigrate(&product{})
    mockData(db)
    return productRepositoryDB{db: db}
}

func (r productRepositoryDB) GetProducts() (products []product, err error) {
    err = r.db.Order("quantity desc").Limit(30).Find(&products)
    if err != nil {
        return nil, err
    }
    return products, err
}
```

```go
// repositories/product_redis.go
package repositories

...

type productRepositoryRedis struct {
    db *gorm.DB
    redisClient *redis.Client
}

func NewProductRepositoryDB(db *gorm.DB, redisClient *redis.Client) ProductRepository {
    db.AutoMigrate(&product{})
    mockData(db)
    return productRepositoryRedis{db, redisClient}
}

func (r productRepositoryRedis) GetProducts() (products []product, err error) {

    key := "repository::GetProcusts"

    // Chack data in Redis
    productsJson, err := r.redisClient.Get(context.Background(), key).Result()
    if err == nil {
        err = json.Unmarshal([]byte(productsJson, &products)
        if err == nil {
            return products, nil
        }
    }

    err = r.db.Order("quantity desc").Limit(30).Find(&products)
    if err != nil {
        return nil, err
    }

    // Import to Redis
    data, err := json.Marshal(products)
    if err != nil {
        return nil, err
    }
    err = r.redisClient.Set(context.Background(), key, string(data), time.Second * 10).Err()
    if err != nil {
        return nil, err
    }
    return products, err
}
```

### Services

```go
// services/catalog.go
package services

type Product struct {
    ID       int    `json:"id"`
    Name     string `json:"name"`
    Quantity int    `json:"quantity"`
}

type CatalogService interface {
    GetProducts() ([]Product, error)
}
```

```go
// services/catalog_service.go
package services

...

type catalogService struct {
    productRepo repositories.ProductRepository
}

func NewCatalogService(productRepo repositories.ProductRepository) CatalogService {
    return catalogService{productRepo}
}

func (s catalogService) GetProducts() (products []Product, err error) {
    productsDB, err := s.productRepo.GetProducts()
    if err != nil {
        return nil, err
    }

    for _, p := range productsDB {
        products = append(products, Product{
            ID:         p.ID,
            Name:       p.Name,
            Quantity:   p.Quantity,
        })
    }
    return products, nil
}
```

```go
// services/catalog_redis.go
package services

...

type catalogServiceRedis struct {
    productRepo repositories.ProductRepository
    redisClient *redis.Client
}

func NewCatalogServiceRedis(productRepo repositories.ProductRepository, redisClient *redis.Client) CatalogService {
    return catalogServiceRedis{productRepo, redisClient}
}

func (s catalogServiceRedis) GetProducts() (products []Product, err error) {
    key := "services::GetProcusts"

    // Chack data in Redis
    if productsJson, err := s.redisClient.Get(context.Background(), key).Result(); err == nil {
        if json.Unmarshal([]byte(productsJson, &products) == nil {
            return products, nil
        }
    }

    // Repository
    productsDB, err := s.productRepo.GetProducts()
    if err != nil {
        return nil, err
    }

    for _, p := range productsDB {
        products = append(products, Product{
            ID:         p.ID,
            Name:       p.Name,
            Quantity:   p.Quantity,
        })
    }

    // Import to Redis
    if data, err := json.Marshal(products); err == nil {
        s.redisClient.Set(context.Background(), key, string(data), time.Second * 10)
    }
    return products, nil
}
```

### Handler

```go
// handlers/catalog.go
package handlers

...

type CatalogHandler interface {
    GetProducts(c *fiber.Ctx) error
}
```

```go
// handlers/catalog.handlers.go
package handlers

...

type catalogHandler struct {
    catalogSrv services.CatalogService
}

func NewCatalogHandler(catalogSrv services.CatalogService) CatalogHandler {
    return catalogHandler{catalogSrv}
}

func (h catalogHandler) GetProducts(c *fiber.Ctx) error {
    products, err := h.catalogSrv.GetProducts()
    if err != nil {
        return err
    }
    response := fiber.Map{
        "status": "ok",
        "products": products,
    }
    return c.JSON(response)
}
```

```go
// handlers/catalog_redis.go

package handlers

...

type catalogHandlerRedis struct {
    catalogSrv services.CatalogService
    redisClinet *redis.Client
}

func NewCatalogHandlerRedis(catalogSrv services.CatalogService, redisClient *redis.Client) catalogHandlerRedis {
    return catalogHandlerRedis{catalogSrv, redisClient}
}

func (h catalogHandlerRedis) GetProducts(c *fiber.Ctx) error {
    key := "handler::GetProcusts"

    // Chack data in Redis
    if responseJson, err := s.redisClient.Get(context.Background(), key).Result(); err == nil {
        c.Set("Content-Type", "applicatin/json")
        return c.SendString(responseJson)
    }

    products, err := h.catalogSrv.GetProducts()
    if err != nil {
        return err
    }
    response := fiber.Map{
        "status": "ok",
        "products": products,
    }

    // Import to Redis
    if data, err := json.Marshal(response); err == nil {
        h.redisClient.Set(context.Background(), key, string(data), time.Second * 10)
    }

    return c.JSON(response)
}
```

### Database

```go
// main.go

...

func main() {
    db := initDatabase()
    redisClient := initRedis()

    productRepo := repositories.NewProductRepositoryDB(db)
    // // Or,
    // productRepo := repositories.NewProductRepositoryRedis(db, redisClient)
    // products, err := productRepo.GetProducts()

    productService := services.NewCatalogService(productRepo)
    // // Or,
    // productService := services.NewCatalogServiceRedis(productRepo, redisClient)
    // products, err := productService.GetProducts()

    productHandler := handler.NewCatalogHandler(productService)
    // Or,
    productHandler := handler.NewCatalogHandlerRedis(productService, redisClient)

    app := fiber.New()
    app.Get("/products", productHandler.GetProducts)
    app.Listen(":8000")
}

func initDatabase() *gorm.DB {
    dial := mysql.Open("root:P@ssw0rd@tcp(localhost:3306)/product")
    db, err := gorm.Open(dial, &gorm.Config{})
    if err != nil {
        panic(err)
    }
    return db
}

func initRedis() *redis.Client {
    return redis.NewClient(&redis.Option{
        Addr: "localhost:6379"
    })
}
```

```shell
curl localhost:8000/products | jq
```

## References

-
