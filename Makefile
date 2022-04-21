PROJECT_NAME=hindsite

start:
	@docker-compose up --detach
	sleep 5
	@docker exec -it hindsite python manage.py makemigrations
	@docker exec -it hindsite python manage.py migrate
	@docker exec -it hindsite python manage.py populate_organizations


superuser:
	@docker exec -it hindsite python manage.py createsuperuser


stop:
	@docker-compose stop
	@docker-compose down --volumes --remove-orphans
	@docker image rmi -f hindsite