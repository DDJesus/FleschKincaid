from curses.ascii import isdigit
from nltk.corpus import cmudict
import string
from string import digits, punctuation

class FleschKincaid(object):

    @classmethod
    def grade(self, body, debug_mode=False):
        try:
            d = cmudict.dict()  # Instantiates nltk
            debug_items = []

            word_count = 0
            sentence_count = 0
            syllable_count = 0

            for word in body.split():
                try:
                    if word == '':
                        pass
                    else:
                        word_count += 1
                        word = self.remove_digits(word)
                        sentence_count += self.sentence_count(word, sentence_count)
                        if "'" in word:
                            word = word.split("'", maxsplit=1)[0]
                        word = self.remove_punc(word)
                        syllable_count += self.nsyl(word, d)[0]
                except KeyError as e:
                    pass

            debug_items.append(str(word_count))
            debug_items.append(str(sentence_count))
            debug_items.append(str(syllable_count))
            if sentence_count == 0:
                sentence_count = 1
            average_words = self.average_words(word_count, sentence_count)
            average_syllables = self.average_syllables(syllable_count, word_count)
            debug_items.append(str(average_words))
            debug_items.append(str(average_syllables))

            result = self.formula(average_words, average_syllables, debug_items, debug_mode)
            if debug_mode:
                self.debugging(debug_items)

            return result[0]

        except Exception as e:
            return e


    def remove_digits(word):
        remove_digits = str.maketrans('', '', digits)
        word = word.translate(remove_digits)

        return word


    def sentence_count(word, sentence_count):
        sentences = 0
        endings_repeat = ["..", "??", "!!"]
        if any(i in word for i in endings_repeat):
            sentences += 1

            return sentences
        else:
            sentences += word.count(".")
            sentences += word.count("?")
            sentences += word.count("!")

            return sentences


    def remove_punc(word):
        translator = str.maketrans('', '', string.punctuation)
        word = word.translate(translator)

        return word


    def nsyl(word, d):
        syllables = [len(list(y for y in x if isdigit(y[-1]))) for x in d[word.lower()]]

        return syllables

    def average_words(word_count, sentence_count):
        average_words = word_count / sentence_count
        if average_words >= 25:
            run_on_sentence = average_words / 25
            sentence_count += (math.ceil(run_on_sentence))
            average_words = word_count / sentence_count

        return average_words


    def average_syllables(syllable_count, word_count):
        average_syllables = syllable_count / word_count

        return average_syllables


    def formula(average_words, average_syllables, debug_items, debug_mode):
        words = (average_words * .39)
        syllables = (average_syllables * 11.8)
        added = (words + syllables)
        result = (added - 15.59)
        debug_items.append(str(words))
        debug_items.append(str(syllables))
        debug_items.append(str(added))
        debug_items.append(str(result))

        return [int(round(result)), debug_items]


    def debugging(debug_items):
        var_list = ["word_count", "sentence_count", "syllable_count", "average_words", "average_syllables", 
                    "words * .39", "syllables * 11.8", "added", "result"]
        for index, item in enumerate(var_list):
            print(item + ": " + debug_items[index])

