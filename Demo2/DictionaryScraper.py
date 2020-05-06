from selenium import webdriver
import re
from difflib import SequenceMatcher
from googletrans import Translator

class DictionaryScraper:
    def __init__(self, model):
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        #options.add_argument('--headless')
        self.driver = webdriver.Chrome("./chromedriver.exe", options=options)
        self.model = model

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
                all_synonyms.append(j.strip().lower())

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
        all_meanings = self.__MeriamScraperMeaning(keyword)
        all_synonyms = self.__MeriamScraperSynonym(keyword)
        return (all_meanings, all_synonyms)


    """
    It is a pretrained model, which gives output which are the most similar words in the model.
    :parameter (self, keyword)
    :return (all_meanings, all_synonyms)
    """
    def get_words_from_model (self,word):
        try:
            prediction_similar = self.model.most_similar(positive=[word], topn=10)
            # print(prediction_similar)

            if prediction_similar[0][1] > 0.60:
                # print("Prediction has sufficient accuracy for the word: {} ".format(word.upper()))
                model_result = prediction_similar
            else:
                # print("not sufficient accuracy for the word: {}".format(word.upper()))
                # print("best accuracy: ", str(prediction_similar[0][1]))
                model_result = []
                return model_result
        except:
            # print("could not find the word: {}".format(word.upper()))
            model_result = []
            return model_result
        # searching the predictions
        less_similars = []
        for check in model_result:
            if check[1] < float(0.50):
                less_similars.append(check)
        for i in less_similars:
            model_result.remove(i)

        # eliminate if the word is very similar to the word given
        # since we dont want to show the answer of the clue
        result = []
        for i in model_result:
            similarity = self.__similar(word.lower(), i[0].lower())
            #print(similarity)
            if similarity < 0.5 :
                result.append(i[0].lower())

        return result

    """
    :parameter (self, keyword)
    :return clue
    """
    def get_google_clue(self, word):

        word = word.lower()

        name, definition = self.__google_snippet(word)

        if name == "" or definition == "":
            return ""

        name = name.strip().lower()
        definition = definition.strip().lower()

        translator = Translator()
        definition = translator.translate(definition).text

        name_list = name.split()

        clue = ""
        for n in name_list:
            if n != word:
                clue = clue + " " + n
            else:
                clue = clue + " ___ "

        clue = clue + ", " + definition
        return clue


    """
    :parameter (self, keyword)
    :return all_meanings
    """
    def __MeriamScraperMeaning(self, keyword):
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
    def __MeriamScraperSynonym (self, keyword):
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
                    all_synoyms.append(word.lower())

        return all_synoyms


    def __google_snippet(self, keyword):
        name = ""
        definition = ""

        self.driver.get("https://www.google.com/search?q =" + str(keyword.lower))
        webElement = self.driver.find_element_by_name("q")
        webElement.send_keys(keyword.lower())
        webElement.submit()

        try:
            element = self.driver.find_element_by_xpath("//*[@data-attrid=\"title\"]")
            name = element.text
        except:
            name = ""

        try:
            element = self.driver.find_element_by_xpath("//*[@data-attrid=\"subtitle\"]")
            definition = element.text
        except:
            definition = ""

        return name, definition

    def __similar(self, a, b):
        similarity = SequenceMatcher(None, a, b).ratio()
        return similarity

