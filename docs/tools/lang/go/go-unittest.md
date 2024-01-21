# GO Unittest

**Update**: `2023-05-04` |
**Tag**: `GO` `Unittest`

## Test

```go
// services/grade_test.go
package services_test

import "testing"

func TestCheckGrade(t *testing.T) {
    // test function for CheckGrade(80)
    grade := services.CheckGrade(80)
    expected := "A"

    if grade != expected {
        t.Errorf("get %v expected %v", grade, expected)
    }
}
```

```go
// services/grade.go
package services

func CheckGrade(score int) string {
    switch {
        case score >= 80:
            return "A"
        case score >= 70:
            return "B"
        case score >= 60:
            return "C"
        case score >= 50:
            return "D"
        default:
            return "F"
    }
}
```

```shell
go test <module-name>/serices -v

go test <module-name>/serices -v -run=TestCheckGrade

go test ./... -v
```

```shell
# Get test coverage
go test <module-name>/services -cover
```

## Create Sub-test

```go
// services/grade_test.go

func TestCheckGrade(t *testing.T) {
    t.Run("A", func(t *testing.T) {
        grade := services.CheckGrade(80)
        expected := "A"

        if grade != expected {
            t.Errorf("get %v expected %v", grade, expected)
        }
    })

    t.Run("B", func(t *testing.T) {
        grade := services.CheckGrade(70)
        expected := "B"

        if grade != expected {
            t.Errorf("get %v expected %v", grade, expected)
        }
    })
}
```

```shell
go test <module-name>/services -run="TestCheckGrade/A" -v
```

### Change to be Good Coverage

```go
// services/grade_test.go

func TestCheckGrade(t *testing.T) {
    type testCase struct {
        name     string
        score    int
        expected string
    }

    cases := []testCase{
        {name: "a", score: 80, expected: "A"},
        {name: "b", score: 70, expected: "B"},
        {name: "c", score: 60, expected: "C"},
        {name: "d", score: 50, expected: "D"},
        {name: "f", score: 0, expected: "F"},
    }

    for _, c := range cases {
        t.Run(c.name, func(t *testing.T) {
            grade := services.CheckGrade(c.score)
            if grade != c.expected {
                t.Errorf("get %v expected %v", grade, expected)
            }
        })
    }

}
```

## Benchmark

```go
// services/grade_test.go

func BenchmarkCheckGrade(b *testing.B) {
    for i := 0; i < b.N; i ++ {
        services.CheckGrade(80)
    }
}
```

```shell
go test <module-name>/services -bench=.

# For check memory benchmark
go test <module-name>/services -bench=. -benchmem
```

## Example

```shell
go get golang.org/x/tools/cmd/godoc
```

```go
// services/grade_test.go

func ExampleCheckGrade() {
    grade := services.CheckGrade(80)
    fmt.Println(grade)
    // Output: A
}
```

```shell
godoc -http=:8000
```

## Mock

```shell
go get github.com/stretchr/testify
```

```go
// main.go
package main

func main() {
    c := CustomerRepositoryMock{}
    c.On("GetCustomer", 1).Return("Tom", 18, nil)
    c.On("GetCustomer", 2).Return("", 0, errors.New("not found"))

    // Try to use
    name, age, err := c.GetCustomer(1)
    if err != nil {
        fmt.Println(err)
        return
    }
    fmt.Println(name, age)
}

type CustomerRepository interface {
    GetCustomer(id int) (name string, age int, err error)
}

type CustomerRepositoryMock struct {
    mock.Mock
}

func (m *CustomerRepositoryMock) GetCustomer(id int) (name string, age int, err error) {
    args := m.Called(id)
    return args.String(0), args.Int(1), args.Error(2)
}
```

### Implement Mock

```go
// repositories/promotion_mock.go
package repositories

type promotionRepositoryMock struct {
    mock.Mock
}

func NewPromotionRepositoryMock() *promotionRepositoryMock{
    return &promotionRepositoryMock{}
}

func (m *promotionRepositoryMock) GetPromotion() (Promotion, error) {
    args := m.Called()
    // Cast type of first value to Promotion
    return args.Get(0).(Promotion), args.Error(1)
}
```

```go
// services/promotion_test.go
package services_test

import (
    "<module-name>/repositories"
    "<module-name>/services"
    "testing"
)

func TestPromotionCalculateDiscount(t *testing.T) {

    // Arrage
    promoRepo := repositories.NewPromotionRepositoryMock()
    promoReop.On("GetPromotion").Return(repositories.Promotion{
        ID:              1,
        PurchaseMin:     100,
        DiscountPercent: 20,
    }, nil)


    promoService := services.NewPromotionService(promoRepo)

    // Act
    discount, _ := promoService.CalculateDiscount(100)
    expected := 80

    // Assert
    assert.Equal(t, expected, discount)
}
```

### Change Code

```go
// services/promotion_test.go
package services_test

func TestPromotionCalculateDiscount(t *testing.T) {

    type testCase struct {
        name            string
        purchaseMin     int
        discountPercent int
        amount          int
        expected        int
    }

    cases := []testCase{
        {name: "applied 100", purchaseMin: 100, discountPercent: 20, amount: 100, expected: 80},
        {name: "applied 200", purchaseMin: 100, discountPercent: 20, amount: 200, expected: 160},
        {name: "applied 300", purchaseMin: 100, discountPercent: 20, amount: 300, expected: 240},
        {name: "not applied 50", purchaseMin: 100, discountPercent: 20, amount: 50, expected: 50},
    }

    for _, c := range cases {
        t.Run(c.name, func(t *testing.T) {
            // Arrage
            promoRepo := repositories.NewPromotionRepositoryMock()
            promoReop.On("GetPromotion").Return(repositories.Promotion{
                ID:              1,
                PurchaseMin:     c.purchaseMin,
                DiscountPercent: c.discountPercent,
            }, nil)


            promoService := services.NewPromotionService(promoRepo)

            // Act
            discount, _ := promoService.CalculateDiscount(c.amount)
            expected := c.expected

            // Assert
            assert.Equal(t, expected, discount)
        })
    }

    t.Run("purchase amount zero", func(t *testing.T) {
        promoRepo := repositories.NewPromotionRepositoryMock()
        promoReop.On("GetPromotion").Return(repositories.Promotion{
            ID:              1,
            PurchaseMin:     100,
            DiscountPercent: 20,
        }, nil)

        promoService := services.NewPromotionService(promoRepo)

        // Act
        _, err := promoService.CalculateDiscount(0)

        // Assert
        assert.ErrorIs(t, err, services.ErrZeroAmount)
        promoRepo.AssertNotCalled(t, "GetPromotion")
    })

    t.Run("repository error", func(t *testing.T) {
        promoRepo := repositories.NewPromotionRepositoryMock()
        promoReop.On("GetPromotion").Return(repositories.Promotion{}, errors.New(""))

        promoService := services.NewPromotionService(promoRepo)

        // Act
        _, err := promoService.CalculateDiscount(100)

        // Assert
        assert.ErrorIs(t, err, services.ErrRepository)
    })
}
```

## Tags

```go
// handlers/promotion_test.go
//go:build unit

...
```

```shell
go test <module-name>/handlers -v -tags=unit

go test <module-name>/handlers -v -tags=integation,unit
```

## References

- https://youtu.be/Wd3O6GcA20w
