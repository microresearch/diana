# how can be sure it makes some sense?  either start with some kind of
# structure or discard nonsense after (how to test-with
# regexpr/grammar???)

#way horror portico

#our lady of the white flowers
#queen of hearts
#princess of...

import nltk, random

def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)

def a(input):
    x = input[random.randint(0,len(input) - 1)]
    return x

def plaintaggedtree(text):
    sentences = nltk.sent_tokenize(text)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = [nltk.pos_tag(sent) for sent in sentences] 
    return sentences

#f = open("/root/collect2012-3/diana/documents/paget2.txt")
f = open("/root/diana/chapters/3_glass-crash/texts/allnvfmold")
#f = open("crashchap1")
crash=f.read()#+ff.read()
crash=removeNonAscii(crash)
tokens = nltk.word_tokenize(crash)
text1 = nltk.Text(tokens)
#lines=text1.concordance("autumn", 140, 1000)
# list of terms to re-permute
ll={}

for rnge in range(21):
    ll[rnge]=[]

c = nltk.ConcordanceIndex(text1.tokens, key = lambda s: s.lower())

# list of all words for each position which is what we want

for offset in c.offsets('autumn'):
    for rnge in range(21):
        ll[rnge]=ll[rnge]+[text1.tokens[offset+(rnge-10)]]

# but if we want just words of concordance then:

#for offset in c.offsets('autumn'):
#    print ' '.join(text1.tokens[offset-10:offset+10])



# permute/randomise our x terms
def a(input):
    x = input[random.randint(0,len(input) - 1)]
    return x

sentences=""
for x in range(100):
    sentence=''
    for y in range(21):
        lll=a(ll[y])
        if lll==',':
            sentence= sentence[:-1]+ lll +" "
    # TODO: get rid of all punctuation
        else:
            sentence+= lll +" "
#    print sentence
    sentences+=sentence[:-1]+"."
    print sentence[:-1]+"."

#process sentences

sentences=plaintaggedtree(sentences)

grammar = "NP: {<JJ.*>?<VBD|N.*>?<IN|VBD>?<NN>?<N.*>}" # dt jj nn = the adjective noun 
#grammar = "NP: {<JJ|NN>?<NN><MD|R.*|WDT||V.*|JJ.*|CC|P.*|TO|DT|IN|NN.*|NN|COL|CHR>+}" 


cp = nltk.RegexpParser(grammar)
result = [cp.parse(sent) for sent in sentences]
#print result

nounphrase=[]
npp=""
for sent in result:
    for subtree in sent.subtrees():
#    if len(subtree) == 5:
        np=""
        if subtree.label() == 'NP':
            x=' '.join(nltk.tag.untag(subtree))
            for i in x:
                np += i
            npp += np +" " 
#            print np
            nounphrase.append(np)
#print " ".join(nounphrase)

# sentence=""

for sent in result:
    for subtree in sent.subtrees():
#    if len(subtree) == 5:
        np=""
        if subtree.label() == 'NP':
 #           x=' '.join(nltk.tag.untag(subtree))
#            print x+",",
            for words in sent:
                if isinstance(words[0], tuple):
                    sentence+= a(nounphrase)+" "
                else:
                    if words[0]=="," or words[0]==".":
                        sentence= sentence[:-1] + words[0]+" "
                    else:
                        sentence+=words[0]+" "
        if len(sentence)>100:
            xx=sentence.find("autumn")
            if xx>50:
                print sentence[xx-50:xx+50]
 #               print"",
        #        print sentence[:-1]
        sentence=""


#splitz


# tagging concordances below

