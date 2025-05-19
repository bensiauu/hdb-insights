package api

import "github.com/gofiber/fiber/v2"

func GetResaleData(c *fiber.Ctx) error {
	return c.JSON(fiber.Map{"message": "resale data placeholder"})
}

func GetTrends(c *fiber.Ctx) error {
	return c.JSON(fiber.Map{"message": "trends placeholder"})
}

func PredictResalePrice(c *fiber.Ctx) error {
	return c.JSON(fiber.Map{"message": "predict placeholder"})
}

func TriggerSync(c *fiber.Ctx) error {
	return c.JSON(fiber.Map{"message": "sync placeholder"})
}
