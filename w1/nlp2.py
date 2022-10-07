from nltk.corpus import wordnet as wn
import nltk
import random
import numpy as np
from nltk import CFG
import spacy
import stanza

stanza.download('en')
nltk.download('omw-1.4')
nltk.download('wordnet')


'''
    Ex. 4) https://docs.google.com/document/d/1HT5_4lr77TAyJ5k4cI48qGw8tpVekUyRmMOyGr5eJzo/edit?fbclid=IwAR1X-hCiYZ1BIluIgCiJ7xO_N8AwTpU7XBwGRdc3JGchq0pQxF7tOtHRjSc
'''


sentence1 = "Papa eats octopus in pajamas"
sentence2 = "John often eats sea food or octopus"
sentence3 = "John and Mary eat often together"


grammar = nltk.CFG.fromstring("""
  S -> NP VBZ | NP 
  NP -> NP CC NP VB 
  VB -> VB RB PDT
  VBZ -> VBZ NN | RB VBZ 
  NN -> IN NN | NN | NN CC

  NN -> "octopus" | "pajamas" | "sea" | "food"
  NP ->  "Papa" | "John" | "Mary"
  VBZ -> "eats"
  VB -> "eat"
  RB -> "often"
  PDT -> "together"
  IN -> "in" 
  CC -> "and" | "or"
""")


def parse_sentence(grammar, sentence):
    parser = nltk.ChartParser(grammar)
    sentence = sentence.split()

    for tree in parser.parse(sentence):
        print (list(tree))


def left_corner_chart_parser(grammar, sentence):
    sr_parser = nltk.LeftCornerChartParser(grammar, trace=2)
    sentence = sentence.split()
    sr_parser.parse(sentence)


def stanza_dep_parser(sentence):
    nlp = stanza.Pipeline('en', processors = 'tokenize,pos,lemma,depparse')
    doc = nlp(sentence)
    doc.sentences[0].print_dependencies()


def main():
    parse_sentence(grammar, sentence1)
    left_corner_chart_parser(grammar, sentence2)
    stanza_dep_parser(sentence3)

if __name__ == "__main__":
    main()

