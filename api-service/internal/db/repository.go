package db

import "github.com/bensiauu/hdb-insights/internal/model"

func GetResaleData(town, flatType string) ([]model.ResaleRecord, error) {
	var results []model.ResaleRecord
	query := DB
	if town != "" {
		query = query.Where("town = ?", town)
	}

	if flatType != "" {
		query = query.Where("flat_type = ?", flatType)
	}

	if err := query.Order("month DESC").Limit(100).Find(&results).Error; err != nil {
		return nil, err
	}
	return results, nil
}
