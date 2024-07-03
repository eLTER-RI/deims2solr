# DEIMS 2 SOLR
### Project eLTER PLUS
### Author: Vladan Minić
### Purpose:
Harvest DEIMS.org and store results in database so SOLR can make full text search.
### Setup Instructions:
In the directory containing your `script.py`, `run_cron.sh`, and `Dockerfile`, run the following commands:
#### Build the Docker images:
```sh
docker-compose up -d
```

#### Stop the Docker images:
```sh
docker-compose down
```