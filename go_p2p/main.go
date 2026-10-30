package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"sync"
)

type State struct {
	Energy float64 `json:"energy"`
	Tick   int     `json:"tick"`
}

var (
	mu    sync.Mutex
	state = State{Energy: 1000.0, Tick: 0}
)

func main() {
	http.HandleFunc("/sync", func(w http.ResponseWriter, r *http.Request) {
		mu.Lock()
		defer mu.Unlock()

		if r.Method == "POST" {
			var newState State
			json.NewDecoder(r.Body).Decode(&newState)
			if newState.Tick > state.Tick {
				state = newState
			}
		}
		json.NewEncoder(w).Encode(state)
	})

	fmt.Println("🌐 OuroborosX P2P Node running on :8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
