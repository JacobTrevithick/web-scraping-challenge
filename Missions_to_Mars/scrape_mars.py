from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager 
import pandas as pd


def scrape():
    
    # make sure google chrome up to date and open browser
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    website_dict = {}
    
    '''
    NEWS section
    '''
    news_url = 'https://redplanetscience.com/'
    browser.visit(news_url)
    
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    # Gathering latest Mars news
    news_title = soup.find('div', class_ = 'content_title').text
    news_p = soup.find('div', class_= 'article_teaser_body').text
    
    # append to dictionary
    website_dict['news_title'] = news_title
    website_dict['news_p'] = news_p
    
    
    '''
    MARS IMAGE section
    '''
    jpl_url = 'https://spaceimages-mars.com/'
    browser.visit(jpl_url)
    
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    # getting latest mars image
    mars_img_rel_path = soup.find('img', class_ = "headerimage fade-in")['src']
    mars_img_url = jpl_url + mars_img_rel_path
    
    # append to dictionary
    website_dict['mars_image'] = mars_img_url
    
    
    '''
    FACTS section
    '''
    facts_url = 'https://galaxyfacts-mars.com/'
    
    # read in tables from facts_url
    tables = pd.read_html(facts_url)
    
    # select comparison table
    mars_facts_df = tables[0]

    # reformat table
    mars_facts_df.columns = mars_facts_df.iloc[0]
    mars_facts_df = mars_facts_df.drop(0,axis=0)
    
    # export table to html code string
    table_string = mars_facts_df.to_html()
    
    website_dict['mars_facts'] = table_string
    
    
    
    '''
    HEMISPHERE IMAGES section
    '''
    hem_url = 'https://marshemispheres.com/'
    browser.visit(hem_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    results = soup.find_all("div", class_="item")

    hemisphere_imgs = []

    for result in results:
        img_dict = {}
        
        item = result.find('div', class_='description')
        header = item.find('h3').text
        
        x = result.find('a', class_='itemLink product-item')['href']
        
        browser.links.find_by_partial_text(header).click()
        
        html_2 = browser.html
        soup_2 = BeautifulSoup(html_2, 'html.parser')
        
        img_rel_path = soup_2.find('img', class_='wide-image')['src']
        
        img_abs_path = hem_url + img_rel_path
        
        browser.visit(hem_url)
        
        img_dict['title'] = header
        img_dict['url'] = img_abs_path
        hemisphere_imgs.append(img_dict)
    
    website_dict['hem_imgs'] = hemisphere_imgs

    browser.quit()

    return website_dict

    