dev:
	npm run dev

build:
	npm run build

test:
	npm run test

lint:
	npm run lint

format:
	npm run format

up:
	docker compose --profile pull up -d

up-build:
	docker compose --profile build up -d --build

down:
	docker compose --profile pull down

down-build:
	docker compose --profile build down

clean:
	docker compose --profile pull down --volumes --remove-orphans && \
	docker rmi sakanbeer88/hotel-value-analyzer:latest

clean-build:
	docker compose --profile build down --volumes --remove-orphans && \
	docker rmi sakanbeer88/hotel-value-analyzer:latest
