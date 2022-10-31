from cmath import exp
import translators as ts
from nltk.util import ngrams

import json
phrase1 = input('Enter phrase: ')
ts_phrase1 = ts.google(phrase1, from_language='ro', to_language='en')
print(f'phrase1 translated: {ts_phrase1}')
is_correct1 = input('is phrase1 correctly translated? (y/n): ')
if is_correct1 == 'n':
    ts_phrase1_correct = input('input the correct translation for phrase1: ')
else:
    ts_phrase1_correct = ts_phrase1
print()
print(phrase1)
print(ts_phrase1_correct)


output_words = set(ts_phrase1.split(' '))
expected_words = set(ts_phrase1_correct.split(' '))


correct_words = output_words & expected_words
print(correct_words)

correct = len(correct_words)

precision = correct / len(output_words)
recall = correct / len(expected_words)
fscore = 2 * precision * recall / (precision + recall)


print(f'precision={precision}')
print(f'recall={recall}')
print(f'fscore={fscore}')


# bleu score
brevity_penalty = len(ts_phrase1.split(' ')) / len(ts_phrase1_correct.split(' '))


max_n = 4
precision_ngrams = {}
for n in range(1,max_n+1):
    output_ngrams = list(ngrams(ts_phrase1.split(' '), n))
    expected_ngrams = list(ngrams(ts_phrase1_correct.split(' '), n))
    precision_ngrams[n] = len( set(output_ngrams) & set(expected_ngrams) ) / len(output_ngrams)

print(json.dumps(precision_ngrams, indent=4))

produs = 1
for value in precision_ngrams.values():
    produs *= value

bleu_score = min(1, len(output_words)/len(expected_words)) * produs ** 1/4
print(bleu_score)




