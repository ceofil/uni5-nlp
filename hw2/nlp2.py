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

    One application that needs syntactic and dependency parsing is, for example, 
    the gmail writing assistant which has to understand the context and the syntactic 
    meaning of the sentences that the user writes in order to suggest suitable words. 

    Another application that uses both syntactic and dependency parsing consists of 
    any voice assistant, for instance, the car voice assistant, Cortana, Siri etc. 
    This type of assistant has to understand the rules of language in order to answer 
    back properly or the commands that it is given. In most cases, the answer to common 
    questions can be hardcoded but by doing so the level of understanding the input is 
    very limited.
 
    Dependency parsing is especially important for applications that rely on text mining
    and on the comprehension of relationships between the subject and the other objects
    in ambiguous cases. This type of application can be found in the business intelligence 
    sector, in advertising, in news (e.g. gathering information about who does the action 
    in headlines). 

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

