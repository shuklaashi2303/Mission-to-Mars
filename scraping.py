from splinter import Browser
from bs4 import BeautifulSoup as soup
import time
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)

def scrape_info():
    browser = init_browser()
    

    # Visit visitcostarica.herokuapp.com
# Visit the mars nasa news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

# Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

# Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    slide_elem = news_soup.select_one('div.list_text')
    slide_elem.find('div', class_='content_title')
# Use the parent element to find the first a tag and save it as `news_title`
    news_title = slide_elem.find('div', class_='content_title').get_text()

# Use the parent element to find the paragraph text
    news_p = slide_elem.find('div', class_='article_teaser_body').get_text()


# Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

# Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

# Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')


# find the relative image url
    img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')


# Use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'



    df = pd.read_html('https://galaxyfacts-mars.com')[0]


    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)


    facts= df.to_html()

# 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'

    browser.visit(url)

    html = browser.html
    first_soup = soup(html, 'html.parser')
    first = first_soup.find('div', class_="collapsible results")
    items = first.find_all('div', class_="item")


# 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
    for item in items:  
        x = item.find("h3").text
        hemisphere_image_urls.append(x)



    hemi_data = []
    for hemi in hemisphere_image_urls:
        browser.visit(url)
        browser.is_element_present_by_text(hemi, wait_time=1)
        enhanced_image_elem = browser.links.find_by_partial_text(hemi)
        enhanced_image_elem.click()
        
        html = browser.html
        hemi_soup = soup(html, 'html.parser')
        
        hemi_title = hemi_soup.find("h2", class_="title").text
        
        hemi_url = hemi_soup.find("a", text="Sample").get("href")
        hemi_dict = {'title':hemi_title, 'img_url': f'{url}{hemi_url}'}
        # append to list of dictionaries
        hemi_data.append(hemi_dict)

    # Store data in a dictionary
    scraping = {
        "featured_image": img_url,
        "news_title": news_title,
        "news_paragraph": news_p,
        "facts": facts,
        "hemispheres": hemi_data,
    }

    # Quite the browser after scraping
    browser.quit()

    # Return results
    return scraping
