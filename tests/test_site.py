import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

BASE_URL = os.environ.get("BASE_URL", "http://localhost")

@pytest.fixture(scope="module")
def driver():
    opts = Options()
    opts.binary_location = "/usr/bin/chromium"
    for a in ["--headless=new", "--no-sandbox", "--disable-dev-shm-usage", "--window-size=1280,800"]:
        opts.add_argument(a)
    d = webdriver.Chrome(service=Service("/usr/bin/chromedriver"), options=opts)
    d.get(BASE_URL)
    yield d
    d.quit()

def test_title(driver):
    assert driver.title == "Lab 11 Site"

def test_heading(driver):
    heading = driver.find_element(By.ID, "heading").text
    assert "Welcome" in heading
    assert "built by" in heading

def test_version_label(driver):
    assert driver.find_element(By.ID, "version").text.startswith("Version")

def test_button_click_and_screenshot(driver):
    driver.find_element(By.ID, "btn").click()
    assert driver.find_element(By.ID, "message").text == "Button clicked"
    driver.save_screenshot("screenshot.png")
