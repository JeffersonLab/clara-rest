#Clara Web Application

User web interface based on django python 1.7

### Installation
```sh
$ git clone ssh://git@git.earthdata.nasa.gov:7999/naiads/clara-webapp.git
$ cd clara-webapp
```

Once in the main folder, run the following command in order to install the dependencies

```sh
$ pip install -r requirements.txt
```

### Running the App in development mode
Inside the application folder, you will first need to build the development database. You can do this by running in your terminal:

```sh
$ python manage.py syncdb
```
Once this is done, you can start the develpment server by doing:

```sh
$ python manage.py runserver
```

In order to access the django site, try the URLs, like in the following example. As you can see the URLs follow the hierarchy of the Clara Framework 

```sh
# HTTP Method	URL
GET http://localhost:8000/dpes
POST    http://localhost:8000/dpes
GET http://localhost:8000/dpes/{dpe_id}/
DELETE  http://localhost:8000/dpes/{dpe_id}/
GET http://localhost:8000/dpes/{dpe_id}/containers
POST 	http://localhost:8000/dpes/{dpe_id}/containers
DELETE  http://localhost:8000/dpes/{dpe_id}/containers
GET	http://localhost:8000/dpes/{dpe_id}/containers/{container_id}
DELETE  http://localhost:8000/dpes/{dpe_id}/containers/{container_id}
GET	http://localhost:8000/dpes/{dpe_id}/containers/{container_id}/services/
POST	http://localhost:8000/dpes/{dpe_id}/containers/{container_id}/services/
GET http://localhost:8000/dpes/{dpe_id}/containers/{container_id}/services/{service_id}
GET	http://localhost:8000/containers/
POST    http://localhost:8000/containers/
GET	http://localhost:8000/containers/{container_id}
DELETE	http://localhost:8000/containers/{container_id}
GET	http://localhost:8000/services/
POST	http://localhost:8000/services/
GET	http://localhost:8000/subscriptions/
POST	http://localhost:8000/subscriptions/
GET	http://localhost:8000/subscriptions/{subscription_id}
DELETE	http://localhost:8000/subscriptions/{subscription_id}
# You Check documentation and test the API directly at:
http://localhost:8000/docs
```
More details about the URLs in: docs/API-current_urls_methods.png

###Testing the application
Tests for each of the Django models can be found in each app package, if you want to run them, you can type the following in the main directory

```sh
$ python manage.py test
```
####Test Coverage Report
To get a report about the test coverage

```sh
$ coverage run --source='.' --omit=./ClaraWebREST/wsgi.py manage.py test
$ coverage report 
```

###TODO
  - Complete the documentation of this README file
  - Connecting with Clara
