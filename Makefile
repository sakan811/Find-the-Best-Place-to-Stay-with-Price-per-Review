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
	cd auth_headers && python extract_booking_headers.py

auth-headers-ruff:
	cd auth_headers && ruff check . --fix && ruff format .

auth-headers-test:
	cd auth_headers && pytest

frontend-dev:
	cd frontend && npm run dev

frontend-test:
	cd frontend && npm run test

docker-compose-up:
	docker-compose up -d

docker-compose-down:
	docker-compose down

docker-compose-clean:
	docker-compose down --volumes --remove-orphans