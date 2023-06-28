import pytest


from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

@pytest.mark.selenium
def test_open_index_page(live_server, firefox_browser_instance):

    browser = firefox_browser_instance
    browser.get(f'{live_server.url}')

    assert browser.title == 'Main'
    about_page = browser.find_element(By.ID,'About')
    about_page.click()
    
    assert browser.title == 'About'
    
    
    

@pytest.mark.selenium
def test_open_about_page(live_server,firefox_browser_instance):
    browser = firefox_browser_instance
    browser.get(f'{live_server.url}/about')
    
    assert browser.title == 'About'
    