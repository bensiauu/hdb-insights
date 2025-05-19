package db

import (
	"log"
	"os"

	"github.com/bensiauu/hdb-insights/internal/model"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

var DB *gorm.DB

func Init() {
	dsn := os.Getenv("DATABASE_URL")
	if dsn == "" {
		log.Fatal("DATABASE_URL not set")
	}

	var err error
	DB, err = gorm.Open(postgres.Open(dsn), &gorm.Config{})
	if err != nil {
		log.Fatalf("Failed to connect to DB: %v", err)
	}
}

func Migrate() {
	if err := DB.AutoMigrate(&model.ResaleRecord{}); err != nil {
		log.Fatalf("Failed to migrate schema: %v", err)
	}

	log.Println("Schema migrated successfully")
}
