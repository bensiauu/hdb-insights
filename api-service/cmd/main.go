package main

import (
	"fmt"
	"log"
	"os"

	"github.com/bensiauu/hdb-insights/internal/api"
	"github.com/bensiauu/hdb-insights/internal/db"
	"github.com/gofiber/fiber/v2"
	"github.com/joho/godotenv"
)

func main() {
	if err := godotenv.Load(); err != nil {
		fmt.Println("No .env file found, using env vars")
	}

	db.Init()
	db.Migrate()

	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}
	app := fiber.New()
	api.RegisterRoutes(app)

	log.Printf("Server running on localhost:%s", port)
	if err := app.Listen(":" + port); err != nil {
		log.Fatal(err)
	}
}
