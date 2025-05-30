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
	docker compose --profile pull down --rmi local --remove-orphans --volumes

clean-build:
	docker compose --profile build down --rmi local --remove-orphans --volumes
