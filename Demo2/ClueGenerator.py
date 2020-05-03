from DictionaryScraper import DictionaryScraper

class ClueGenerator:
    # def __init__(self):

    def get_new_clues (self, across_match, down_match):
        new_clues_across = []
        new_clues_down = []
        for i in across_match:
            new_clues_across.append(i[0] + str(self.generate_clue(i[1])))
        for i in down_match:
            new_clues_down.append (i[0] + str(self.generate_clue(i[1])))

        return new_clues_down, new_clues_across

    def generate_clue(self, word):
        x = "selam"
        return x