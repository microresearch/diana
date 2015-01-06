import random,pickle
import nltk

# modify for weighted listDONE

from pyevolve import G1DList
from pyevolve import GSimpleGA, Consts
from pyevolve import Selectors
from pyevolve import Initializators, Mutators, Crossovers
import math

def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)

def choose(listie):
# but we need counter for each POS! - in each list as listie[0] but where is code?
    count=listie[0]+1
    if count>len(listie):
        listie[0]=0
        count=1
    else:
        listie[0]=count
    return listie[count]

#train_txt = open("/root/collect2012-3/diana/documents/paget.txt").read()
train_txt = open("/root/diana/chapters/3_glass-crash/texts/wounds/crashwounds").read()
train_txt = removeNonAscii(train_txt)
#train_txt = open("crash.txt").read()
#train_txt = open("allnvfmold").read()

train_sens = nltk.sent_tokenize(train_txt)
train_txt = []
for sen in train_sens:
    train_txt += nltk.pos_tag(nltk.word_tokenize(sen))

# pickle the tokenised

#out = open("crash_tagged004.pickle", 'rb')
#out = open("paget_tagged2.pickle", 'rb')
#out = open("witness_tagged.pickle", 'rb') TAGGD ONLY FOR LOC?PERSON

#train_txt=pickle.load(out) 

#print train_txt

mm = {}


for tword in train_txt:
#    print tword
    if not(tword[1] in mm):
#        mm[tword[1]] = [0]
#        mm[tword[1]].append(tword[0])
        mm[tword[1]] = [tword[0]]
    else:
        mm[tword[1]].append(tword[0])

ll=mm.keys()
ll.sort()
#print ll

#1]

# so we have our prefered sequence expressed as series of numbers referencing ll dictionary

sentence="Almost every conceivable violent confrontation between the automobile and its occupants was listed: mechanisms of passenger ejection, the geometry of kneecap and hip-joint injuries, deformation of passenger compartments in head-on and rear-end collisions, injuries sustained in accidents at roundabouts, at trunkroad intersections, at the junctions between access roads and motorway intersections, the telescoping mechanisms of car-bodies in front-end collisions, abrasive injuries formed in roll-overs, the amputation of limbs by roof assemblies and door sills during roll-over, facial injuries caused by dashboard and window trim, scalp and cranial injuries caused by rear-view mirrors and sun-visors, whiplash injuries in rear-end collisions, first and second-degree burns in accidents involving the rupture and detonation of fuel tanks, chest injuries caused by steering column impalements, abdominal injuries caused by faulty seat-belt adjustment, second-order collisions between front-seat and rear-seat passengers, cranial and spinal injuries caused by ejection through windshields, the graded injuries to the skull caused by variable windshield glasses, injuries to minors, both children and infants in arms, injuries caused by prosthetic limbs, injuries caused within cars fitted with invalid controls, the complex self-amplifying injuries of single and double amputees, injuries caused by specialist automobile accessories such as record players, cocktail cabinets and radiotelephones, the injuries caused by manufacturers' medallions, safety belt pinions and quarter-window latches."

sentence=removeNonAscii(sentence)

# convert Ballard sentence to these numbers

sens = nltk.sent_tokenize(sentence)
crash = []
indexcrash=[]
randomcrash=[]
for sen in sens:
    crash += nltk.pos_tag(nltk.word_tokenize(sen))

# start with random sequence of same length

for word in crash:
    pos = word[1]
        # print position of pos in ll
    if pos in ll:
        indexcrash+=ll.index(pos),    
    randomcrash.append(random.randint(0,len(ll)))

#print indexcrash
#print randomcrash

# iterate genetic development towards our preferred sequence

#2]

# interbreeding of chunks for sentence generation or for NP chunkings


# for x in range(100):
#     out = ""
#     for word in crash:
# #        pos = word[1]
# #    print word
#         newword = ""
#         try:
# #        newword = choose(mm[word[1]]) # + " "
#             newword = random.choice(mm[word[1]]) # choose from POS key
# #        print mm[word[1]]
#         except:
#             newword = word[0]
#         out += newword + " "
#     print out+"\n"
        
# outfile = open("crashpaget002", "w")
# outfile.write(out)
# outfile.close()

numeric_sentence = indexcrash

def evolve_callback(ga_engine):
   generation = ga_engine.getCurrentGeneration()
   if generation%50==0:
      indiv = ga_engine.bestIndividual()
      out = ""
      for posnum in indiv:
          newword = ""
          # choose random word from pos key
          poskey=ll[posnum]
          newword = random.choice(mm[poskey]) # choose from POS key
          out += newword + " "
      print out+"\n"


   return False

# def eval_func(chromosome):
#    score = 0.0
#    print chromosome
#    score += 0.1
#    return score


def run_main():
   genome = G1DList.G1DList(len(sentence))
   genome.setParams(rangemin=min(numeric_sentence),
                    rangemax=max(numeric_sentence),
                    bestrawscore=0.00,
                    gauss_mu=1, gauss_sigma=4)

   genome.initializator.set(Initializators.G1DListInitializatorInteger)
   genome.mutator.set(Mutators.G1DListMutatorIntegerGaussian)
   genome.evaluator.set(lambda genome: sum(
                           [abs(a-b) for a, b in zip(genome, numeric_sentence)]
                        ))
#   genome.evaluator.set(eval_func)

   ga = GSimpleGA.GSimpleGA(genome)
   ga.stepCallback.set(evolve_callback)
   ga.setMinimax(Consts.minimaxType["minimize"])
   ga.terminationCriteria.set(GSimpleGA.RawScoreCriteria)
   ga.setPopulationSize(60)
   ga.setMutationRate(0.02)
   ga.setCrossoverRate(0.9)
   ga.setGenerations(5000)
   ga.evolve(freq_stats=100)

   best = ga.bestIndividual()
   print "Best individual score: %.2f" % (best.score,)
#   print ''.join(map(chr, best)) # prints junk

if __name__ == "__main__":
   run_main()


