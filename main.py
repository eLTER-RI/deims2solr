"""
Project: eLTER PLUS
File: main.py
Description: DEIMS.org site metadata harvester

Author: Vladan Minić
Institution: BioSense Institute
Date: 2024-07-01
Version: 1.0.0

Dependencies:
    - requests, psycopg2

Usage:
    - Python scripts runs on docker deploy
    - Crontab runs python script every night at 3

License:
    - EUPL - The European Union Public Licence
"""

import os
import requests
import time
import psycopg2
from psycopg2.extras import Json
from datetime import datetime


# Print debug info
DEBUG = False
# Remove geometry from JSON responses
REMOVE_GEOMETRY = True
# DEIMS network UUID
NETWORK = '4742ffca-65ac-4aae-815f-83738500a1fc'
# Database params
DB_HOST = os.environ['POSTGRES_HOST']
DB_NAME = os.environ['POSTGRES_DB']
DB_USER = os.environ['POSTGRES_USER']
DB_PASS = os.environ['POSTGRES_PASSWORD']


def fetch_and_store_site_data():
    """Fetch site data from the API and store it in PostgreSQL."""
    conn = psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS)
    cur = conn.cursor()

    # Call the initial API to get the list of sites
    url = f'https://deims.org/api/sites?network={NETWORK}&verified=true'
    response = requests.get(url)
    sites = response.json()

    for index, site in enumerate(sites):
        suffix = site['id']['suffix']
        if DEBUG:
            print(f"Index {index}: ID Suffix = {suffix}")

        site_detail_url = f"https://deims.org/api/sites/{suffix}"
        site_detail_response = requests.get(site_detail_url)
        site_detail = site_detail_response.json()

        # Remove the 'geographic' block
        if REMOVE_GEOMETRY and 'geographic' in site_detail['attributes']:
            del site_detail['attributes']['geographic']

        # Extract the changed timestamp from the new data
        new_changed = datetime.strptime(site_detail['changed'], '%Y-%m-%dT%H:%M:%S%z').replace(tzinfo=None)

        # Check if the site already exists in the database
        cur.execute("SELECT changed FROM site_data WHERE id = %s", (suffix,))
        result = cur.fetchone()

        if result:
            # Compare the existing and new 'changed' timestamps
            existing_changed = result[0]
            if new_changed > existing_changed:
                # Update the record if the new 'changed' is greater
                cur.execute("""
                UPDATE site_data
                SET data = %s, changed = %s
                WHERE id = %s
                """, (Json(site_detail), new_changed, suffix))
                conn.commit()
                if DEBUG:
                    print(f"UPDATED ID {suffix}")
        else:
            # Insert the new record if it doesn't exist
            cur.execute("""
            INSERT INTO site_data (id, data, changed)
            VALUES (%s, %s, %s)
            """, (suffix, Json(site_detail), new_changed))

            # Commit the transaction
            conn.commit()
            if DEBUG:
                print(f"INSERTED ID {suffix}")

    cur.close()
    conn.close()


def delete_obsolete():
    """Delete outdated DEIMS records from PostgreSQL."""
    # Call the initial API to get the list of sites
    url = f'https://deims.org/api/sites?network={NETWORK}&verified=true'
    response = requests.get(url)
    sites = response.json()

    # Extract all 'id' values
    deims_list = [item['id']['suffix'] for item in sites]

    conn = psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS)
    cur = conn.cursor()
    # Check if the site already exists in the database
    cur.execute("SELECT id FROM site_data")
    results = cur.fetchall()
    results = [row[0] for row in results]

    for id in results:
        if id not in deims_list:
            # Delete the record if it doesn't exist on DEIMS
            cur.execute(f"DELETE FROM site_data WHERE id = '{id}'")
            # Commit the transaction
            conn.commit()
            if DEBUG:
                print(f"Deleted ID {id}")
    cur.close()
    conn.close()


def main():
    """Main function to create table and fetch/store site data."""
    # Wait for 60 sec to be sure that postgres docker is up and running
    time.sleep(60)
    fetch_and_store_site_data()
    delete_obsolete()
    url = "http://solr:8983/solr/deims2solr/dataimport?command=full-import"
    response = requests.get(url)
    if DEBUG:
        if response.status_code == 200:
            print("Data import triggered successfully.")
        else:
            print(f"Failed to trigger data import. Status code: {response.status_code}")


if __name__ == "__main__":
    main()
