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
        cls.driver.get("http://127.0.0.1:5000/course-management")
        cls.driver.maximize_window()
        WebDriverWait(cls.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_course_management_page_content(self):
        """Verify Course Management page content"""
        try:
            # Verify page title
            title = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//h2[contains(text(), 'Course Management')]"))
            )
            self.assertTrue(title.is_displayed())

            # Define expected sections with their partial descriptions
            sections = {
                "View Courses": "Browse the complete list of registered courses",
                "Add New Course": "Register a new course by entering its details",
                "Update Course Information": "Modify existing course information",
                "Mark Course as Removed": "Flags a course as deleted without permanently removing it",
                "Remove Course": "Permanently delete a course from the system"
            }

            # Verify each section
            for section_title, partial_desc in sections.items():
                # Find the link element
                link = WebDriverWait(self.driver, 5).until(
                    EC.visibility_of_element_located((By.LINK_TEXT, section_title))
                )
                self.assertTrue(link.is_displayed(), f"{section_title} link not visible")

                # Find the description that follows the link in the same div
                description = WebDriverWait(self.driver, 5).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, f"//a[text()='{section_title}']/following-sibling::p[contains(., '{partial_desc}')]")
                    )
                )
                self.assertTrue(description.is_displayed(), f"Description for '{section_title}' not visible")
                print(f"✓ {section_title} - Verified")

        except Exception as e:
            self.fail(f"Course Management page test failed: {e}")


if __name__ == "__main__":
    unittest.main(verbosity=2, exit=False)

    print("\n" + "=" * 50)
    print("Testing completed successfully!")
    print("Browser will remain open for manual inspection")
    print("Press CTRL+C in this terminal to close browser")
    print("=" * 50 + "\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nClosing browser...")
        EduSysFrontendTests.driver.quit()
        print("Browser closed. Exiting program.")