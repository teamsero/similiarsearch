db/up:
	docker compose up -d

db/down:
	docker compose down

init:
	pip install -r requirements.txt

seek:
	go run seek.go
run:
	python3 qdrant.py
run2:
	python3 qdrant_v2.py
