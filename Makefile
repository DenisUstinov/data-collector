up:
	docker compose -f docker-compose.dc.yml -p dc up --build -d --force-recreate
	docker compose -f docker-compose.dc.yml -p dc logs -f

bg:
	docker compose -f docker-compose.dc.yml -p dc up -d --build --force-recreate

down:
	docker compose -f docker-compose.dc.yml -p dc down

cl:
	docker compose -f docker-compose.dc.yml -p dc down --volumes --rmi all --remove-orphans