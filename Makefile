up:
	docker compose up -d

down:
	docker compose down && docker network prune --forse