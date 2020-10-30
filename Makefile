restart:
	docker-compose rm -s -f
	docker-compose up --build
