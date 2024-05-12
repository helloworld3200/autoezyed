from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException

from dataclasses import dataclass
from time import sleep

# Strucure of answers:
# List of Answer objects. for example: answers[1] references answer to q2.
# For each instance in the list: there can be radios, checkboxes, nums, etc.
# Access these using Answer.nums, Answer.radios, etc. These are all lists.
@dataclass
class Answer:
    text: list = []

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
    def __init__(self, implicit_wait_time = 2):
        self.driver = None

        self.phyiscs_xpath = "//a[@href='https://www.ezyeducation.co.uk/learning-zone/courses/139-edexcel-igcse-physics.html']"

        self.total_questions = 0
        self.answers = []

        self.implicit_wait_time = implicit_wait_time

        print("AutomaticEzyed initialised")

    def run(self):
        print("Start auto sequence")
        self.driver = wd.Chrome()
        self.driver.get("https://www.ezyeducation.co.uk/")
        self.driver.implicitly_wait(self.implicit_wait_time)

        # TODO: Remove later, only for debugging
        username = input("Email: ")
        password = input("Password: ")
        self._login(username, password)

        # TODO: Add different subjects later
        subject_to_use = "PHYSICS"
        if subject_to_use == "PHYSICS":
            self._select_physics_subject()

        # TODO: Make this not in the CLI
        task_input = input("Homework ID: ")
        # Why is the below line commented? See comment above TaskID class
        #task_id = TaskID(task_input)
        task_element = self.driver.find_element(By.XPATH, "//a[contains(@title, '" + task_input + "')]")
        task_link = task_element.get_attribute("href")
        self._go_into_task(task_link)

        self._set_total_questions()
        self._set_correct_answers()

        self._go_into_task(task_link)



        input("AutomaticEzyed finished automation, press enter to continue")

        self.driver = None

    def _set_correct_answers(self):
        for question in range(self.total_questions):
            # TODO: Add logic for questions that arent numbers
            self._submit_question()
            answer_div = self._get_correct_answer_div()

            answer_text = self._get_answer_text(answer_div)

            answer = Answer(answer_text)
            self.answers.append(answer)

            if question != self.total_questions - 1:
                self._submit_task()
            else:
                self._goto_next_question()

    # TODO: do these functions
    def _submit_task(self):
        pass

    def _goto_next_question(self):
        pass

    def _get_correct_answer_div(self):
        topDiv = self.driver.find_element(By.ID, "jlms-math-image-wrapper-correct")
        firstChildElement = topDiv.find_element(By.XPATH, "./*[1]")
        return firstChildElement

    def _get_answer_text(self, answer_div):
        answer_div.find_elements(By.XPATH, ".//child[@type='text']")
        answer_text = []
        for answer in answer_div:
            answer_text.append(answer.get_attribute("innerHTML"))
        answer_text = [answer[1:] for answer in answer_text]

        return answer_text

    def _submit_question(self):
        self.driver.execute_script("jq_QuizNextOn();")

    def _set_total_questions(self):
        js_total_questions = self.driver.execute_script("return cur_quest_num;")
        self.total_questions = int(js_total_questions)

    def _login(self, username: str, password: str):
        userBox = self.driver.find_element(By.NAME, "username")
        passBox = self.driver.find_element(By.NAME, "password")

        self._send_keys_to_element(userBox, username)
        self._send_keys_to_element(passBox, password)

        submitButton = self.driver.find_element(By.XPATH, "//button[@value='Log in']")
        submitButton.click()

    def _send_keys_to_element(self, element, keys):
        ActionChains(self.driver)\
            .send_keys_to_element(element, keys)\
            .perform()

    def _go_into_task(self, task_link):
        self.driver.get(task_link)
        # If the task has not been attempted, ever, Next button will show.
        # Otherwise, only the Restart button will show. We need to test for
        # which one this is.
        try:
            element = self.driver.find_element(By.XPATH, "//a[@value='Next']")
            element.click()
        except NoSuchElementException:
            element = self.driver.find_element(By.XPATH, "//a[@value='Restart']")
            element.click()
            self._go_into_task(task_link)

    def _select_physics_subject(self):
        element = self.driver.find_element(By.XPATH, self.phyiscs_xpath)
        element.click()

def main():
    automation = AutomaticEzyed()
    automation.run()

if __name__ == "__main__":
    main()
