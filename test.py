import re
import pandas as pd
from spellchecker import SpellCheck

checker = SpellCheck()
#######################################################
######## TESTING ACCURACY WITH CUSTOM CORPUS ##########
#######################################################
misspelling_dict = {"ackward": "backward", "acording": "according", "acolade": "accolade",
                          "achived": "achieved", "idaes": "ideas", "identicial": "identical"}

correct_spelling = list(misspelling_dict.values())
n_correct = 0
n_wrong = 0

suggestion_list = [checker.get_best_candidate(word) for word in misspelling_dict.keys()]
      # print(suggestion_list)
for idx, val in enumerate(suggestion_list):
    # print(correct_spelling[idx], "in", val)
    if correct_spelling[idx] in val:
        # print("true")
              n_correct += 1
    else:
              # print("false")
              n_wrong += 1

    accuracy = (n_correct) / (n_correct + n_wrong)
    print(f"Accuracy is {accuracy * 100}%")


#################################################################
####### PREPARING Aspell CORPUS OF MISSPELLED WORDS ##########
#################################################################
test_corpus = "250Aspell_dataset.txt"
#test_corpus = "aspell_dataset.txt"
corpus_dict = {}
with open(test_corpus) as file:
  # read every two lines in the file
  for line1, line2 in zip(file, file):
    #remove the dollar (i.e $) sign
    line1, line2 = re.sub('[^A-Za-z0-9]+', '', line1), re.sub('[^A-Za-z0-9]+', '', line2)
    #print(line1, line2)
    # lowercase the words both the misspellings and their corrections
    line1, line2 = line1.lower(), line2.lower()
    corpus_dict[line1] = line2

print(f"There are a total of {len(corpus_dict)} misspelled words and their corresponding correct spellings in the corpus")

########################################################################################
####### MAKING A PANDAS DATAFRAME WITH THE MISSPELLINGS AND THE CORRECT WORDS ##########
########################################################################################
df = pd.DataFrame(list(zip(corpus_dict.keys(), corpus_dict.values())),columns =['Correct', 'Wrong'])
print(df)


#########################################################
####### TESTING ACCURACY OF  CORRECTING NON-WORDS ERROR WITH WIKIPEDIA CORPUS ##########
#########################################################
correct_spelling = df['Correct']
n_correct = 0
n_wrong = 0

suggestion_list = [checker.get_best_candidate(word) for word in df['Wrong']]
for idx, val in enumerate(suggestion_list):
  #print(correct_spelling[idx], "in", val)
  if val is None:
    #print(idx, correct_spelling[idx],"-->", val)
    continue
  if correct_spelling[idx] in val or val is None:
    #print("true")
    n_correct += 1
  else:
    #print("false")
    n_wrong += 1
    print(idx, correct_spelling[idx],"-->", val)
accuracy = (n_correct ) / (n_correct + n_wrong)
print(f"Accuracy is {accuracy * 100:.2f}%")