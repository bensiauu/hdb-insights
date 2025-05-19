package api

import "github.com/gofiber/fiber/v2"

func RegisterRoutes(app *fiber.App) {
	api := app.Group("/api/v1")
	api.Get("/resale-data", GetResaleData)
	api.Get("/trends", GetTrends)
	api.Post("/predict", PredictResalePrice)

	admin := api.Group("/admin")
	admin.Post("/sync", TriggerSync)
}
