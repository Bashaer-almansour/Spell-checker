import re  # Regular Expression (re) in python
import nltk  # Natural Language Processing Toolkits (nltk) in python
from nltk.tokenize import word_tokenize

nltk.download('punkt')


RAW_CORPUS_PATH = "PG corpora.txt"
TOKEN_PATH = "the processed PG corpora.txt"
LEXICON_PATH = "the unique words.txt"

class PrepareCorpus:

    def __init__(self):
        contents = open(RAW_CORPUS_PATH, "r", encoding='UTF-8')
        corpora_contents = contents.readlines()
        lines = [content.strip() for content in corpora_contents]
        clean_word_token = [self.remove_bad_char("".join(token)) for token in lines]
        doc = " ".join([word.lower() for word in clean_word_token])
        doc = nltk.word_tokenize(doc)
        #print(f"Total number of PG corpora words after pre-processing: {len(doc)}")
        #print(f"sample of text after pre-processing : {doc[0:8]}")

        # write the tokenized text into a file to speed up processing
        with open(TOKEN_PATH, "w", encoding='UTF-8') as out_file:
            for word in doc:
                out_file.write(word)
                out_file.write("\n")
        lexicon = sorted(set(doc))
        #print(f"sample of text the unique words : {lexicon[4:14]}")

        #print(f"Total number of lexicon words : {len(lexicon)}")
        with open(LEXICON_PATH, "w", encoding='UTF-8') as lexicon_file:
            for word in lexicon:
                lexicon_file.write(word)
                lexicon_file.write("\n")

    @staticmethod
    def remove_bad_char(text):
        """Removes everything aside alphabets"""
        return re.sub(r'[^A-Za-z]', ' ', text)

if __name__ == '__main__':
    PrepareCorpus()