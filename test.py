# cat ~/diana/chapters/3_glass-crash/texts/isbrand | python test.py

import nltk
import re
import sys
import random
from textclean.textclean import textclean

def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)

text = ''
for line in sys.stdin:
#    print line
    text += removeNonAscii(line)


def tokenize_text_and_tag_named_entities(text):
    tokens = []
    names_list = []
    for sentence in nltk.sent_tokenize(text):
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sentence))):
            try:
                chunk.label()
            except AttributeError:
                tokens.append(chunk[0])
            else:
                if chunk.label() == 'PERSON':
                    names = ' '.join(c[0] for c in chunk.leaves())
                    if names not in names_list:
                        names_list.append(names)
    print ', '.join(names_list)
    return tokens


tokenize_text_and_tag_named_entities(text)
  
