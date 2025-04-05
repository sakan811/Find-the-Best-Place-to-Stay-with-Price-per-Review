backend-dev:
	cd backend && python manage.py runserver

backend-test:
	cd backend && pytest

backend-migrations:
	cd backend && python manage.py makemigrations

backend-migrate:
	cd backend && python manage.py migrate

backend-ruff:
	cd backend && ruff check . --fix && ruff format .

auth-headers:
	cd auth_headers && python app.py

auth-headers-ruff:
	cd auth_headers && ruff check . --fix && ruff format .

auth-headers-test:
	cd auth_headers && python -m pytest

frontend-dev:
	cd frontend && npm run dev

frontend-test:
	cd frontend && npm run test

health-endpoint:
	curl -s http://localhost:4000/health

extract-headers-endpoint:
	curl -s http://localhost:4000/extract-headers

extract-headers-with-save:
	curl -s "http://localhost:4000/extract-headers?save=true"

get-headers-endpoint:
	curl -s http://localhost:4000/get-headers

test-all-endpoints:
	curl -s http://localhost:4000/health && \
	curl -s http://localhost:4000/extract-headers && \
	curl -s "http://localhost:4000/extract-headers?save=true" && \
	curl -s http://localhost:4000/get-headers

docker-compose-auth-headers:
	docker-compose --profile phase1 up -d

docker-compose-app:
	docker-compose --profile phase2 up -d

docker-compose-build-auth-headers:
	docker-compose -f docker-compose.build.yml --profile phase1 up -d --build

docker-compose-build-app:
	docker-compose -f docker-compose.build.yml --profile phase2 up -d --build

docker-compose-down:
	docker-compose --profile phase1 down && \
	docker-compose --profile phase2 down

docker-compose-clean:
	docker-compose --profile phase1 down --volumes --remove-orphans && \
	docker-compose --profile phase2 down --volumes --remove-orphans