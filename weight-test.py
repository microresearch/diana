import nltk,random
from pyevolve import G1DList
from pyevolve import GSimpleGA, Consts
from pyevolve import Selectors
from pyevolve import Initializators, Mutators, Crossovers
import math
from textclean.textclean import textclean

train_txt = open("/root/diana/chapters/3_glass-crash/texts/allnvfmold").read()
#train_txt = open("crash.txt").read()
#train_txt = open("allnvfmold").read()

train_txt = textclean.clean(train_txt)

train_sens = nltk.sent_tokenize(train_txt)
train_txt = []
for sen in train_sens:
    train_txt += nltk.pos_tag(nltk.word_tokenize(sen))

fdist1 = nltk.FreqDist(train_txt) 
vocab = fdist1.keys()

#  list of tuples of weights 

wordposweightlist=[]

#for word in train_txt:
#    wordposweightlist.append((word, fdist1[word]/float(fdist1[vocab[0]])))

#takes a weighted list and returns a random selection
#assuming the second item in the tuple is the weight

def choose_weighted(wlist):
     if isinstance(wlist, list):
         wlist.sort(key=lambda x: x[1])
         choice = random.random() * sum(j for i, j in wlist)
         for i, w in wlist:
             choice -= w
             if choice < 0:
                 return i
     else:
         return wlist[0]

mm = {}

def insertTuple(d, k, tup):
    if k not in d:
        d[k] = tup
    elif type(d[k]) == tuple:
        d[k] = [ d[k], tup ]
    elif not(tup in d[k]):
        d[k].append(tup) # fixed for repeats

for tword in train_txt:
    insertTuple(mm, tword[1], ([tword[0]],fdist1[tword]))

#print choose_weighted(mm["VBN"])

ll=mm.keys()
ll.sort()
#print ll

sentence="Almost every conceivable violent confrontation between the automobile and its occupants was listed: mechanisms of passenger ejection, the geometry of kneecap and hip-joint injuries, deformation of passenger compartments in head-on and rear-end collisions, injuries sustained in accidents at roundabouts, at trunkroad intersections, at the junctions between access roads and motorway intersections, the telescoping mechanisms of car-bodies in front-end collisions, abrasive injuries formed in roll-overs, the amputation of limbs by roof assemblies and door sills during roll-over, facial injuries caused by dashboard and window trim, scalp and cranial injuries caused by rear-view mirrors and sun-visors, whiplash injuries in rear-end collisions, first and second-degree burns in accidents involving the rupture and detonation of fuel tanks, chest injuries caused by steering column impalements, abdominal injuries caused by faulty seat-belt adjustment, second-order collisions between front-seat and rear-seat passengers, cranial and spinal injuries caused by ejection through windshields, the graded injuries to the skull caused by variable windshield glasses, injuries to minors, both children and infants in arms, injuries caused by prosthetic limbs, injuries caused within cars fitted with invalid controls, the complex self-amplifying injuries of single and double amputees, injuries caused by specialist automobile accessories such as record players, cocktail cabinets and radiotelephones, the injuries caused by manufacturers' medallions, safety belt pinions and quarter-window latches."

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
#    print pos
        # print position of pos in ll
    indexcrash+=ll.index(pos),    
    randomcrash.append(random.randint(0,len(ll)))

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
          #print mm[poskey]
#          newword = random.choice(mm[poskey]) # choose from POS key
          newword=''.join(choose_weighted(mm[poskey])) # choose from POS key - weighted
          out += newword + " "
      print out+"\n"
#          print newword
   return False

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
