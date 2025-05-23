from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
import time


class EduSysFrontendTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        cls.driver.get("http://127.0.0.1:5000/course-management/create-course-profile")
        cls.driver.maximize_window()
        WebDriverWait(cls.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()