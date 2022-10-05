from nltk.corpus import wordnet as wn
import nltk
import random
import numpy as np


# nltk.download('omw-1.4')
# nltk.download('wordnet')

def get_hypernyms(theme):
  all_hypernyms = []
  n_hypernyms = 10

  curr_hypernyms = theme.hypernyms()
  all_hypernyms.extend(curr_hypernyms)

  tries = 0
  while len(all_hypernyms) < n_hypernyms and tries < 1000:
    new_hypernyms = []
    for word in curr_hypernyms:
      word_hypernyms = word.hypernyms()
      new_hypernyms.extend(word_hypernyms)
    curr_hypernyms = new_hypernyms
    all_hypernyms.extend(new_hypernyms)
    tries += 1
  if len(all_hypernyms) < n_hypernyms:
    print(f'only {len(all_hypernyms)} hypernims found')
  return all_hypernyms

def get_antonyms(word_str):
  antonyms = []
  for syn in wn.synsets(word_str):
      for i in syn.lemmas():
          if i.antonyms():
                antonyms.append(i.antonyms()[0].name())
  return antonyms

def get_hyponyms(theme):
  all_hyponyms = []
  n_hyponyms = 10

  curr_hyponyms = theme.hyponyms()
  all_hyponyms.extend(curr_hyponyms)


  tries = 0
  while len(all_hyponyms) < n_hyponyms and tries < 1000:
    new_hyponyms = []
    for word in curr_hyponyms:
      word_hyponyms = word.hyponyms()
      new_hyponyms.extend(word_hyponyms)
    curr_hyponyms = new_hyponyms
    all_hyponyms.extend(new_hyponyms)
    tries += 1
  if len(all_hyponyms) < n_hyponyms:
    print(f'only {len(all_hyponyms)} hypernims found')

  return all_hyponyms

def get_nyms(theme, max_nyms=7):
  all_nyms = get_hyponyms(theme) + get_hypernyms(theme) 
  random.shuffle(all_nyms)
  return all_nyms[:max_nyms]

def get_synonyms(word):
  synonyms = []
  for syn in wn.synsets(word):
    for l in syn.lemmas():
      synonyms.append(l.name())
  return synonyms

def get_hint(word):
  hint_types = [
      'definition',
  ]
  antonyms = get_antonyms(str(word))
  synonyms = get_synonyms(str(word))

  if antonyms:
    hint_types.append('antonym')
  if synonyms:
    hint_types.append('synonym')
  hint_type = random.choice(hint_types)
  hint = None
  if hint_type == 'antonym':
    hint = antonyms[0]
  elif hint_type == 'synonym':
    hint = synonyms[0]
  elif hint_type == 'definition':
    hint = word.definition()
  return hint_type, hint

def get_all_hints(words):
  all_hints = []

  for word in words:
    for antonym in get_antonyms(str(word)):
      all_hints.append({
        'word': word.lemma_names()[0],
        'type': 'antonym',
        'hint': antonym
      })
    for synonym in get_synonyms(str(word)):
      all_hints.append({
        'word': word.lemma_names()[0],
        'type': 'synonym',
        'hint': synonym
      })
    all_hints.append({
        'word': word.lemma_names()[0],
        'type': 'definition',
        'hint': word.definition()
    })
  return all_hints

import sys
theme_str = 'dog'
if len(sys.argv) > 1:
    theme_str = sys.argv[1]
theme = wn.synsets(theme_str)[0]
nyms = get_nyms(theme, max_nyms=7)
# for word in nyms:
#   print(word, get_hint(word))

  
words = [word.name().split('.')[0] for word in nyms]
words.sort(key=lambda w: len(w), reverse=True)

width = 51
height = 51



board = np.chararray((width, height))
board[:] = '-'


def put_h_word(word, x, y):
  global board
  board[y, x:x+len(word)] = np.array(list(word))

def put_v_word(word, x, y):
  global board
  board[y:y+len(word), x] = np.array(list(word))

