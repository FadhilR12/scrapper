import json
import re

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


# membuat fungsi untuk mengatur dan menginisialisasi driver Chrome
def setup_driver():
    CHROMEDRIVER_PATH = '/Users/fadhilr12/Downloads/chromedriver'

    # membuat opsi Chrome untuk konfigurasi browser
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    service = Service(CHROMEDRIVER_PATH)
    return webdriver.Chrome(service=service, options=chrome_options)


# membuat fungsi untuk mendapatkan semua link pekerjaan berdasarkan kata kunci
def get_job_links(keyword):
    driver = setup_driver()
    job_links = []

    try:
        search_url = f"https://www.linkedin.com/jobs/search/?geoId=102454443&keywords={keyword}&refresh=true"
        # mengarahkan browser ke URL pencarian
        driver.get(search_url)
        # menunggu selama 20 detik hingga elemen dengan selector 'ul.jobs-search__results-list' muncul di halaman
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'ul.jobs-search__results-list'))
        )

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        # membuat varabel untuk menampung semua elemen list pekerjaan dari halaman
        job_listings = soup.select('ul.jobs-search__results-list li')

        # menggunakan loop untuk melalui semua elemen list pekerjaan
        for job in job_listings:
            # menemukan elemen link penuh dalam pekerjaan
            link = job.select_one('a.base-card__full-link')
            # melakukan percabangan jika link ditemukan maka akan menambah link" ke variabel 'job_links'
            if link:
                job_links.append(link['href'])

        return job_links
    # menangkap dan mencetak kesalahan jika terjadi
    except Exception as e:
        print(f"Error: {e}")
        return None
    # menutup browser setelah selesai
    finally:
        driver.quit()


# membuat fungsi untuk mengambil rincian pekerjaan berdasarkan link pekerjaan
def get_job_details(job_link):
    driver = setup_driver()

    try:
        # mengarahkan browser ke halaman rincian pekerjaan
        driver.get(job_link)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'h1.top-card-layout__title'))
        )

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # mencari data data yang ingin diambil dari struktur html menggunakan soup.find
        title = soup.find('h1', class_='top-card-layout__title')
        company = soup.find('a', class_='topcard__org-name-link')
        location = soup.find('span', class_='topcard__flavor--bullet')
        description = soup.find('div', class_='show-more-less-html__markup')

        # membuat dictionary menggungakan data data yang sudah diambil
        job_details = {
            'Title': title.get_text(strip=True) if title else '-',
            'Company': company.get_text(strip=True) if company else '-',
            'Location': location.get_text(strip=True) if location else '-',
            'Description': description.get_text(strip=True) if description else '-',
            'Apply link': job_link
        }

        return job_details

    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        driver.quit()


# meminta pengguna untuk memasukkan kata kunci pencarian pekerjaan
keyword = input("Masukkan kata kunci pekerjaan: ")
# membuat variabel 'job_links' untuk menyimpan daftar link pekerjaan berdasarkan kata kunci yang dimasukkan
job_links = get_job_links(keyword)


def create_filename(title):
    return re.sub(r'[\\/*?:"<>|]', "", title)
    pass


if job_links:
    print(f"Jumlah pekerjaan ditemukan: {len(job_links)}")

    for link in job_links:
        job_details = get_job_details(link)
        if job_details:
            valid_filename = create_filename(job_details['Title'])
            with open(f'{valid_filename}.json', 'w') as f:
                json.dump(job_details, f, ensure_ascii=False, indent=4)
            print(f'Data pekerjaan {job_details["Title"]} berhasil disimpan ke {valid_filename}.json')
        else:
            print(f"Gagal mengambil data dari {link}")
else:
    print('Gagal mengambil data pekerjaan.')
