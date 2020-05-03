from selenium import webdriver
import re
import numpy as np

class DictionaryScraper:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        # options.add_argument('--headless')
        self.driver = webdriver.Chrome("./chromedriver.exe", options=options)

    """
    :parameter (self, keyword)
    :returns (all_meanings, all_examples)
    """
    def UrbanScraper (self, keyword):
        # No need to make it lower but it is done just for convenience
        self.driver.get("https://www.urbandictionary.com/define.php?term=" + keyword.lower())
        all_meanings = []
        all_examples = []

        try:
            # finding the selenium object which has all of the informations for the given keyword
            definitions = self.driver.find_elements_by_class_name("def-panel")
        except:
            return (all_meanings, all_examples)

        for definition in definitions:
            try:
                # to check whether the header name is the same with the keyword given
                header_element = definition.find_element_by_class_name("def-header")
                header_ = header_element.text
            except:
                continue

            if (keyword.lower() != header_.lower()) :
                continue

            try:
                # getting the meaning
                meaning_element = definition.find_element_by_class_name("meaning")
                all_meanings.append(meaning_element.text)
            except:
                pass

            try:
                # getting the example
                example_element = definition.find_element_by_class_name("example")
                all_examples.append(example_element.text)
            except:
                pass

        return (all_meanings, all_examples)


    """
    :parameter (self, keyword)
    :return (all_meanings, all_synonyms)
    """
    def WordNetScraper(self, keyword):
        self. driver.get("http://wordnetweb.princeton.edu/perl/webwn?s=" + keyword.lower())

        # Under the li tag - they are storing all the information about keyword
        definitions = self.driver.find_elements_by_tag_name("li")

        all_meanings = []
        for definition in definitions:
            text = str(definition.text)
            # for eliminating first paranthesis we find ')' then delete first part
            first_ = text.find(")")
            text = text[first_:]
            # then find the '(' in the remaining text which shows the starting point of the definition
            def_begin = text.find("(")
            def_end = text.rfind (")")
            meaning = text[def_begin + 1: def_end]
            all_meanings.append(meaning)


        arr = []
        for definition in definitions:
            text = str(definition.text)
            # for eliminating first paranthesis we find ')' then delete first part
            first_ = text.find(")")
            text = text[first_ + 1:]
            # then find the '(' in the remaining text which shows the starting point of the definition
            def_begin = text.find("(")
            syn = text[1: def_begin - 1]
            arr.extend([syn])

        all_synonyms = []
        for i in arr:
            words = i.split(",")
            for j in words:
                all_synonyms.append(j.strip())

        try:
            header = all_synonyms[0]
            all_synonyms = list(dict.fromkeys(all_synonyms))
            all_synonyms.remove(header)
        except:
            pass

        return (all_meanings, all_synonyms)


    """
    :parameter (self, keyword)
    :return (all_meanings, all_synonyms)
    """
    def MeriamScraper(self,keyword):
        all_meanings = self.MeriamScraperMeaning(keyword)
        all_synonyms = self.MeriamScraperSynonym(keyword)
        return (all_meanings, all_synonyms)


    """
    :parameter (self, keyword)
    :return all_meanings
    """
    def MeriamScraperMeaning(self, keyword):
        # to be able to direct to the correct site we are using lower function which makes it all lower case letter
        self.driver.get("https://www.merriam-webster.com/dictionary/" + keyword.lower())

        definitions_header = []
        count = 1
        while 1:
            try:
                definitions_header.append(self.driver.find_element_by_id("dictionary-entry-" + str(count)))
                count += 1
            except:
                break

        all_meanings = []

        for definition in definitions_header:
            # getting the object which includes the text
            meaning_elements = definition.find_elements_by_class_name("dtText")

            try:
                # checking wheter header elements are matching with the keyword given
                header_element = definition.find_element_by_tag_name("em")
                header = header_element.text
            except:
                continue

            if (header.lower() != keyword.lower()):
                continue

            # extracting the meanings from the hyper objects
            # first making it string then getting the relevant parts for us
            for meaning in meaning_elements:

                text_found = str(meaning.text)
                index = text_found.find("\n")
                if (index != -1):
                    text_found = text_found[:index]
                if (text_found[0] == ':'):
                    text_found = text_found[2:]
                all_meanings.append(text_found)
        return all_meanings


    """
    :parameter (self, keyword)
    :return all_synonyms
    """
    def MeriamScraperSynonym (self, keyword):
        # to be able to direct to the correct site we are using lower function which makes it all lower case letter
        self.driver.get("https://www.merriam-webster.com/thesaurus/" + keyword.lower())
        synonyms_header = []

        all_thesaurus = self.driver.find_elements_by_class_name("thesaurus-entry")
        all_synoyms = []

        for thesaure in all_thesaurus:

            try:
                # checking wheter header elements are matching with the keyword given
                header_element = thesaure.find_element_by_class_name("thes-list-header")
                header = header_element.text.split(" ")
                header = header[2:]
                header = ''.join(header)
            except:
                continue

            keyword = header
            # getting the object which includes the text
            all_text = thesaure.text.lower()
            first = ("Synonyms for " + keyword + "\n").lower()
            last = ("\nWords Related to " + keyword).lower()

            # extracting the synonyms from the hyper objects
            # first making it string then getting the relevant parts for us
            # print(all_text)
            pattern = first + "(.*?)" + last
            substring = re.findall(pattern, all_text)
            for st in substring:
                each_ = st.split(",")
                for i in each_:
                    word = i.strip()
                    all_synoyms.append(word)

        return all_synoyms


