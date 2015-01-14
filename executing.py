# copying code from: classgen.py
# start to think how to execute text on itself
# using POS tag as instruction and fdist as operand?
# what kind of operations on text, text to come, text passed
# subsitute POS of next/previous word...

import nltk, random

def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)


train_txt = open("/root/diana/chapters/3_glass-crash/texts/crashchap1").read()
train_txt=removeNonAscii(train_txt)
train_sens = nltk.sent_tokenize(train_txt)
train_txt = []
for sen in train_sens:
	train_txt += nltk.pos_tag(nltk.word_tokenize(sen))

xx=[]
inc=0
fdist1 = nltk.FreqDist(train_txt) 
mm = {}

for word in train_txt:
    xx.append((word, fdist1[word]))
    if not(word[1] in mm): # key
	    mm[word[1]] = [(word[0],word[1])]
    else:
	    mm[word[1]].append((word[0], word[1]))

# map part of speech to instruction/number - dictionary

instructionlist=[]
for elements in xx:
	if elements[0][1] not in instructionlist:
		instructionlist.append(elements[0][1])
#print instructionlist

# test access elements

# for elements in xx:
# 	print "word %s inst %s op %s" %  (elements[0][0], instructionlist.index(elements[0][1]), elements[1]) 

IP=0
x=1

# how can we handle threads? as a list parsed from the beginning?
# and each thread with local register and a leaking stack

register=0
while x:
	IP+=1
	if IP>=len(xx):
		x=0
		IP=0
	opcode=instructionlist.index(xx[IP][0][1])
	operand=xx[IP][1]
#	print "instruction %s operand %s" % (opcode,operand)
	opcode=opcode%11
	print xx[IP][0][0], # print the word
	if   opcode == 0: x=1 #do nothing
	elif opcode == 1: # change word to random word in same POS
		newword = random.choice(mm[xx[IP][0][1]]) # choose from POS key 
		xx[IP]=(newword,fdist1[newword])
	elif opcode == 2: # change prev word
		newword = random.choice(mm[xx[IP][0][1]]) # choose from POS key 
		where=IP-1
		if where<0: where=0
		xx[where]=(newword,fdist1[newword])
	elif opcode == 3: # change next word
		newword = random.choice(mm[xx[IP][0][1]]) # choose from POS key 
		where=IP+1
		if where==len(xx): where=len(xx)-1
		xx[where]=(newword,fdist1[newword])
		IP+=1
	elif opcode == 4:
		IP=operand%len(xx)
	elif opcode == 5:
		if register==0:
			IP=operand%len(xx)
	elif opcode == 6:
		newword = random.choice(mm[xx[IP][0][1]]) # choose from POS key 
		where=register
		xx[where]=(newword,fdist1[newword])
	elif opcode == 7:
		newword = random.choice(mm[xx[register][0][1]]) # choose from POS key at register 
		where=IP
		xx[where]=(newword,fdist1[newword])
	elif opcode == 8:
		# load register from word at operand
		register=instructionlist.index(xx[operand%len(xx)][0][1])
	elif opcode == 9:
		register=(register+instructionlist.index(xx[operand%len(xx)][0][1]))%len(xx)
	elif opcode == 10:
		register=(register-instructionlist.index(xx[operand%len(xx)][0][1]))%len(xx)
		

#     elif opcode == 1 : reg[r]=mem[addr]          # load register
#     elif opcode == 2 : mem[addr]=reg[r]          # store register
#     elif opcode == 3 : reg[r]=addr               # load register immediate
#     elif opcode == 4 : reg[r]=mem[reg[addr]]     # load register indexed
#     elif opcode == 5 : reg[r]=reg[r]+reg[addr]   # add register
#     elif opcode == 6 : reg[r]=reg[r]-reg[addr]   # sub register
#     elif opcode == 7 : reg[r]=reg[r]*reg[addr]   # mul register
#     elif opcode == 8 : reg[r]=reg[r]/reg[addr]   # div register
#     elif opcode ==10 :
#         pReg=addr; updatePanel('pReg',pReg)      # jump unconditionally
#     elif opcode ==11 :
#         if reg[r]==0 :
#             pReg=addr; updatePanel('pReg',pReg)  # jump if register zero


# execute these - look up instruction, execute with operand, move instruction pointer
# how far to go in execution - have a word stack?

# thinking also of x threads with "." as loop round (execute sentences)

# what are the instructions, for examples: 

# - replace word with another
# - replace next word 
# - replace previous word
# - replace word at register
# - shift IP to new place
# - arithmetic on register
# - pop word onto stack
# - remove word from stack

