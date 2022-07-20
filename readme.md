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

### start app locally for production testing
`cd Documents/terry/projects/deploy-django-with-docker-compose`
`docker-compose -f docker-compose-deploy.yml down --volumes`
`docker-compose -f docker-compose-deploy.yml build`
`docker-compose -f docker-compose-deploy.yml up` add `-d` to the end to run in the background
`docker-compose -f docker-compose-deploy.yml run --rm app sh -c "python manage.py createsuperuser"`
go to `http://127.0.0.1/admin/`

### start app in ec2 instance
`cd documents/terry/keypairs`
`ssh -i mac_ec2.pem ec2-user@Public_IPv4_address`
`git clone https://github.com/tpmac1990/deploy-django-with-docker-compose.git`
`cd deploy-django-with-docker-compose`
`nano .env`
DB_NAME=app   
DB_USER=approotuser
DB_PASS=superpassword123
SECRET_KEY=secretkey12gh
ALLOWED_HOSTS=Public_IPv4_DNS,hostname2,hostname3

`docker-compose -f docker-compose-deploy.yml up -d`
`docker-compose -f docker-compose-deploy.yml run --rm app sh -c "python manage.py createsuperuser"`

### updating deployed app
commit changes to github
`git pull origin`
`docker-compose -f docker-compose-deploy.yml build app` app is the name of the service
`docker-compose -f docker-compose-deploy.yml up --no-deps -d app` replace app with new version but not affect any dependencies


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

## add proxy + run app through uWSGI + add docker-compose-deploy.yml for production
- add a proxy to help manage static files for efficiently in production. Get a better description from 'comments' branch
    - develoment: static files will be stored in data/web
- created docker-compose-deploy.yml to run image in production.

## cleaned up Dockerfile
- Combined all Run commands. This will reduce image size.

## added Sample model to test user saved media files are stored correctly
- added model in home app
- added wagtail_hooks module
- had to add "wagtail.contrib.modeladmin" to installed apps
- tested it by adding an image in the admin using both docker-compose
    and docker-compose-deploy.
    - docker-compose: saves images in the data/web/ directory
    - docker-compose-deploy: saves images elsewhere. All paths including `static` are intercepted so the 
        proxy can serve the static files instead (more efficient). Same for saving static files.


## adjusted heap size for elasticsearch
- added "ES_JAVA_OPTS=-Xms512m -Xmx512m" & "restart: always" to solve elastic search crashing


## htmx & tailwind todo in home app
- tut: https://www.youtube.com/watch?v=Pr8z9XxyrJc
- setup of both using CDN's




# todo:
- add react
- add tests (django)
- add tests (react)
- unable to switch between docker-compose and docker-compose-deploy without resetting the database.
- create react app and copy over
- make a change to a template
- create svelte SPA
- create react SPA
- create react component
- add htmx