def print_board():
  global board
  for y in range(board.shape[0]):
    for x in range(board.shape[1]):
      print(board[y,x].decode("utf-8"), end='')
    print('')

def get_board_str():
    global board
    output = ''
    for y in range(board.shape[0]):
        for x in range(board.shape[1]):
            output += board[y,x].decode("utf-8")
        output += '\n'
    return output

def get_matches(word):
  global board
  matches = []
  for y in range(board.shape[0]):
    for x in range(board.shape[1]):
      cell_value = board[y,x].decode("utf-8")
      if cell_value in word:
        cell_pos = (x,y)
        word_pos = word.find(cell_value)
        match = (cell_pos, word_pos)
        matches.append(match)
  return matches

def check_if_segment_breaks(word, segment):
  for encoded_segment_letter, word_letter in zip(segment, word):
    segment_letter = encoded_segment_letter.decode('utf8')
    if segment_letter == '-':
      continue
    if segment_letter == word_letter:
      continue
    return True 
  return False

def check_if_match_is_valid(word, match):
  global board
  cell_pos, word_pos = match
  vertical_y_start = cell_pos[1] - word_pos
  vertical_slice = board[
      vertical_y_start : vertical_y_start + len(word), 
      cell_pos[0]
  ]

  horizontal_x_start = cell_pos[0] - word_pos
  horizontal_slice = board[
      cell_pos[1],
      horizontal_x_start : horizontal_x_start + len(word)
  ]
  
  if not check_if_segment_breaks(word, horizontal_slice):
    return 'h'
  if not check_if_segment_breaks(word, vertical_slice):
    return 'v'
  return '' # evaluated as false

def trim_board():
  global board
  xs = []
  ys = []
  for y in range(board.shape[0]):
    for x in range(board.shape[1]):
      cell_value = board[y,x].decode("utf-8")
      if not cell_value == '-':
        xs.append(x)
        ys.append(y)
  top = min(ys)
  bottom = max(ys)
  left = min(xs)
  right = max(xs)

  board = board[top:bottom+1, left:right+1] 
  return left,top
    
board_info = [
    {
          'x': width//2 - len(words[0])//2,
          'y': height//2,
          'orientation': 'h',
          'word': words[0]
    }
]
put_h_word(words[0], width//2 - len(words[0])//2, height//2)

for word in words[1:]:
  matches = get_matches(word)
  random.shuffle(matches)
  for match in matches:
    valid_orientation = check_if_match_is_valid(word, match)
    if not valid_orientation: 
      continue
    cell_pos, word_pos = match
    if valid_orientation == 'h':
      horizontal_x_start = cell_pos[0] - word_pos
      put_h_word(word, horizontal_x_start, cell_pos[1])
      info = {
          'x': horizontal_x_start,
          'y': cell_pos[1],
          'orientation': 'h',
          'word': word
      }
      board_info.append(info)
      break
    elif valid_orientation == 'v':
      vertical_y_start = cell_pos[1] - word_pos
      put_v_word(word, cell_pos[0], vertical_y_start)
      info = {
          'x': cell_pos[0],
          'y': vertical_y_start,
          'orientation': 'v',
          'word': word
      }
      board_info.append(info)
      break


# for word in words:
#   print(word)
left,top = trim_board()
# print_board()

import json 
for info in board_info:
  info['x'] -= left
  info['y'] -= top
board_info_dumps = json.dumps(board_info)
hints_dumps = json.dumps(get_all_hints(nyms))

with open('template.html', 'r') as fd:
    template = fd.read()
    template = template.replace('$HINTS', hints_dumps)
    template = template.replace('$BOARDSINFO', board_info_dumps)
    template = template.replace('$BOARD', get_board_str())

    result_path = f'{theme_str}.html'
    with open(result_path, 'w') as result_fd:
        result_fd.write(template)
        print(f'puzzle path: {result_path}')
    