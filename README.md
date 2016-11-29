
# Clara REST API [![Build Status](https://travis-ci.org/JeffersonLab/clara-rest.svg?branch=dev)](https://travis-ci.org/JeffersonLab/clara-rest)

REST interface based on django python 1.9

## API Endpoints

```sh
# HTTP Method	URL
GET /dpes
GET /dpes/{dpe_id}/
DELETE /dpes/{dpe_id}/

GET /dpes/{dpe_id}/containers
DELETE /dpes/{dpe_id}/containers
GET	/dpes/{dpe_id}/containers/{container_id}
DELETE /dpes/{dpe_id}/containers/{container_id}

GET /dpes/{dpe_id}/containers/{container_id}/services/
GET /dpes/{dpe_id}/containers/{container_id}/services/{service_id}

GET	/containers/
GET	/containers/{container_id}
DELETE /containers/{container_id}

GET	/services/
# You Check documentation and test the API directly at:
http://<clara-host>/docs
```


Once in the main folder, run the following command in order to install the dependencies

```sh
$ pip install -r requirements.txt
```

System requirements:

- InfluxDB server, for the clara runtime database (it needs to have an empty DB called 'claraRuntime')
- Clara for python (>=2.0.6) [here](https://github.com/JeffersonLab/clara-python/)

## Running the App in development mode
Inside the application folder, you can do this by running in your terminal:

```sh
$ pip install -r claraweb/requirements/dev.txt
$ ./local_development
```

## Running the App in production

### System Requirements

```sh
pip
nginx
uwsgi (via pip)
virtualenv (isolated environment for python interpreter)
supervisor
```

### Procedure for deployment

__virtualenv__
* Create a virtualenv in the machine
* activate the created virtualenv
* install the requirements like this ```pip -r claraweb/requirements/production.txt```


__Nginx__

Configure nginx with the given scripts:

```sh
$ echo "daemon off;" >> /etc/nginx/nginx.conf
$ cp claraweb/nginx-app.conf /etc/nginx/sites-available/default
$ cp claraweb/supervisor-app.conf
```
once everything is in its place simply run supervisor to start the server

```sh
$ supervisor -n
```

Note that some of this scripts will need to be modified with the absolute path to the code

## Monitoring
In order to subscribe to the Clara DPE's runtime and registration data we need to start the DPE monitor, this process can run even with the web server not running.

```sh
$ ./manage.py monitor
```

In order to access the django site, try the URLs, like in the following example. As you can see the URLs follow the hierarchy of the Clara Framework

### Other commands for monitoring

If any change is introduced in the runtime database, please execute the following command in order to recreate the influxDB database. This command will DROP the current database and will CREATE a new instance.

```sh
./manage.py monitor --sync-influx-db
```
The clean_old_data command is meant to clean up the registration database from DPE that have not reported in the last ten minutes. This command is supposed to run as a cron Job, so it is regularly checking currently stored data.

```sh
./manage.py monitor --clean-old-data
```

Or do ***--help*** for more commands and help

```sh
./manage.py monitor --help
```
