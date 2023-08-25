package main

import (
	"encoding/json"
	"fmt"
	"os"

	"github.com/alok87/goutils/pkg/random"
)

type Card struct {
	ID              int     `json:"id"`
	Title           string  `json:"title"`
	Desc            string  `json:"desc"`
	Exp             int     `json:"exp"`
	Cost            Cost    `json:"cost"`
	ReputationLevel int     `json:"reputation_level"`
	Star            float64 `json:"star"`
}

type Cost struct {
	Price       int    `json:"price"`
	Unit        string `json:"unit"`
	Concurrency string `json:"concurence"`
}

var (
	costs = []Cost{
		{
			Price:       10,
			Unit:        "Per hour",
			Concurrency: "USD",
		},
		{
			Price:       5,
			Unit:        "Per hour",
			Concurrency: "USD",
		},
		{
			Price:       3,
			Unit:        "Per hour",
			Concurrency: "USD",
		},
		{
			Price:       200000,
			Unit:        "Per hour",
			Concurrency: "VND",
		},
		{
			Price:       2000,
			Unit:        "Per month",
			Concurrency: "USD",
		},
	}
)

type SeekJob struct {
	Title string `json:"title"`
	Desc  string `json:"desc"`
}

func main() {
	seekjobs := getSeekJob()
	maxItem := 20
	cards := make([]Card, 0)
	for i := 0; i < maxItem; i++ {

		randomTitleIndex := random.RangeInt(0, len(seekjobs)-1, 1)[0]
		randomCost := random.RangeInt(0, len(costs)-1, 1)[0]
		cards = append(cards, Card{
			ID:              i,
			Title:           seekjobs[randomTitleIndex].Title,
			Desc:            seekjobs[randomTitleIndex].Desc,
			Exp:             randomTitleIndex,
			ReputationLevel: randomCost,
			Cost:            costs[randomCost],
			Star:            float64(randomCost),
		})
	}

	jsonData, err := json.Marshal(cards)
	if err != nil {
		fmt.Println("Error marshaling JSON:", err)
		return
	}

	file, err := os.Create("seek.json")
	if err != nil {
		fmt.Println("Error creating JSON file:", err)
		return
	}
	defer file.Close()

	_, err = file.Write(jsonData)
	if err != nil {
		fmt.Println("Error writing JSON file:", err)
		return
	}

	fmt.Println("JSON file created successfully!")
}

func getSeekJob() []SeekJob {
	file, err := os.Open("seekjob.json")
	if err != nil {
		fmt.Println("Lỗi khi mở file:", err)
	}
	defer file.Close()

	var jobs []SeekJob
	json.NewDecoder(file).Decode(&jobs)

	return jobs
}
