package main

import (
	"fmt"
	"github.com/labstack/echo/v4"
	"math/rand"
	"time"
)

func main() {
	e := echo.New()
	e.GET("/", func(c echo.Context) error {
		responseCodes := []int{200, 201, 301, 400, 500}
		rand.Seed(time.Now().UnixNano())
		respcode := responseCodes[rand.Intn(len(responseCodes))]
		fmt.Println(respcode)
		return c.String(respcode, "Hello, World!")
	})
	e.Logger.Fatal(e.Start(":1323"))
}
