import random,pickle
import nltk
import math
from textclean.textclean import textclean

# FITNESS BY HAND - but use a smaller population

POPSIZE=100
SENTSIZE=24

# or automatically score according to POS distance from ideal
# number of POS/position matches

sentence="Almost every conceivable violent confrontation between the automobile and its occupants was listed: mechanisms of passenger ejection, the geometry of kneecap and hip-joint injuries, deformation of passenger compartments in head-on and rear-end collisions, injuries sustained in accidents at roundabouts, at trunkroad intersections, at the junctions between access roads and motorway intersections, the telescoping mechanisms of car-bodies in front-end collisions, abrasive injuries formed in roll-overs, the amputation of limbs by roof assemblies and door sills during roll-over, facial injuries caused by dashboard and window trim, scalp and cranial injuries caused by rear-view mirrors and sun-visors, whiplash injuries in rear-end collisions, first and second-degree burns in accidents involving the rupture and detonation of fuel tanks, chest injuries caused by steering column impalements, abdominal injuries caused by faulty seat-belt adjustment, second-order collisions between front-seat and rear-seat passengers, cranial and spinal injuries caused by ejection through windshields, the graded injuries to the skull caused by variable windshield glasses, injuries to minors, both children and infants in arms, injuries caused by prosthetic limbs, injuries caused within cars fitted with invalid controls, the complex self-amplifying injuries of single and double amputees, injuries caused by specialist automobile accessories such as record players, cocktail cabinets and radiotelephones, the injuries caused by manufacturers' medallions, safety belt pinions and quarter-window latches."

# convert Ballard sentence to these numbers

sens = nltk.sent_tokenize(sentence)
crashier = []
for sen in sens:
	crashier += nltk.pos_tag(nltk.word_tokenize(sen))

# read-in ballard section (chap14)
crash_raw = open("/root/diana/chapters/3_glass-crash/texts/chap14").read() 
#crash_raw = open("crash.txt").read() 
# own section
crash_raw += open("/root/diana/chapters/3_glass-crash/texts/ownshort").read() 
# diana section
crash_raw = open("/root/diana/chapters/3_glass-crash/texts/shortpaget").read() 
#crash_raw = open("death_strip1").read() 

crash_raw = textclean.clean(crash_raw)

# generate POPULATION: ballardian noun-phrases(methods? - fixed grammar with
# weighted choices, permutations, markov??)

sens = nltk.sent_tokenize(crash_raw)
crash = []
for sen in sens:
    crash += nltk.word_tokenize(sen)

def weighted_choice(items):
  """
  Chooses a random element from items, where items is a list of tuples in
  the form (item, weight). weight determines the probability of choosing its
  respective item. Note: this function is borrowed from ActiveState Recipes.
  """
  weight_total = sum((item[1] for item in items))
  n = random.uniform(0, weight_total)
  for item, weight in items:
    if n < weight:
      return item
    n = n - weight
  return item


def fitness(dna): # fitness is inverse
  fitness = 50
  tagged = nltk.pos_tag(nltk.word_tokenize(" ".join(dna)))
  x=0
  for word in tagged:
      if word[1]==crashier[x][1]: fitness=fitness-1
      x+=1
# other ways for fitness: 
# -- distance from ideal ballardian sentence (not just matching)
# -- how well (size of phrase) we match IP (injury phrase)... evolving injuries...
#   print 
#   print " ".join(dna)
#   fitness = raw_input("Score: ")
  return 100-int(fitness)

def genballardpop():
  pop = []
  for i in range(POPSIZE):
      ttt=[]
      for xx in range(SENTSIZE):
          ttt.append(a(crash))
      pop.append(ttt)
  return pop

#print genballardpop()

# mutate-replace random word with another chosen from text

def a(input):
    x = input[random.randint(0,len(input) - 1)]
    return x

def random_word():
    return a(crash)

def mutate(dna):
  dna_out = []
  mutation_chance = 10
  for c in xrange(len(dna)):
    if int(random.random()*mutation_chance) == 1:
      dna_out.append(random_word())
    else:
      dna_out.append(dna[c])
  return dna_out

xxx=genballardpop()
#print mutate(xxx[0])

# crossover on words

def crossover(dna1, dna2):
# for sentences of varying size???
#smallest
    senta=len(dna1)
    sentb=len(dna2)
    if senta>sentb:
        sntsize=sentb
    else:
        sntsize=senta

    pos = int(random.random()*sntsize) 
    return (dna1[:pos]+dna2[pos:], dna2[:pos]+dna1[pos:])

#print crossover(xxx[0],xxx[1])

# judge fittest by hand (score prompt)
# mutate-mate these
# repeat!

population = xxx

for generation in xrange(500):
    print "Generation %s... Random sample: '%s' Fitness: %s" % (generation, " ".join(population[0]), fitness(population[0]))
#    for m in population:
#        print " ".join(m)
    weighted_population = []

    # Add individuals and their respective fitness levels to the weighted
    # population list. This will be used to pull out individuals via certain
    # probabilities during the selection phase. Then, reset the population list
    # so we can repopulate it after selection.
    for individual in population:
      fitness_val = fitness(individual) 

      # Generate the (individual,fitness) pair, taking in account whether or
      # not we will accidently divide by zero.
      if fitness_val == 0:
        pair = (individual, 1.0)
      else:
        pair = (individual, 1.0/fitness_val)

      weighted_population.append(pair)

    population = []

    # Select two random individuals, based on their fitness probabilites, cross
    # their genes over at a random point, mutate them, and add them back to the
    # population for the next iteration.
    for _ in xrange(POPSIZE/2):
      # Selection
      ind1 = weighted_choice(weighted_population)
      ind2 = weighted_choice(weighted_population)

      # Crossover
      ind1, ind2 = crossover(ind1, ind2)

      # Mutate and add back into the population.
      population.append(mutate(ind1))
      population.append(mutate(ind2))



