import nltk

def rhyme(inp, level):
     entries = nltk.corpus.cmudict.entries() ## pronunciation dict
     syllables = [(word, syl) for word, syl in entries if word == inp]
     rhymes = []
     for (word, syllable) in syllables:
             rhymes += [word for word, pron in entries if pron[-level:] == syllable[-level:]]
     return set(rhymes)

print rhyme("delight",2)

# example: generate xxx ballardian or whatever noun phrases, or match NPs to poem say isbrand
# count syllables against poem and discard un-matching
# check each for any necessary rhymes after analysis
