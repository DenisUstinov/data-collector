up:
	docker compose  up --build -d --force-recreate
	docker compose logs -f
bg:
	docker compose up -d --build --force-recreate

down:
	docker compose down