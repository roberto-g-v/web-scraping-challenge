
# ------------------------------
#Step 2 - MongoDB and Flask Application
# ------------------------------

#Import dependencies
import os
import re
import time
import requests
import pandas as pd
import datetime as dt
from splinter import Browser
from bs4 import BeautifulSoup


#Converting Jupyter notebook into a Python script called scrape

def init_browser():
    # Capture path to Chrome Driver & Initialize browser
    executable_path = {'executable_path':"chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()

# Create a dictionary for all of the scraped data
mars_data = {}

#------------------------------
# Mars News
# ------------------------------

def mars_news(browser):
    url = "https://mars.nasa.gov/news/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    news_title = soup.find_all('div', class_='content_title')
    news_p = soup.find_all('div', class_='rollover_description_inner')


# # Add the news date, title and summary to the dictionary
    title = news_title[0].text.replace('\n', '')
    paragraph = news_p[0].text.replace('\n', '')

# Close the browser after scraping
# browser.quit()

    return title, paragraph


# ------------------------------
# JPL Mars Space Images
# ------------------------------

def space_image(browser):

    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    full_image_button = browser.find_by_id("full_image")
    full_image_button.click()

    browser.is_element_present_by_text("more info", wait_time=1)
    more_info_element = browser.find_link_by_partial_text("more info")
    more_info_element.click()

    html = browser.html
    image_soup = BeautifulSoup(html, "html.parser")

    img_url = image_soup.select_one("figure.lede a img").get("src")
    img_url = f'https://www.jpl.nasa.gov{img_url}'

# Close the browser after scraping
# browser.quit()

    return img_url


# ------------------------------
# Mars Weather
# ------------------------------

def mars_weather(browser):

# Mars weather's latest tweet from the website
    url_weather = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_weather)
    html_weather = browser.html
    soup = BeautifulSoup(html_weather, "html.parser")
    # Find a Tweet with the data-name `Mars Weather`
    mars_weather = soup.find("div", attrs={"class": "tweet", "data-name": "Mars Weather"})
    try:
        mars_weather = mars_weather.find("p", "tweet-text").get_text()
        mars_weather
    except AttributeError:
        pattern = re.compile(r'sol')
        mars_weather = soup.find('span', text=pattern).text

# Close the browser after scraping
# browser.quit()

    return mars_weather


# ------------------------------
# Mars Facts
# ------------------------------

# Visit the Mars Facts Site Using Pandas to Read
def df_mars_facts():

    df_mars_facts = pd.read_html("https://space-facts.com/mars/")[0]
    df_mars_facts.columns=["Description", "Value"]
    df_mars_facts.set_index("Description", inplace=True)

# Close the browser after scraping
# browser.quit()

    return df_mars_facts.to_html(classes="table table-striped")


# ------------------------------
# Mars Hemispheres
# ------------------------------

def hemisphere_image(browser):

# Visit web page
    browser = Browser('chrome', headless=False)
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    hemisphere_image_urls = []

    links = browser.find_by_css("a.product-item h3")
    for item in range(len(links)):
        hemisphere = {}
        browser.find_by_css("a.product-item h3")[item].click()
        sample_element = browser.find_link_by_text("Sample").first
        hemisphere["img_url"] = sample_element["href"]

        hemisphere["title"] = browser.find_by_css("h2.title").text
        hemisphere_image_urls.append(hemisphere)
        browser.back()

    # browser.quit()

    return hemisphere_image

def get_everything():
    browser = Browser('chrome', headless=False)

    news_title, news_p = mars_news(browser)
    img_url = space_image(browser)
    mars_twitter_weather = mars_weather(browser)
    facts = df_mars_facts()
    hemisphere_urls = hemisphere_image(browser)
    timestamp = dt.datetime.now()

    data_dict = {
        "news_title": news_title,
        "news_paragraph": news_p,
        "featured_image": img_url,
        "weather": mars_twitter_weather,
        "facts": facts,
        "hemispheres": hemisphere_urls,
        "last_modified": timestamp
    }

    browser.quit()
    return data_dict

if __name__ == "__main__":
    print(get_everything())
