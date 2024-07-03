<p align="center">
  <img src="assets/eLTER-IMAGE-eLTER_logo-v01.svg" alt="eLTER Project Logo" width="300" height="auto"/>
</p>

# Repository title

DEIMS2SOLR


![](https://img.shields.io/badge/license-EUPL--1.2-orange)
![](https://img.shields.io/badge/Postgres-latest-orange)
![](https://img.shields.io/badge/Python-v3.9-orange)
![](https://img.shields.io/badge/Solr-9.2.1-orange)

## Description

Stanadalone project that provides full text search of DEIMS.org sites using Apache Solr

## Table of Contents

Add a table of contents at the beginning of the `README.md` file.

-   [Installation and usage](#installation-and-usage)
-   [Dockers](#dockers)  
-   [Authors](#authors)
-   [License](#license)
-   [Acknowledgments](#acknowledgments)

## Installation and usage

#### Build and run the Docker images:
```sh
docker-compose up -d
```

#### Stop the Docker images:
```sh
docker-compose down
```

## Dockers
This is a list of used docker images and their setup
For detailed configuration, please see docker-compose.yml

### Postgres docker
Latest postgres docker image that uses init.sql to create table.
Data are stored in postgres volume

### Python docker

This docker image run Python script that fetch sites metadata from deims.org
Script run on docker deploy and every night at 3:00

- User may specify different eLTER network for meta-data harvesting.
- Debug info can be turned on/off in order to print harvesting results in colsole
- User may turn on/off saving geometry saving from meta-data

Harvested metadata are stored in postgres docker.
After harvesting is done, Solr is called to refresh the imported data.

Please see Dockerfile.python for more details

### Solr docker
Solr docker use deims2solr core that read the data from postgres docker.


Please see Dockerfile.solr

## Authors

|       Author       |               Affiliation                |                       e-mail                       |
|:------------------:|:----------------------------------------:|:--------------------------------------------------:|
| Milica Milovanović | [BioSense Institue](https://biosense.rs) | [milicam\@biosense.rs](mailto:milicam@biosense.rs) |
|    Mina Bjelica    | [BioSense Institue](https://biosense.rs) |   [minab\@biosense.rs](mailto:minab@biosense.rs)   |
|    Vladan Minić    | [BioSense Institue](https://biosense.rs) |   [minic\@biosense.rs](mailto:minic@biosense.rs)   |


## License

-   This project is licensed under the [EUPL
    License](https://eupl.eu/) - see the [LICENSE](LICENSE) file for
    details.

## Acknowledgments

<p align="center">
  <a href="https://elter-ri.eu/elter-ppp">
    <img src="assets/eLTER-IMAGE-PPP_logo-v01.svg" alt="eLTER PLUS Logo" width="175" height="auto"/>
  </a> <a href="https://elter-ri.eu/elter-plus">
    <img src="assets/eLTER-IMAGE-PLUS_logo-v01.svg" width="175" height="auto"/>
  </a> <a href="https://elter-ri.eu/elter-enrich">
    <img src="assets/eLTER-IMAGE-EnRich_logo-v01.svg" alt="eLTER EnRich Logo" width="175" height="auto"/>
  </a>
</p>