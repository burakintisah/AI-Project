from DictionaryScraper import DictionaryScraper
from difflib import SequenceMatcher
import gensim
from gensim.models import FastText
from gensim.test.utils import get_tmpfile
import os


class ClueGenerator:
    def __init__(self):
        # print('Loading Model..')
        self.model = self.__load_model()
        # Initializing data scraper
        self.ds = DictionaryScraper(self.model)

    def __similar(self, a, b):
        similarity = SequenceMatcher(None, a, b).ratio()
        return similarity


    def get_new_clues (self, across_match, down_match):
        new_clues_across = []
        new_clues_down = []
        for i in across_match:
            new_clues_across.append(i[0] + str(self.generate_clue(i[1])).capitalize())
        for i in down_match:
            new_clues_down.append (i[0] + str(self.generate_clue(i[1])).capitalize())

        return new_clues_down, new_clues_across


    def generate_clue(self, word):

        print("\nCreating clue for the word: {}".format(word.upper()))
        result = ""

        print("Scraping data from Wordnet: {}".format(word.upper()))
        meaning_wordnet, synonym_wordnet = self.ds.WordNetScraper(word)
        meaning_wordnet = self.check_data (word, meaning_wordnet, 0)

        if len(meaning_wordnet) == 0:

            print("Scraping data from Meriam: {}".format(word.upper()))
            meaning_meriam, synonym_meriam = self.ds.MeriamScraper(word)
            meaning_meriam = self.check_data(word, meaning_meriam, 0)

            if len(meaning_meriam) == 0:


                print("Scraping data from Urban: {}".format(word.upper()))
                meaning_urban, example_urban = self.ds.UrbanScraper(word)
                meaning_urban = self.check_data(word, meaning_urban, 0)

                if len(meaning_urban) == 0:

                    print("Scraping data from Google: {}".format(word.upper()))
                    clue = self.ds.get_google_clue(word)

                    if clue == "":

                        print("Scraping data from model for the word: {}".format(word.upper()))
                        synonym_model = self.ds.get_words_from_model(word)
                        all_synonyms = synonym_wordnet + synonym_model + synonym_meriam

                        if len(all_synonyms) != 0:
                            synonyms_organized = self.check_data(word, all_synonyms, 1)
                            result = synonyms_organized[0]

                    else:
                        result = clue

                else:
                    result = meaning_urban[0]
            else:
                result = meaning_meriam[0]
        else:
            result = meaning_wordnet[0]

        print(result.capitalize())
        return result.lstrip()


    def check_data (self, word, all_data, is_synonym):
        result = []
        for text in all_data:
            text_arr = text.split()
            text_len = len(text_arr)
            if text_len > 10:
                continue
            all_diff = 1
            for each in text_arr:
                similarity = self.__similar(each.lower(), word.lower())
                if similarity > 0.5:
                    all_diff = 0
                    break
            if all_diff == 0:
                continue
            result.append(text)

        if is_synonym == 1:
            result = list(dict.fromkeys(result))
            #result.sort(key=lambda a: self.__similar(a, word))
        return result


    # we load our vector which we have downloaded from the internet and saving it as 'customModel.model'
    def __save_model (self):
        model = gensim.models.KeyedVectors.load_word2vec_format("wiki-news-300d-1M.vec")
        model.save("customModel.model")


    def __load_model (self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        loadModel = get_tmpfile(dir_path + "/" + "customModel.model")
        model = gensim.models.KeyedVectors.load(loadModel)
        return model

'''
cg = ClueGenerator()
a = cg.generate_clue('desus')'''