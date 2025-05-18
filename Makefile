dev:
	npm run dev

test:
	npm run test

lint:
	npm run lint

format:
	npm run format

up:
	docker compose up -d

build:
	docker compose -f docker-compose.build.yml up -d --build

down:
	docker compose down

clean:
	docker compose down --volumes --remove-orphans

rm-image:
	docker rmi sakanbeer88/hotel-value-analyzer:latest
