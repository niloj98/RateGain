#!/usr/bin/env python
# coding: utf-8

# In[41]:


#WEB SCRAPING USING REQUESTS AND BEAUTIFULSOUP


import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_soup(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()  
    return BeautifulSoup(response.text, 'html.parser')

def extract_titles(soup, data):
    titles = soup.select('div.content h6 a')
    for title in titles:
        title_text = title.get_text(strip=True)
        print(f"Title: {title_text}")
        data['Title'].append(title_text)

def extract_dates(soup, data):
    dates = soup.select('div.bd-item')
    for date in dates:
        icon_class = date.select_one('i')['class']
        span_text = date.select_one('span').get_text(strip=True)
        if 'material-design-icon-history-clock-button' in icon_class:
            print(f"Date: {span_text}")
            data['Date'].append(span_text)

def extract_image_urls(soup, data):
    img_a_tags = soup.select('div.img a.rocket-lazyload')
    for img_a in img_a_tags:
        img_href = img_a.get('href', 'No href found')
        print(f"Image Href: {img_href}")
        data['Image Url'].append(img_href)

def extract_likes_count(soup, data):
    likes_tags = soup.select('a.zilla-likes i.material-design-icon-favorite-heart-outline-button + span')
    for likes_tag in likes_tags:
        likes_count = likes_tag.get_text(strip=True)
        digit_part = ''.join(char for char in likes_count if char.isdigit())
        print(f"Likes Count: {digit_part}")
        data['Number of Likes'].append(int(digit_part))

def scrape_blog(base_url, num_pages):
    data = {'Title': [], 'Date': [], 'Image Url': [], 'Number of Likes': []}


    urls_to_scrape = [f"{base_url}page/{page_num}/" for page_num in range(1, num_pages + 1)]

    
    for url in urls_to_scrape:
        try:
            soup = get_soup(url)
            extract_titles(soup, data)
            extract_dates(soup, data)
            extract_image_urls(soup, data)
            extract_likes_count(soup, data)
            print("=" * 80)
        except requests.RequestException as e:
            print(f"Failed to retrieve content from {url}: {e}")

 
    df = pd.DataFrame(data)

 
    df.to_csv('scraped_data.csv', index=False)
    df.to_excel('scraped_dataexcel.xlsx', index=False)

if __name__ == "__main__":
    base_url = "https://rategain.com/blog/"
    num_pages_to_scrape = 3
    scrape_blog(base_url, num_pages_to_scrape)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[22]:


#WEB SCRAPING USING SELENIUM AND WEBDRIVER



import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

def scrape_blog(base_url, num_pages):
    path = r"C:\Program Files\chromedriver.exe"
    driver = webdriver.Chrome(path)

    data = {'Title': [], 'Date': [], 'Likes Count': []}

    try:
        urls_to_scrape = [f"{base_url}page/{page_num}/" for page_num in range(1, num_pages + 1)]

        for url in urls_to_scrape:
            driver.get(url)

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "content"))
            )

            # Extract titles
            titles = driver.find_elements(By.CSS_SELECTOR, 'div.content h6 a')
            for title in titles:
                title_text = title.text
                data['Title'].append(title_text)

            # Extract dates
            dates = driver.find_elements(By.CSS_SELECTOR, 'div.bd-item i.material-design-icon-history-clock-button + span')
            for date in dates:
                date_text = date.text
                data['Date'].append(date_text)

            # Extract likes count
            likes_elements = driver.find_elements(By.CSS_SELECTOR, 'a.zilla-likes i.material-design-icon-favorite-heart-outline-button + span')
            for likes_element in likes_elements:
                likes_count = likes_element.text
                digit_part = ''.join(char for char in likes_count if char.isdigit())
                data['Likes Count'].append(int(digit_part))

            print("=" * 80)

    finally:
        # Close the browser
        driver.quit()

    # Create a DataFrame
    df = pd.DataFrame(data)

    # Save the DataFrame to CSV
    df.to_csv('scraped_dataselenium.csv', index=False)
    df.to_excel('scraped_dataexcelselenium.xlsx', index=False)

if __name__ == "__main__":
    base_url = "https://rategain.com/blog/"
    num_pages_to_scrape = 3
    scrape_blog(base_url, num_pages_to_scrape)


# In[ ]:




