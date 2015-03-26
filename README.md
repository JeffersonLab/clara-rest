#Clara Web Application

User web interface based on django python 1.7

### Installation
```sh
$ git clone ssh://git@git.earthdata.nasa.gov:7999/naiads/clara-webapp.git
$ cd clara-webapp
$ # TODO requirements handling
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
http://localhost:8000/dpes
http://localhost:8000/dpes/{dpe_id}/
http://localhost:8000/dpes/{dpe_id}/containers
http://localhost:8000/dpes/{dpe_id}/containers/{container_id}
http://localhost:8000/dpes/{dpe_id}/containers/{container_id}/services/
http://localhost:8000/dpes/{dpe_id}/containers/{container_id}/services/{service_id}
http://localhost:8000/subscriptions/
http://localhost:8000/subscriptions/{subscription_id}
```

###Testing the application
Tests for each of the Django models can be found in each app package, if you want to run them, you can type the following in the main directory

```sh
$ python manage.py test
```

###TODO
  - Complete the documentation of this README file
  - Complete the django data models
