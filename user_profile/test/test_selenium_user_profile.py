import pytest


from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


@pytest.mark.selenium
def test_open_admin_page_and_sign_in(live_server,firefox_browser_instance,create_super_user_profile):
    
    super_user = create_super_user_profile
    browser = firefox_browser_instance
    browser.get(f'{live_server.url}/admin/login')
    
    user_name = browser.find_element(By.NAME, "username")
    user_password = browser.find_element(By.NAME, "password")
    submit = browser.find_element(By.XPATH, '//input[@value="Log in"]')
    
    user_name.send_keys("infinity")
    user_password.send_keys("12345678")
    
    submit.click()
    
    assert "Site administration" in browser.page_source

    