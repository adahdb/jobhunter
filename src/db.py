import sqlite3
import json

import services

CREATE_JOBS_TABLES = """
    CREATE TABLE IF NOT EXISTS job (
        id TEXT PRIMARY KEY,
        headline TEXT,
        brief TEXT,
        timePosted TEXT,
        occupation_group_label TEXT,
        occupation_group_concept_id TEXT,
        occupation_field_label TEXT,
        occupation_field_concept_id TEXT,
        employer TEXT,
        municipality TEXT,
        municipality_concept_id TEXT,
        region TEXT,
        region_concept_id TEXT,
        country TEXT,
        country_concept_id TEXT,
        urls TEXT
    )"""

def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}

def init():
    connection = sqlite3.connect("jobs.db")
    connection.row_factory = dict_factory
    connection.execute(CREATE_JOBS_TABLES)
    connection.commit()
    services.db = connection

def save_jobs(jobs):
    cursor = services.db.cursor()
    jobs_tuples = convert_to_tuples(jobs)
    cursor.executemany("INSERT OR IGNORE INTO job VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", jobs_tuples)
    services.db.commit()

    #result = cursor.execute("SELECT * FROM job")
    #result = result.fetchall()
    # print(result)

def convert_to_tuples(jobs):
    job_tuples = [
        (
            job["id"],
            job["headline"],
            job["brief"],
            job["timePosted"],
            job["occupation_group_label"],
            job["occupation_group_concept_id"],
            job["occupation_field_label"],
            job["occupation_field_concept_id"],
            job["employer"],
            job["municipality"],
            job["municipality_concept_id"],
            job["region"],
            job["region_concept_id"],
            job["country"],
            job["country_concept_id"],
            json.dumps(job["urls"])  # converts the list to a JSON string for storage
        )
        for job in jobs
    ]
    return job_tuples

def get_jobs_by_fields(occupation_field_concept_id, region, yesterday_date):
    cursor = services.db.cursor()
    cursor.execute(
        "SELECT * FROM job WHERE occupation_field_concept_id = ? AND region_concept_id = ? AND timePosted = ?",
        (occupation_field_concept_id,region,yesterday_date)
    )
    return cursor.fetchall()

def close():
    if services.db:
        services.db.close()