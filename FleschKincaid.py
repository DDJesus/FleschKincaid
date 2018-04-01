from curses.ascii import isdigit
from nltk.corpus import cmudict
import string
from string import digits, punctuation

class FleschKincaid(object):

	@classmethod
	def grade(self, body):
		try:
			d = cmudict.dict()  # Instantiates nltk

			word_count = 0
			sentence_count = 1
			syllable_count = 0

			for word in body.split():
				if word == '':
					pass
				else:
					word_count += 1
					word = self.remove_digits(word)
					sentence_count += self.sentence_count(word, sentence_count)
					word = self.remove_punc(word)
					syllable_count += self.nsyl(word, d)[0]

			average_words = self.average_words(word_count, sentence_count)
			average_syllables = self.average_syllables(syllable_count, word_count)
			return self.formula(average_words, average_syllables)
		except KeyError as e:
			return 'KeyError: ' + str(e) + '. This error is usually thrown when a word passed to grade() is unrecognized by the nltk library, or if there is no text. Did you spell the word correctly? You can read more about this libary here: https://www.nltk.org/'

	def remove_digits(word):
		remove_digits = str.maketrans('', '', digits)
		word = word.translate(remove_digits)
		return word


	def sentence_count(word, sentence_count):
		endings_repeat = ["..", "??", "!!"]
		if any(i in word for i in endings_repeat):
			sentence_count += 1
		else:
			sentence_count += word.count(".")
			sentence_count += word.count("?")
			sentence_count += word.count("!")
			return sentence_count


	def remove_punc(word):
		translator = str.maketrans('', '', string.punctuation)
		word = word.translate(translator)
		return word


	def syllable_count(word, syllable_count, d):
		syllable_list = nsyl(word, d) 
		syllable_count += syllable_list[0]
		return syllable_count


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


	def formula(average_words, average_syllables):
		words = (average_words * .39)
		syllables = (average_syllables * 11.8)
		added = (words + syllables)
		result = (added - 15.59)
		return int(round(result))