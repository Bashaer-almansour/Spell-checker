# import nltk
import re
import spacy
import pandas as pd
from collections import Counter, OrderedDict
from operator import itemgetter
from nltk.metrics.distance import edit_distance

TOKEN_PATH = "the processed PG corpora.txt"
LEXICON_PATH = "the unique words.txt"
nlp = spacy.load("en_core_web_sm")

class SpellCheck:
    """ The SpellChecker class utilizes the power of edit distance, N-gram[uni-gram], look-up dictionary and NER
      to detect and correct misspellings specially non-word errors .
    """
    def __init__(self):
        """Read tokenized text [i.e., the processed data]"""
        # read tokenized words and converting them to a set
        # to obtain the unique words to enrich the lookup dictionary
        with open(LEXICON_PATH, "r", encoding='UTF-8') as vocab_list:
            unique_contents = vocab_list.readlines()
            unique_word = [word.strip().lower() for word in unique_contents]
        self.vocab_list_set = unique_word

        with open(TOKEN_PATH, "r", encoding='UTF-8') as token_file_content:
            tokenized_word = [word.strip().lower() for word in token_file_content]
        self.vocab_list = tokenized_word
        self.unigram_count = Counter(self.vocab_list)
        #print(list(self.unigram_count.items())[:10])
        #self.unigram_count = Counter(self.vocab_list_set)
        #print(self.unigram_count["project"])

    def get_statistics(self):
        print(f"Total number of words after preprocessing is {len(self.vocab_list)}")
        print(f"Total number of unique words is {len(self.vocab_list_set)}")

    def get_candidates(self, token):

        """ Get nearest word for a given incorrect word.
            Args:
                token (str): The string to be filtered for misspelled words
            Returns:
                list (str): List of alternative words
        """
        s = [edit_distance(i, token) for i in self.vocab_list_set]
        # Store the nearest words in ordered dictionary
        dist = dict(zip(self.vocab_list_set, s))
        dist_sorted = dict(sorted(dist.items(), key=lambda x: x[1]))
        minimal_dist = list(dist_sorted.values())[0]
        alternative_word_list = list(filter(lambda k: dist_sorted[k] == minimal_dist, dist_sorted.keys()))

        return alternative_word_list

    def check(self, text):
        """Given a word, check it for typo
          Args:
            text (str): The string to be filtered for misspelled words
          Returns:
            Bool (str): True if it is a misspelling and False if otherwise
        """
        if self.check_error(text):
            return True
        return False
    def check_error(self, text):
        """ Given a word, find out the errors
        Args:
            text (str): The string to be filtered for misspelled words
        Returns:
            list (str): List of misspelled words
        """
        #contractions_list =[ ]
        input_text = nlp(text)
        list_miss = [token for token in input_text
                     if token.text.lower() not in self.vocab_list_set
                     if "'" not in token.text
                     #and token.text.lower() not in contractions_list
                     and token.ent_type_ != "PERSON"
                     and (token.ent_type_ != "GPE")
                     and (token.ent_type_ != "ORG")
                     and (not token.like_num)
                     and (not token.is_currency)
                     and (not token.like_email)
                     and (not token.like_url)
                     and (not token.is_space)]
        return list_miss

    def get_unigram_probability(self):
        """This function returns a unigram frequency for a given word."""
        total_unigram_count = float(sum(self.unigram_count.values()))
        unigram_probability = {word: self.unigram_count[word] / total_unigram_count for word in
                               self.unigram_count.keys()}
        return unigram_probability



    def get_best_candidate(self, word):
        """ Given an incorrectly spelt word, we want to get a list of close candidate
            Args:
                word (str): The string to be filtered for misspelled words
            Returns:
                list (str): List of best candidate matches for the misspelled word
        """
        # check if word is a typo, if yes, return None, if No, get suggested words
        error = self.check_error(word)
        if not error:
            print(f"{word} is a valid entry")
            return None
        if self.check_error(word):
            candidates = self.get_candidates(word)
            if not candidates:
                print(f"No suggestions for {word}")
                return None
            if len(candidates) == 1:
                return candidates
            elif len(candidates) > 1:
                unigram_prob = self.get_unigram_probability()
                # get the probability of each suggested word
                best_candidate = [(word, unigram_prob[word]) for word in candidates]
                # sort the candidates based on their probability
                best_candidate = sorted(best_candidate, key=itemgetter(1), reverse=True)
                # get only the words from the list of tuples and ignore their probabilities
                best_candidate = [candidate[0] for candidate in best_candidate]
                # return all the candidates if they are not more than 5, else return only the top 5
                if len(best_candidate) == 5:
                    return best_candidate
                return best_candidate[:5]

    def get_sent_candidate(self, sentence):
        """ Given a sentence with incorrectly spelt words, we want to get a dictionary of close candidate
            Args:
                sentence (str): The string to be filtered for misspelled words
            Returns:
                dict (str): Dictionary of best candidate matches for the misspelled word
        """
        suggestion_dict = OrderedDict()  # we use Orderdict instead of dict() to preserve the order of the dictionary
        word_list = [token.text for token in nlp(sentence)]
        for word in word_list:
            if self.check_error(word):
                candidates = self.get_candidates(word)
                # check that suggestions are valid english word
                candidates = [candidate for candidate in candidates if candidate in self.vocab_list_set]
                suggestion_dict[word] = candidates
        return suggestion_dict


#if __name__ == '__main__':
      #checker = SpellCheck()
      # checker.check("fathir")
      # checker.get_unigram_probability()
      # checker.check("boy")
      #print(checker.get_candidates("boye"))
      # checker.get_best_candidate("wrods")
      #print(checker.get_sent_candidate("This is a poweful spel checking softwaer because it can't take long time to detect the errors"))
      #print(checker.get_sent_candidate("This is intentonally mispelled to knowe if the softwera works corectly or it containe mistace and seev how it can bz correted using ngram"))
      #print(checker.check_error("This is a poweful spel checking softwaer because it can't take long time to detect the errors"))