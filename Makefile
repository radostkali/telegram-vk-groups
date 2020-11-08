restart:
	docker-compose rm -s -f
	docker-compose up --build

up:
	docker-compose up -d --build

stop:
	docker-compose stop

logs:
	docker-compose logs --follow
