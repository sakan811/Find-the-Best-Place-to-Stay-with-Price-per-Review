dev:
	npm run dev

test:
	npm run test

compose:
	docker compose up -d

compose-build:
	docker compose -f docker-compose.build.yml -d --build

compose-down:
	docker compose down

compose-clean:
	docker compose down --volumes --remove-orphans

rm-image:
	docker rmi sakanbeer88/hotel-value-analyzer:latest
