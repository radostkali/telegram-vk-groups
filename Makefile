restart:
	docker-compose rm -s -f
	docker-compose up --build -d

up:
	docker-compose up -d --build

stop:
	docker-compose stop

log:
	docker-compose logs --follow

shell:
	docker exec -it telegram_memes_bot bash