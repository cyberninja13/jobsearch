# scrape_indeed.py

import csv
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def initiate_driver():
    return webdriver.Chrome(ChromeDriverManager().install())

def scrape_indeed_jobs(query, location, num_pages):
    start_list = [page * 10 for page in range(num_pages)]
    base_url = 'https://in.indeed.com'

    job_data = []

    for start in start_list:
        url = base_url + f'/jobs?q={query}&l={location}&start={start}'

        # Use the initiate_driver function
        driver = initiate_driver()
        driver.get(url)
        time.sleep(1)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        items = soup.find_all('td', {'class': 'resultContent'})

        for job in items:
            s_link = job.find('a').get('href')
            job_title = job.find('span', title=True).text.strip()
            company = job.find('span', class_='companyName').text.strip()
            location = job.find('div', class_='companyLocation').text.strip()
            if job.find('div', class_='metadata salary-snippet-container'):
                salary = job.find('div', class_='metadata salary-snippet-container').text
            elif job.find('div', class_='metadata estimated-salary-container'):
                salary = job.find('div', class_='metadata estimated-salary-container').text
            else:
                salary = ""

            job_link = base_url + s_link

            job_data.append([job_title, company, location, job_link, salary])

        driver.quit()

    # Save the data to a CSV file
    filename = f'{query}_{location}_job_results.csv'
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Job Title', 'Company', 'Location', 'Job Link', 'Salary'])
        writer.writerows(job_data)

if __name__ == "__main__":
    # Example usage
    scrape_indeed_jobs("python", "remote", 2)
