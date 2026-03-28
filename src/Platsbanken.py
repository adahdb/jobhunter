import requests


base_url = "https://links.api.jobtechdev.se/joblinks"
params = {
    "limit": 100,
    "offset": 0,
    "published-after": "",
    "region": "CaRE_1nn_cSU",
    "occupation-field": "apaJ_2ja_LuF"
}

def callApi(yesterday_date):
    params["published-after"] = yesterday_date
    response = requests.get(base_url, params=params)
    return response


def getJobs(yesterday_date):
    all_jobs = []
    total = 0
    params["offset"] = 0

    while True:
        response = callApi(yesterday_date)
        if response.status_code == 200:
            url_data = response.json()

            if total == 0:
                total = url_data["total"]["value"]

            jobs = url_data["hits"]
            if not jobs:
                break

            all_jobs.extend(jobs)
            params["offset"] += 100
        else:
            print(f"Error: {response.status_code}")
            break

    return parseJobs(all_jobs, total)


def parseJobs(jobs, total):
    jobbList = []

    hits = total
    print(f"Hits: {hits}")

    for job in jobs:
        jobUrlList = []

        headline = job["headline"]
        if "cookies" in headline.lower():
            continue

            # Basic job info
        id = job["id"]
        brief = job["brief"]
        timePosted = job["publication_date"]

        # Occupation classification
        occupation_group_label = job["occupation_group"]["label"]
        occupation_group_concept_id = job["occupation_group"]["concept_id"]
        occupation_field_label = job["occupation_field"]["label"]
        occupation_field_concept_id = job["occupation_field"]["concept_id"]

        # Employer name
        employer = job["employer"].get("name") or "-"

        # workplace_addresses
        addresses = job["workplace_addresses"]
        if addresses:
            municipality = addresses[0]["municipality"]
            municipality_concept_id = addresses[0]["municipality_concept_id"]
            region = addresses[0]["region"]
            region_concept_id = addresses[0]["region_concept_id"]
            country = addresses[0]["country"]
            country_concept_id = addresses[0]["country_concept_id"]
        else:
            municipality = "Unknown"
            municipality_concept_id = None
            region = "Unknown"
            region_concept_id = None
            country = "Unknown"
            country_concept_id = None

        # Source links
        job_src = job["source_links"]
        for link in job_src:
            url = link["url"]
            jobUrlList.append(url)

            # debug
            #data(id, headline, timePosted, brief, occupation_group_label, occupation_group_concept_id, occupation_field_label, occupation_field_concept_id, employer, municipality, municipality_concept_id, region, region_concept_id, country, country_concept_id, jobUrlList, hits)

        jobDict = {
            "id": id,
            "headline": headline,
            "brief": brief,
            "timePosted": timePosted,
            "occupation_group_label": occupation_group_label,
            "occupation_group_concept_id": occupation_group_concept_id,
            "occupation_field_label": occupation_field_label,
            "occupation_field_concept_id": occupation_field_concept_id,
            "employer": employer,
            "municipality": municipality,
            "municipality_concept_id": municipality_concept_id,
            "region": region,
            "region_concept_id": region_concept_id,
            "country": country,
            "country_concept_id": country_concept_id,
            "urls": jobUrlList
        }
        jobbList.append(jobDict)

    print(f"Jobs: {len(jobbList)}")
    return jobbList


def data(id, headline, timePosted, brief, occupation_group_label, occupation_group_concept_id,
         occupation_field_label, occupation_field_concept_id, employer, municipality,
         municipality_concept_id, region, region_concept_id, country, country_concept_id, jobUrlList, hits):
    print(f"Hits:                  {hits}")
    print(f"ID:                    {id}")
    print(f"Headline:              {headline}")
    print(f"Time Posted:           {timePosted}")
    print(f"Brief:                 {brief[:80]}...")
    print(f"Occupation Group:      {occupation_group_label} ({occupation_group_concept_id})")
    print(f"Occupation Field:      {occupation_field_label} ({occupation_field_concept_id})")
    print(f"Employer:              {employer}")
    print(f"Municipality:          {municipality} ({municipality_concept_id})")
    print(f"Region:                {region} ({region_concept_id})")
    print(f"Country:               {country} ({country_concept_id})")
    print(f"Source URLs:           {jobUrlList}")
    print("-------------------------------------------------------")

