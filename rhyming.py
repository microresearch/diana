import random, pickle
import nltk
from textclean.textclean import textclean
import poetry

# improved sentence breakup with sentence structure intact as was lost before

# TODO: cleanups, ryhming scheme analysis and matchings
# redo so generates and checks after we have syllable count and rhyme scheme
# done as so but doesn't find rhymes
# easiest to suggest rhymes and choose which best fits POS, then recheck syllables,,,,

esc_chars = ["/","?","[","(",")","!",".","...",']',';','%','^','&','_','{',"}","~"]
esc_words = [",",".","'",":","?","'s","'"]

def rhymexxx(inp, level):
     entries = nltk.corpus.cmudict.entries() ## pronunciation dict
     syllables = [(word, syl) for word, syl in entries if word == inp]
     rhymes = []
     for (word, syllable) in syllables:
             rhymes += [word for word, pron in entries if pron[-level:] == syllable[-level:]]
     return set(rhymes)

def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)

def storepickle(text,where):
    out = open(where, 'wb')
    pickle.dump(text, out)
    out.close()

def recallpickle(where):
    out = open(where, 'rb')
    text=pickle.load(out) 
    out.close()
    return text

def choose(listie):
# but we need counter for each POS! - in each list as listie[0] but where is code?
    count=listie[0]+1
    if count>len(listie):
        listie[0]=0
        count=1
    else:
        listie[0]=count
    return listie[count]

#print rhyme("delight",2)

# example: 

# 1-generate xxx ballardian or whatever noun phrases, or match NPs to poem say isbrand

# 1.1 read in and tokenize/list of POSs for train_text/mm

# crash_raw = open("/root/writing/donne").read()
# # crash_raw = open("/root/diana/chapters/3_glass-crash/texts/isbrand").read()
# crash_raw=removeNonAscii(crash_raw)
# nltk_splitter = nltk.data.load('tokenizers/punkt/english.pickle')
# nltk_tokenizer = nltk.tokenize.TreebankWordTokenizer()
# sentences = nltk_splitter.tokenize(crash_raw)

# # what we want is to SPLIT on newline!
# # other approach remove end punkt and add . (with donne by hand!)

# #for para in crash_raw.split('\n'):
# #  sentences.extend(nltk_splitter.tokenize(para)) 
# #print sentences

# tokenized_sentences = [nltk_tokenizer.tokenize(sent) for sent in sentences]
# pos = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
# pos = [[(word, postag) for (word, postag) in sentence] for sentence in pos] # format?

#print pos

mm = {}
train_txt = open("/root/diana/chapters/3_glass-crash/texts/allnvfmold").read()
train_txt=removeNonAscii(train_txt)
train_sens = nltk.sent_tokenize(train_txt)
train_txt = []
for sen in train_sens:
    train_txt += nltk.pos_tag(nltk.word_tokenize(sen))
mm = {}

for tword in train_txt:
    if not(tword[1] in mm):
        mm[tword[1]] = [tword[0]]
    else:
        mm[tword[1]].append(tword[0])

storepickle(mm,"mmfm.pickle") 
#storepickle(pos,"fulldonnepos.pickle") 

#mm=recallpickle("mmfm.pickle") 
pos=recallpickle("fullcrashpos.pickle") # pos is really donne not CRASH....

# rhyme scheme and syllable count first!

syllables=[]
for sentence in pos:
    sylcnto=0
    for word in sentence:
        sylcnto+=poetry.nsyl(word[0])
    syllables.append(sylcnto)

# as 0,1,2 etc

# last words, number of line rhymes with
lastwords=[]

for sentence in pos:
# what is last word?
     lastwords.append(sentence[-2][0])

# dict of rhymescheme
rhymescheme={}

for idx, lastword in enumerate(lastwords):
    #first of lastwords?
    # does it rhy,me with any lastwords we have encountered
    for idxx,lastcomp in enumerate(lastwords[:idx]):
       if poetry.rhyme(lastword,lastcomp):
#           print idx,lastword,lastcomp,idxx
           # dict line x rhymes with line y
           rhymescheme[idx]=idxx 
           break

#print rhymescheme

#//////

# 1.2- list of possible NPs for each sentence

allsentences=[]
for idx,sentence in enumerate(pos):
    while 1:
        out=[]
        for lenny,word in enumerate(sentence):
            try:
                newword = random.choice(mm[word[1]]) # choose from POS key
            except:
                newword = word[0]

            newword = newword.translate(None, '!@#$//[]')
            if lenny==len(sentence)-2:         # are we on last (but one) word. last is punctuation! 
                    if idx in rhymescheme:
                        # find a rhyme
                        oldword=newword
                        newword=""
                        for eachone in mm[word[1]]:
                            if poetry.rhyme(eachone,allsentences[rhymescheme[idx]][-2]):
                                newword=eachone # take the last
                        ## result or not? if not then just take last newword generated (as is now)
                        ## or force this to random rhyme from dict matching POS?- now is just random
                        if newword=="":
                            try:
                                newword=random.choice(rhymexxx(allsentences[rhymescheme[idx]][-2], 2))
                            except:
                                newword=oldword
            out.append(newword)
        #count syllables for out
        syl=0
        for word in out:
            syl+=poetry.nsyl(word)
        if syl==syllables[idx]:
            allsentences.append(out)
#            print " ".join(allsentences[idx])
            break

# TODO: formatting of sentences    
# end of lines, punctuation within
for sentences in allsentences:
    words=""
    for idx,word in enumerate(sentences): 
        for ch in esc_chars:
            word = word.replace(ch,"")
        if word in esc_words:
            words+= word
        elif idx==0: 
            words+=word.title()
        else:
            words+=" "+ word
    print words
