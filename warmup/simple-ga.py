import random

def test(t):
        ''' Generic function that can contain anything to test and optimize. '''
        return abs(0.5-t)

def sa(pop,opt_for_min=True):
        ''' Stochastic optimization. Precursor to GA. It just creates a random number and 
           is just like taking a guess, if the guess is better than the last one then 
           discard the last guess. Will work with just a population of one.
           Basically stripped down ga code.'''

        # Take a random sample
        sample_pop = random.randint(0,len(pop)-1)
        print("Sample Population Index and Value",sample_pop,pop[sample_pop])
        fitness_ref = test(pop[sample_pop]) # Test fitness of the random sample via test function.

        rand_trial = random.random() # Generate a random number 0-1.
        print("Random Trial Value:",rand_trial)
        fitness_rand_trial = test(rand_trial)
        print("Referance Fitness and Random Trial Fitness",fitness_ref,fitness_rand_trial)

        # Test for fitness, eliminating the original if the randomly generated A+B offspring shows better fitness.
        if opt_for_min and fitness_rand_trial < fitness_ref: # Minimize the error in this case. Others cases may involve mazimizing op$
                pop[sample_pop] = rand_trial # Replace a element of pop with random trial.
                print("Replace with offspring that minimizes.")
        elif not opt_for_min and fitness_rand_trial < fitness_ref: # Maximizing optimization
                pop[sample_pop] = rand_trial # Replace a element of pop with random trial.
                print("Replace with offspring that maximizes.")
        else:
                print("Leave original.")




def minimal_ga(pop,opt_for_min=True):
        ''' Run a minimal genetic algorithm. Tests fitness of an element of the population.
            Creates offspring and then tests the fitness of the offspring.
            offspring is the average of two randomly selected elements, selected without 
            repeat. The fittest of them is selected and put in place of the orignally selected
            element.
            Calls function test that tests for fitness. 
            Called twice for both referance and trial fitness tests.'''                 

        # Take a random sample
        sample_pop = random.randint(0,len(pop)-1)
        fitness_ref = test(pop[sample_pop]) # Test fitness of the random sample via test function.
        print("Test Fitness, pop# and fitness: ",sample_pop,fitness_ref) 

        # Breed at random. Random selection from population without replacement/duplication.
        A = random.randint(0,len(pop)-1)
        B = random.randint(0,len(pop)-1)
        # Rechoose if they are equal to the same index. If the indexes are equal reselect until they are not. Quick+Dirty.
        while B == A:
                B = random.randint(0,len(pop)-1)

        # Offspring is taken using a simple average for this simple GA.
        C_value = (pop[A]+pop[B])*0.5 # AVERAGE
        
        print("Breed:",A,B,C_value)

        # Test Fitness of offspring
        fitness_offspring = test(C_value) # Run the value of the offspring through the test function.
        print("Fitness Offsping:",fitness_offspring)

        # Test for fitness, eliminating the original if the randomly generated A+B offspring shows better fitness.
        if opt_for_min and fitness_offspring < fitness_ref: # Minimize the error in this case. Others cases may involve mazimizing optimization.
                pop[sample_pop] = C_value # Replace a element of pop with offspring.
                print("Replace with offspring that minimizes.")
        elif not opt_for_min and fitness_offspring < fitness_ref: # Maximizing optimization
                pop[sample_pop] = C_value # Replace a element of pop with offspring.
                print("Replace with offspring that maximizes.")
        else:
                print("Leave original.")


#MAIN

pop = []
pop_len = 5 # Choose a population size
loops = 200
# Randomly initialize population with uniform random from 0-1
for x in range(pop_len):
  pop.append(random.random()) # Append to the population as a list.
  print("initial population",x,pop[x])

# Run the Genetic Algorithm Main Fxn
for n in range(0,loops):
        print("")
        print("--- Loop ---- :",n)
        print("")
        minimal_ga(pop)
        #sa(pop) 

for x in range(len(pop)):
        print("final population",x,pop[x])

