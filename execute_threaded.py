# using POS (part of speech tag as instruction and frequency code as operand)

import nltk, random

train_txt = open("/root/diana/chapters/3_glass-crash/texts/wounds/crashwounds").read()
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
x=0

# how can we handle threads? as a list parsed from the beginning?
# and each thread with IP, local register and a (leaking) stack

threads=[]
ip=[]
stack=[]
register=[]

sent=[]
for elements in xx:
	sent.append(elements)
	if elements[0][0]==".":
		threads.append(sent)
		sent=[]
		ip.append(0)
		stack.append([])
		register.append(0)

# execute these - look up instruction, execute with operand, move instruction pointer
# how far to go in execution - have a word stack?

xxx=1

while xxx:
	#some leakage in stacks
	if random.randint(0,10)==1:
		# leak one stack into another
		fro=random.randint(0,len(threads)-1)
		too=random.randint(0,len(threads)-1)
		if len(stack[fro])>0 and too !=fro:
			stack[too].append(stack[fro].pop())

	for thread in threads:
		x=threads.index(thread)
		lenny=len(thread)
		ip[x]=ip[x]+1
		if ip[x]>=lenny: ip[x]=0
		IP=ip[x]
		opcode=instructionlist.index(thread[IP][0][1])
		operand=thread[IP][1]
		opcode=opcode%11
#		print thread[IP][0][0], # print the word

		opcode=instructionlist.index(thread[IP][0][1])
		operand=thread[IP][1]
#	print "instruction %s operand %s" % (opcode,operand)
		opcode=opcode%13
#		print thread[IP][0][0], # print the word
		if   opcode == 0: #x=1 do nothing
		# change to print word AT register address
	#		x=1
			print thread[register[x]%lenny][0][0],
		if   opcode == 1:
			which = operand %3
			if which == 0:
				newword = random.choice(mm[thread[IP][0][1]])
			elif which == 1:
				newword = mm[thread[IP][0][1]][operand%len(mm[thread[IP][0][1]])]	
			elif which ==2:
				# change POS
				newword = random.choice(random.choice(mm.values()))
#				print newword
			thread[IP]=(newword,fdist1[newword])
		elif opcode == 2: # change prev word
			newword = random.choice(mm[thread[IP][0][1]]) # choose from POS key 
			where=IP-1
			if where<0: where=0
			thread[where]=(newword,fdist1[newword])
		elif opcode == 3: # change next word
			newword = random.choice(mm[thread[IP][0][1]]) # choose from POS key 
			where=IP+1
			if where==len(thread): where=len(thread)-1
			thread[where]=(newword,fdist1[newword])
			IP+=1
		elif opcode == 4:
			IP=operand%len(thread)
		elif opcode == 5:
			if register[x]==0:
				IP=operand%len(thread)
		elif opcode == 6:
			newword = random.choice(mm[thread[IP][0][1]]) # choose from POS key 
			where=register[x]%lenny
			thread[where]=(newword,fdist1[newword])
		elif opcode == 7:
			newword = random.choice(mm[thread[register[x]%lenny][0][1]]) # choose from POS key at register[x] 
			where=IP
			thread[where]=(newword,fdist1[newword])
		elif opcode == 8:
			# load register[x] from word at operand
			register[x]=instructionlist.index(thread[operand%len(thread)][0][1])
		elif opcode == 9:
			register[x]=(register[x]+instructionlist.index(thread[operand%len(thread)][0][1]))%len(thread)
		elif opcode == 10:
			register[x]=(register[x]-instructionlist.index(thread[operand%len(thread)][0][1]))%len(thread)
		elif opcode == 11:
#			print "push"
			# put word at register on stack
			forstack=thread[register[x]%lenny][0]
			stack[x].append(forstack)
		elif opcode == 12:
			# pop current word from stack onto IP
			if len(stack[x])>0:
				offstack=stack[x].pop()
				thread[IP]=(offstack,fdist1[offstack])			
#				print offstack
