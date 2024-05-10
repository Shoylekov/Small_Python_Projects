from bs4 import BeautifulSoup
import requests
import time

print("Put an unfamiliar skill")
unfamiliar_skill = input("> ")
print(f"Filtering out {unfamiliar_skill}")

def find_jobs():
    html_text = requests.get('https://dev.bg/company/jobs/python/').text
    soup = BeautifulSoup(html_text, 'lxml')
    jobs = soup.find_all('div', class_='job-list-item is-premium')
    for index, job in enumerate(jobs):
        date = job.find('span', class_='date date-with-icon').text.strip()
        company_name = job.find('span', class_='company-name hide-for-small').text.strip()
        skills_divs = job.find_all('div', class_='component-square-badge tech-stack-item has-image')
        skills = set()  # Using a set to store unique skills
        position = job.find('h6', class_='job-title ab-title-placeholder ab-cb-title-placeholder').text.strip()
        more_info = job.find('a', class_='overlay-link ab-trigger')['href']
        
        # Extracting city
        city_elem = job.find('span', class_='badge')
        city = city_elem.text.strip().split('\n')[0] if city_elem else "City not available"
        
        for div in skills_divs:
            skills.add(div.img['title'])
        if unfamiliar_skill not in skills:
            with open(f'posts/{index}_{int(time.time())}.txt', 'w', encoding='utf-8') as f:
                f.write(f"Company: {company_name}\n")
                f.write(f"City: {city}\n")
                f.write(f"Date of publishing: {date}\n")
                f.write(f"Position: {position}\n")
                f.write(f"Skills: {', '.join(skills)}\n")
                f.write(f"More info: {more_info}\n")
                f.write("\n")  # Separate each job listing with a newline
            print(f"File saved: {index} ")
if __name__ == '__main__':
    while True:
        find_jobs()
        wait_time = 10
        print(f"Waiting {wait_time} minutes...")
        time.sleep(wait_time*60)
