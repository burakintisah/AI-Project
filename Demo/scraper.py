from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import copy

class scraper:
    def is_integer(self, n):
        try:
            float(n)
        except ValueError:
            return False
        else:
            return float(n).is_integer()


    def get_data(self):
        # example option: add 'incognito' command line arg to options
        option = webdriver.ChromeOptions()

        option.add_argument("--incognito")

        # create new instance of chrome in incognito mode
        browser = webdriver.Chrome(executable_path='chromedriver.exe', options=option)

        # go to website of interest
        browser.get("https://www.nytimes.com/crosswords/game/mini")

        # waiting at most 10 seconds to load the page and waiting for the okay button to pop up
        # otherwise closing the page
        timeout = 10
        try:
            WebDriverWait(browser, timeout).until(
                EC.visibility_of_element_located((By.XPATH,
                                                  """//*[@id="root"]/div/div/div[4]/div/main/div[2]/div/div[2]/div[3]/div/article/div[2]/button/div/span""")))
        except TimeoutException:
            print("Timed out waiting for page to load")
            browser.quit()

        # clicking the first "OKAY" button at the beginning
        browser.find_element_by_xpath(
            """//*[@id="root"]/div/div/div[4]/div/main/div[2]/div/div[2]/div[3]/div/article/div[2]/button/div/span""").click()
        time.sleep(0.3)
        # revealing the solution of the puzzle first
        # first click reveal button
        browser.find_element_by_xpath(
            """//*[@id="root"]/div/div/div[4]/div/main/div[2]/div/div/ul/div[2]/li[2]/button""").click()
        time.sleep(0.3)
        # clicking the puzzle button
        browser.find_element_by_xpath(
            """//*[@id="root"]/div/div/div[4]/div/main/div[2]/div/div/ul/div[2]/li[2]/ul/li[3]/a""").click()
        time.sleep(0.3)
        # clicking the reveal button popped up
        browser.find_element_by_xpath(
            """//*[@id="root"]/div/div[2]/div[2]/article/div[2]/button[2]/div""").click()
        time.sleep(1)
        # closing the pop-up with the X button
        browser.find_element_by_xpath(
            """//*[@id="root"]/div/div[2]/div[2]/span""").click()

        '''
        At this point we have the New York Times Puzzle fully revealed and ready to extract data from it.
        1 - We will get the across clues 
        2 - We will get the down clues
            i = clue number 
            i + 1 = clue
        '''

        clues = browser.find_elements_by_class_name("ClueList-wrapper--3m-kd")

        across_str = clues[0].text
        down_str = clues[1].text

        across = across_str.split("\n")
        down = down_str.split("\n")

        across_clues = []
        down_clues = []

        for i in range(1, len(across), 2):
            word = ""
            word = across[i] + "  " + across[i + 1]
            across_clues.append(copy.deepcopy(word))

        for i in range(1, len(down), 2):
            word = ""
            word = down[i] + "  " + down[i + 1]
            down_clues.append(copy.deepcopy(word))

        # scrape cells with answers from page content
        cell = browser.find_element_by_xpath('//*[@data-group="cells"]').find_elements_by_tag_name("g")

        char_matrix = []
        char_row = []
        for a in cell:
            text = a.text.replace("\n", ".")
            texts = text.split(".")
            if self.is_integer(texts[0]):
                char_row.append(texts[1])
            else:
                char_row.append(texts[0])

            if len(char_row) == 5:
                char_matrix.append(copy.deepcopy(char_row))
                char_row.clear()

        print("CHAR MATRIX")
        for c in char_matrix:
            print(c)

        print()

        # getting across answers
        answer_across = []
        word = ""
        for row in char_matrix:
            for c in row:
                if c != "":
                    word = word + c
                else:
                    if len(word) != 0:
                        answer_across.append(copy.deepcopy(word))
                        word = ""
            if len(word) != 0:
                answer_across.append(copy.deepcopy(word))
                word = ""


        print("ACROSS ANSWERS")
        print(answer_across)
        print()

        # getting the down answers
        answer_down = []
        word = ""
        for i in range(0, 5):
            for j in range(0, 5):
                c = char_matrix[j][i]
                if c != "":
                    word = word + c
                else:
                    if len(word) != 0:
                        answer_down.append(copy.deepcopy(word))
                        word = ""
            if len(word) != 0:
                answer_down.append(copy.deepcopy(word))
                word = ""
        print("DOWN ANSWERS")
        print(answer_down)
        print()

        # Getting numbers on the new york times puzzle table which indicates the starting char of the clues
        num_matrix = []
        num_row = []
        for a in cell:
            text = a.text.replace("\n", ".")
            texts = text.split(".")
            if self.is_integer(texts[0]):
                num_row.append(texts[0])
            else:
                num_row.append('-1')

            if len(num_row) == 5:
                num_matrix.append(copy.deepcopy(num_row))
                num_row.clear()

        print("NUM MATRIX")
        for a in num_matrix:
            print(a)

        print()

        print(across_clues)
        print(down_clues)
        print()

        across_match = []

        count = 0
        for i in range(0, len(across_clues)):
            row = ""
            row = across_clues[i] + ":" + answer_across[count]
            count = count + 1
            across_match.append(row)

        print(across_match)
        print()

        down_match = []
        count = 0
        for i in range(0, len(down_clues)):
            row = ""
            row = down_clues[i] + ":" + answer_down[count]
            count = count + 1
            down_match.append(row)

        print(down_match)
        browser.quit()
        return char_matrix, num_matrix, across_clues, down_clues, across_match, down_match

