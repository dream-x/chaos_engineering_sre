package main 

import (
	"context"
	"fmt"
	"net/http"
	"time"
    
    "github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
	redis "github.com/redis/go-redis/v9"
)

var ctx = context.Background()

func main () {
	rdb := redis.NewClient(&redis.Options{
		Addr: "localhost:16379",
		Password: "",
		DB: 0,
	})

	pong, err := rdb.Ping(ctx).Result()
	if err != nil {
		panic(err)
	}
	fmt.Println(pong)

	e := echo.New()
    e.GET("/testme", func(c echo.Context) error {
		listKeys(rdb)
        return c.String(http.StatusOK, "Hello, Toxiproxy!")
    })

	e.Use(middleware.TimeoutWithConfig(middleware.TimeoutConfig{
		Timeout: 2 * time.Second, 
	}))

    e.Logger.Fatal(e.Start(":1323"))
}

func listKeys(rdb *redis.Client) {
	iter := rdb.Scan(ctx, 0, "", 0).Iterator()
	if err := iter.Err(); err != nil {
		panic(err)
	}
}
