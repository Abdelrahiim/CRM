from selenium import webdriver
import pytest


@pytest.fixture(scope='session')
def firefox_browser_instance(request):
    browser = webdriver.Firefox()
    # browser.set_page_load_timeout(3)
    yield browser
    
    browser.close()
