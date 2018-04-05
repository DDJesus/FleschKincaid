from curses.ascii import isdigit
from nltk.corpus import cmudict
from nltk.tokenize import sent_tokenize, RegexpTokenizer
from string import digits


class FleschKincaid(object):

    @classmethod
    def grade(self, body, debug=False):
        try:
            d = cmudict.dict()  # Instantiates nltk
            debug_items = []
            body = self.remove_digits(body)
            word_count = self.word_count(body)
            sentence_count = self.sentence_count(body)
            syllable_count = 0

            for word in body.split():
                try:
                    syllable_count += self.nsyl(word, d)[0]
                except KeyError as e:
                    pass

            average_words = self.average_words(word_count, sentence_count)
            average_syllables = self.average_syllables(syllable_count, word_count)

            # Debugging
            debug_items.append(str(word_count))
            debug_items.append(str(sentence_count))
            debug_items.append(str(syllable_count))
            debug_items.append(str(average_words))
            debug_items.append(str(average_syllables))

            result = self.formula(average_words, average_syllables, debug_items, debug)
            if debug:
                self.debugging(debug_items)

            return result[0]

        except Exception as e:
            return e

    def remove_digits(body):
        remove_digits = str.maketrans('', '', digits)
        return body.translate(remove_digits)

    def word_count(body):
        tokenizer = RegexpTokenizer(r'\w+')  # Removes punctuation from being counted as a word
        return len(tokenizer.tokenize(body))

    def sentence_count(body):
        """
        :param body:
        :return:
        """
        return len(sent_tokenize(body))

    def nsyl(word, d):
        """
        :param word: str
        :param d: NLTK dictionary instance
        :return: a list. How many syllables are in a word
        """
        return [len(list(y for y in x if isdigit(y[-1]))) for x in d[word.lower()]]

    def average_words(word_count, sentence_count):
        """
        Check has been added for run-on sentences.
        Per the English language, there should be no more than 25 words per sentence.
        If this happens, divide the total number of words by 25 and add to the total sentence count.
        :param word_count: int
        :param sentence_count: int
        :return: a float. Average words per sentence in body of text
        """
        average_words = word_count / sentence_count
        if average_words >= 25:
            run_on_sentence = average_words / 25
            sentence_count += (math.ceil(run_on_sentence))
            average_words = word_count / sentence_count

        return average_words

    def average_syllables(syllable_count, word_count):
        """
        :param syllable_count: int
        :param word_count: int
        :return: a float. Average syllables in the body of text.
        """
        return syllable_count / word_count

    def formula(average_words, average_syllables, debug_items, debug):
        """
        :param average_words: float
        :param average_syllables: float
        :param debug_items: list
        :param debug: bool
        :return: a list. The Flesch Kincaid grade readability level and a list of variables for debugging.
        """
        words = (average_words * .39)
        syllables = (average_syllables * 11.8)
        added = (words + syllables)
        result = (added - 15.59)

        # Debugging
        debug_items.append(str(words))
        debug_items.append(str(syllables))
        debug_items.append(str(added))
        debug_items.append(str(result))

        if result < 0:
            return [0]
        else:
            return [int(round(result)), debug_items]

    def debugging(debug_items):
        """
        Prints a list of all variables needed for the Flesch Kincaid formula and their values.
        Only called when debug=True is passed to grade()
        :param debug_items: list
        """
        var_list = ["word_count", "sentence_count", "syllable_count", "average_words", "average_syllables", 
                    "words * .39", "syllables * 11.8", "added", "result"]
        for index, item in enumerate(var_list):
            print(item + ": " + debug_items[index])

