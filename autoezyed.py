from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException

# This may be obsolete because ezyed is inefficient xD
# basically html for non-shown tasks are still present in the DOM so u can
# just reference them straightway instead of expanding any divs
class TaskID:
    def __init__(self, task_code):
        self.task_code = task_code

        # Keep naming conventions for task ID sections consistent
        self.topic = self.task_code[:2]
        self.module = self.task_code[2]
        self.unit = self.task_code[4]
        self.work = self.task_code[5]

# TODO: Make settings be extracted from json settings file or external ui,
# not written into the console every time
class AutomaticEzyed:
    def __init__(self):
        self.driver = None
        self.phyiscs_xpath = "//a[@href='https://www.ezyeducation.co.uk/learning-zone/courses/139-edexcel-igcse-physics.html']"

        print("AutomaticEzyed initialised")

    def run(self):
        print("Start auto sequence")
        self.driver = wd.Chrome()
        self.driver.get("https://www.ezyeducation.co.uk/")

        # TODO: Remove later, only for debugging
        username = input("Email: ")
        password = input("Password: ")
        self._login(username, password)

        # TODO: Add different subjects later
        subject_to_use = "PHYSICS"
        if subject_to_use == "PHYSICS":
            self.select_physics_subject()

        # TODO: Make this not in the CLI
        task_input = input("Homework ID: ")
        # Why is the below line commented? See comment above TaskID class
        #task_id = TaskID(task_input)
        task_element = self.driver.find_element(By.XPATH, "//a[contains(@title, '" + task_input + "')]")
        task_link = task_element.get_attribute("href")
        self.go_into_task(task_link)

        input("AutomaticEzyed finished automation, press enter to continue")

        self.driver = None

    def _login(self, username: str, password: str):
        userBox = self.driver.find_element(By.NAME, "username")
        passBox = self.driver.find_element(By.NAME, "password")

        self.send_keys_to_element(userBox, username)
        self.send_keys_to_element(passBox, password)

        submitButton = self.driver.find_element(By.XPATH, "//button[@value='Log in']")
        submitButton.click()

    def send_keys_to_element(self, element, keys):
        ActionChains(self.driver)\
            .send_keys_to_element(element, keys)\
            .perform()

    def go_into_task(self, task_link):
        self.driver.get(task_link)
        # If the task has not been attempted, ever, Next button will show.
        # Otherwise, only the Restart button will show. We need to test for
        # which one this is.
        try:
            element = self.driver.find_element(By.XPATH, "//a[@value='Next']")
        except NoSuchElementException:
            element = self.driver.find_element(By.XPATH, "//a[@value='Restart']")
        element.click()

    def select_physics_subject(self):
        element = self.driver.find_element(By.XPATH, self.phyiscs_xpath)
        element.click()

def main():
    automation = AutomaticEzyed()
    automation.run()

if __name__ == "__main__":
    main()
