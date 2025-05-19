package model

import "time"

type ResaleRecord struct {
	ID             uint      `gorm:"primaryKey" json:"-"`
	Month          time.Time `gorm:"type:date" json:"month"`
	Town           string    `json:"town"`
	FlatType       string    `json:"flat_type"`
	Block          string    `json:"block"`
	StreetName     string    `json:"street_name"`
	StoreyRange    string    `json:"storey_range"`
	FloorAreaSqm   float64   `json:"floor_area_sqm"`
	LeaseCommence  int       `json:"lease_commence_date"`
	RemainingLease string    `json:"remaining_lease"`
	ResalePrice    int       `json:"resale_price"`
}
