### summary
This is a wagtail app boiler plate. To run:
`cd app`
`docker build -t app .`


## basic setup
setup wagtail with docker: https://learnwagtail.com/tutorials/how-install-wagtail-docker/
- I created a virtualenv to create wagtail first, thenstarted a docker container

basic commands:
pip3 install virtualenv
export PATH=$PATH:~/Library/Python/3.8/bin
virtualenv venv    
source venv/bin/activate
pip install wagtail
wagtail start app
source deactivate
delete /venv
docker build -t app . 
docker run -p 8000:8000 app
- in new terminal
docker container ls - get id of container
docker exec -it <container-id> /bin/bash
./manage.py createsuperuser
./manage.py runserver 0.0.0.0:8000


create image: docker build -t app .
list all images: docker images 
delete all images: docker system prune -a
list all containers: docker container ls
stop container: docker stop id
step into container: docker exec -it <container_id> /bin/bash

## commands
### running django commands
`docker-compose run --rm app sh -c "python manage.py _________"`
or 
`docker-compose run app python manage.py _________`

`docker-compose run --rm app sh -c "python manage.py shell" `


### start app locally for development
`cd Documents/terry/projects/deploy-django-with-docker-compose`
`docker-compose build`
`docker-compose up`
`docker-compose run --rm app sh -c "python manage.py createsuperuser"`
go to `http://127.0.0.1:8000/admin/`
stop container `ctrl + c`


## move docker files to root
move Docker + .dockerignore + requirements.txt files to the root
In Dockerfile:
- RUN python app/manage.py collectstatic --noinput --clear
- CMD cd app; set -xe; python manage.py migrate --noinput; gunicorn app.wsgi:application


## create scripts folder to hold all the scripts
create /script/run.sh folder and file
add CMD commands from Dockerfile to the run.sh file
- CMD cd app; set -xe; python manage.py migrate --noinput; gunicorn app.wsgi:application
In the Dockerfile:
- COPY ./scripts /scripts (not sure this is required)
- CMD ["run.sh"] (remove the old CMD command)

## add docker-compose file and set database to postgres
- base settings: app/app/settings/base.py
- add wait_for_db command to app doesn't start until database is running

## add celery + redis
- added broker url in settings.base
- created basic `add` task in home.tasks

## add elasticsearch + test data
- add Post + Retry models
- add document module to map above models to elasticsearch
- add load_posts command to add dummy data to test elastic search with
- load posts with: `docker-compose run web python manage.py load_posts 20`
- test elasticsearch is working: `curl -X GET localhost:9200/_cluster/health`
- https://www.obytes.com/blog/building-a-full-text-search-app-using-django-docker-and-elasticsearch
- https://github.com/obytes/django-elasticsearch-example

