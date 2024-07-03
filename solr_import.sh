#!/bin/bash
# Trigger the data import
curl "http://localhost:8983/solr/deims2solr/dataimport?command=full-import"
