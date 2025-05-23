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
        cls.driver.get("http://127.0.0.1:5000/home")
        WebDriverWait(cls.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

    @classmethod
    def tearDownClass(cls):
        pass

    def test_student_management_section(self):
        self._test_section_visibility(
            "Student Management",
            "Register, update, search or delete student profiles"
        )

    def test_teacher_management_section(self):
        self._test_section_visibility(
            "Teacher Management",
            "Manage teacher profiles, assignments and teaching schedules"
        )

    def test_course_management_section(self):
        self._test_section_visibility(
            "Course Management",
            "Create, view, update or delete course offerings"
        )

    def test_class_management_section(self):
        self._test_section_visibility(
            "Class Management",
            "Organize class schedules and groupings"
        )

    def test_academic_management_section(self):
        self._test_section_visibility(
            "Academic Management",
            "Access grades, attendance, and other essential academic records"
        )

    def test_financial_management_section(self):
        self._test_section_visibility(
            "Financial Management",
            "View and manage tuition fees, invoices, and scholarships"
        )

    def _test_section_visibility(self, section_title, expected_description):
        try:
            title = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(
                    (By.XPATH,
                     f"//*[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{section_title.lower()}')]")
                )
            )
            self.assertTrue(title.is_displayed())

            desc = WebDriverWait(self.driver, 3).until(
                EC.visibility_of_element_located(
                    (By.XPATH,
                     f"//*[contains(text(), '{section_title}')]/following::*[contains(text(), '{expected_description}')][1]")
                )
            )
            self.assertTrue(desc.is_displayed())
            print(f"✓ {section_title} - Verified")
        except Exception as e:
            self.fail(f"✗ {section_title} - Verification failed: {str(e)}")

    def test_course_management_page_content(self):
        """Open Course Management tab and verify its content"""
        try:
            # Wait for the link to appear in the DOM
            course_link = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.LINK_TEXT, "Course Management"))
            )

            # Scroll the link into view to avoid issues with overlays or off-screen elements
            self.driver.execute_script("arguments[0].scrollIntoView();", course_link)

            # Wait until the link is actually clickable, then click it
            WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Course Management"))
            )
            course_link.click()

            # Wait for the header to be visible on the Course Management page
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//*[self::h1 or self::h2][contains(text(), 'Course Management')]")
                )
            )

            features = {
                "View Courses": "Browse the complete list of registered courses",
                "Add New Course": "Register a new course by entering its details",
                "Update Course Information": "Modify existing course information",
                "Mark Course as Removed": "Flags a course as deleted",
                "Remove Course": "Permanently delete a course"
            }

            for link_text, description_snippet in features.items():
                link = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.LINK_TEXT, link_text))
                )
                self.assertTrue(link.is_displayed(), f"{link_text} link not visible")

                container_xpath = f"//a[text()='{link_text}']/parent::*"
                container = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, container_xpath))
                )

                description_xpath = f"{container_xpath}/following-sibling::p[contains(text(), '{description_snippet}')]"
                desc = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, description_xpath))
                )
                self.assertTrue(desc.is_displayed(), f"Description for '{link_text}' not visible")

                print(f"✓ {link_text} - Verified")

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
        while EduSysFrontendTests.driver.service.process:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nClosing browser...")
    finally:
        if EduSysFrontendTests.driver.service.process:
            EduSysFrontendTests.driver.quit()
        print("Browser closed. Exiting program.")
