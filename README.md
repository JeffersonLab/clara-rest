
# Clara REST API

REST interface based on django python 1.9

Once in the main folder, run the following command in order to install the dependencies

```sh
$ pip install -r requirements.txt
```

System requirements:

- InfluxDB server, for the clara runtime database (it needs to have an empty DB called 'claraRuntime') 

### Running the App in development mode
Inside the application folder, you can do this by running in your terminal:

```sh
$ ./manage.py runserver
```


## Monitoring
In order to subscribe to the Clara DPE's runtime and registration data we need to start the DPE monitor, this process can run even with the web server not running.   

```sh
$ ./manage.py monitor
```

In order to access the django site, try the URLs, like in the following example. As you can see the URLs follow the hierarchy of the Clara Framework 

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

### Other commands for monitoring

If any change is introduced in the runtime database, please execute the following command in order to recreate the influxDB database. This command will DROP the current database and will CREATE a new instance.

```sh
./manage.py monitor --sync_influx_db
```

The clean_old_data command is meant to clean up the registration database from DPE that have not reported in the last ten minutes. This command is supposed to run as a cron Job, so it is regularly checking currently stored data.

```sh
./manage.py monitor --clean_old_data
```
