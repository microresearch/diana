# Song by Isbrand. Thomas Lovell Beddoes

# TODO: 
# - to follow structure, verse pattern of text rather than sentence
# - pickle the isbrand and correct classification errors by hnad


import random, pickle
import nltk
from textclean.textclean import textclean

#crash_raw = open("crash.txt").read()

esc_chars = [".","...",']',';','%','^','&','_','{',"}","~"]

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

#crash_raw = open("/root/collect2012-3/diana/documents/paget.txt").read()
#crash_raw = open("wounds/crashwounds").read()
crash_raw = open("texts/isbrand").read()
crash_r = textclean.clean(crash_raw)
#sens = nltk.sent_tokenize(crash_raw)
sens = [word.lower() 
        for word in nltk.sent_tokenize(crash_r)]


crash = []
for sen in sens:
    crash += nltk.pos_tag(nltk.word_tokenize(sen))
    crash += ("XXXXX",)
#print crash

# #train_txt = open("/root/collect2012-3/diana/documents/paget.txt").read()
# train_txt = open("/root/collect2012-3/diana/chapters/witnesscasewget/www.casebook.org/witnesses/allwitnessascii").read()
# #train_txt = open("shortpaget").read()
#train_txt = open("wounds/crashwounds").read()

# train_txt = open("texts/crash.txt").read()
# train_txt = textclean.clean(train_txt)
# train_sens = nltk.sent_tokenize(train_txt)
# train_txt = []
# for sen in train_sens:
# 	train_txt += nltk.pos_tag(nltk.word_tokenize(sen))

# mm = {}

# for tword in train_txt:
#     if not(tword[1] in mm):
# #        mm[tword[1]] = [0]
#  #       mm[tword[1]].append(tword[0])
#         mm[tword[1]] = [tword[0]]
#     else:
#         mm[tword[1]].append(tword[0])

# # pickle the tokenised - rather pickle mm

# storepickle(mm,"pickle/crash1.pickle") 
#ttt=recallpickle("pagetsentenced.pickle")+recallpickle("customcrashsentenced.pickle")

mm=recallpickle("pickle/crash1.pickle")



#for k,v in mm.items():
#    print k,v

#print mm.keys().sort()
#ll=mm.keys()
#ll.sort()
#print ll[0]
#print ll

for x in range(1):
    print x
    out = ""
    for word in crash:
#        pos = word[1]
        print word
        if word=="XXXXX": 
            out+="\n"
        else:
            newword = ""
            try:
            #            newword = choose(mm[word[1]]) # + " "
                newword = random.choice(mm[word[1]])+" " # choose from POS key
            #        print mm[word[1]]
            except:
                newword = word[0]+" "
            for ch in esc_chars:
                newword = newword.replace(ch,"")
            out += newword
#    print newword
    print out+"\n\n"
    
# outfile = open("crashpaget002", "w")
# outfile.write(out)
# outfile.close()
