import json
import re
import requests
from bs4 import BeautifulSoup

keyword = input("Masukkan keyword: ")
url = f"https://www.linkedin.com/jobs/search/?geoId=102454443&keywords={keyword}&refresh=true"

try:
    response = requests.get(url)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f"Error fetching URL: {e}")
    exit()

soup = BeautifulSoup(response.content, 'html.parser')
jobs = soup.find_all('div', class_='base-search-card')
job_list = []

for job in jobs:
    title = job.find('h3', class_='base-search-card__title').get_text(strip=True) if job.find('h3', class_='base-search-card__title') else "-"
    company = job.find('h4', class_='base-search-card__subtitle').get_text(strip=True) if job.find('h4', class_='base-search-card__subtitle') else "-"
    location = job.find('span', class_='job-search-card__location').get_text(strip=True) if job.find('span', class_='job-search-card__location') else "-"
    job_url = job.find('a', class_='base-card__full-link').get('href') if job.find('a', class_='base-card__full-link') else "-"

    if job_url and not job_url.startswith('http'):
        job_url = f'https://www.linkedin.com{job_url}'

    description = "-"
    if job_url != "-":
        description = "-"
        try:
            job_response = requests.get(job_url)
            job_response.raise_for_status()
            job_soup = BeautifulSoup(job_response.content, 'html.parser')
            description_elem = soup.find('div', class_='description__text')
            if description_elem:
                description = description_elem.get_text(strip=True)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching job detail URL: {e}")

    job_data = {
        'Title': title,
        'Company': company,
        'Location': location,
        'Description': description,
        'Apply Link': job_url
    }
    job_list.append(job_data)

    valid_filename = re.sub(r'[^a-zA-Z0-9_\-]', '_', title)

    try:
        with open(f'{valid_filename}.json', 'w') as file:
            json.dump(job_data, file, ensure_ascii=False, indent=4)
        print(f'Data pekerjaan {title} berhasil disimpan ke {valid_filename}.json')
    except IOError as e:
        print(f"Error writing to file: {e}")
