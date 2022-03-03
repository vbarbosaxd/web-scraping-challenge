# import dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

# create scrape function
def scrape():
    # browser = init_browser()
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # use browser to open the url 
    url = "https://redplanetscience.com/"

    browser.visit(url)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # get the latest news
    data = soup.find("div", class_="list_text")

    news_title = data.find("div", class_="content_title").text
    news_p = data.find("div", class_="article_teaser_body").text
    

    # for Mars latest image visit the url and get the full image url
    img_url = 'https://spaceimages-mars.com'

    # use browser to open the url for image
    browser.visit(img_url) 

    # create html to parse
    html = browser.html

    # create soup object to parse html
    soup = bs(html, "html.parser")

    # use beautifulsoup to navigate to the image
    image = []
    for img in soup.findAll('a'):
        image.append(img.get('href'))

    # create the url for the image
    featured_image_url = (img_url + image[2])
    
    # Mars facts
    # get the url for Mars's facts 
    facts_url = "https://galaxyfacts-mars.com/"

    # Use panda's `read_html` to parse the url
    table = pd.read_html(facts_url)

    # convert table to pandas dataframe
    facts_df = table[1]

    #rename the columns
    facts_df.columns=["Description", "Value"]

    # convert dataframe to an html table string
    facts_html = facts_df.to_html()

    # Mars hemisphere
    # get the url and open it with browser
    hemi_url = "https://marshemispheres.com/"
    browser.visit(hemi_url)
    # cerate html 
    html = browser.html

    # use beautiful soup to create soup object
    soup = bs(html, "html.parser")

    data = soup.find_all("div", class_="item")
    
    # creata a list to hold data for hemispheres
    hemisphere_img_urls = []

    # loop the data list to find titles and img urls for hemispheres
    for d in data:
    
        title = d.find("h3").text

        img_url = d.a["href"]
    
        url = (hemi_url + img_url)
    
        # use requests to get full images url 
        response = requests.get(url)
    
        # create soup object
        soup = bs(response.text,"html.parser")
    
        # find full image url
        new_url = soup.find("img", class_="wide-image")["src"]
    
        # create full image url
        full_url = (hemi_url + new_url)
        
        #make a dict and append to the list
        hemisphere_img_urls.append({"title": title, "img_url": full_url})
        
    
    # create mars data dictionary to hold data
    mars_data = {
        "news_title": news_title,
        "news_p" : news_p,
        "featured_image_url": featured_image_url,
        "html_table": facts_html,
        "hemisphere_img_urls": hemisphere_img_urls}

    # Quit the browser
    browser.quit()
    
    # return results
    return mars_data