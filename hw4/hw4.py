import translators as ts



total_phrases = 0
correct = 0

def precision_score(tp, fp):
    return tp / (tp + fp)

def recall_score(tp, fn):
    return tp / (tp + fn)

def f_score(precision_score, recall_score):
    return 2 * (precision_score * recall_score) / (precision_score + recall_score)

phrase = None
while True:
    phrase = input('Enter phrase: ')
    if phrase.upper() == '<END>':
        break
    total_phrases += 1
    ts_phrase = ts.google(phrase, from_language='en', to_language='ro')
    print('translated phrase: ', ts_phrase)

    valid = input('is the translation valid? (y/n): ')
    if valid.lower() == 'y':
        correct += 1

    print(f'correct translations: {correct}/{total_phrases}\n')



# correct