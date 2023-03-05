import random

def test(t):
        ''' Generic function that can contain anything to test and optimize. '''
        return abs(0.5-t)

def calculate_best_parameter(pop_r,best_parameter,smoothing_const=0.1):
        ''' This function averages all of the populations and then uses a smoothing function to create a best parameter.
            Smoothing function works like an EMA or IIR filter. (a*(c-1)+b)/c where c is normally the count overall for
            a running or stream average. In this case... a = a*(1-c) + b*c. Where c is a exponential weighting const that
            takes most of the old value and recurses it with a new b added in small doses. '''

        # Get the best parameter by averaging population.
        pop_avg = sum(pop_r)/len(pop_r)

        # In case the population values jump around due to mutations, smooth the average using EMA.
        if best_parameter is None: # First run, pre-load with the pop_avg to init.
                best_parameter = pop_avg
                print("Init Best Parameter.")
        else:
                best_parameter = best_parameter*(1-smoothing_const) + pop_avg * smoothing_const
                print("Best Parameter:",best_parameter)

        return best_parameter

def generate_random_trial(bounds):
        ''' Generate a uniform random trial value who's vale is constrained by the bounds. '''
        bias = bounds[0] # Find the midpoint and bias the range down from this point.
        range_of_optimize = bounds[1]-bounds[0] # Multiplier for the range of the search.
        rand_trial = (random.random()*range_of_optimize)+bias

        return rand_trial

# EXAMPLE STOCHASTIC ALGORITM normalized
def sa(pop,bounds=[0,1],opt_for_min=True):
        ''' Stochastic optimization. Precursor to GA. It just creates a random number and 
           is just like taking a guess, if the guess is better than the last one then 
           discard the last guess. Will work with just a population of one.
           Basically stripped down ga code.'''

        # Take a random sample from the population
        sample_pop = random.randint(0,len(pop)-1)
        print("Sample Population Index and Value",sample_pop,pop[sample_pop])
        fitness_ref = test(pop[sample_pop]) # Test fitness of the random sample via test function.

        # Generate a bounded uniform random value for the random trial.
        rand_trial = generate_random_trial(bounds)

        print("Random Trial Value:",rand_trial)
        fitness_rand_trial = test(rand_trial)
        print("Referance Fitness and Random Trial Fitness",fitness_ref,fitness_rand_trial)

        # Test for fitness, eliminating the original if the randomly generated A+B offspring shows better fitness.
        pop = fitness_evaluation(pop,opt_for_min,fitness_rand_trial,fitness_ref,rand_trial,sample_pop)

        return pop

def mutate(pop,bounds,mutation_rate):
        ''' Allows an element of the population picked at random to be mutated by replacement via a random value. '''
       # Mutation, mutate at a 5% rate, pick a random index and mutate that populatin with a random seed.
        if random.random() < mutation_rate:
                mut_index = random.randint(0,len(pop)-1)
                bias = bounds[0] # Find the midpoint and bias the range down from this point.
                range_of_optimize = bounds[1]-bounds[0] # Multiplier for the range of the search.
                pop[mut_index] = (random.random()*range_of_optimize)+bias
                print("---- Mutate Population at Index",mut_index)

        return pop


def random_pop_select(pop):
        ''' Randomly select two indexs to grab from the population. The while makes sure that they are unique.'''
        A = random.randint(0,len(pop)-1)
        B = random.randint(0,len(pop)-1)
        # Rechoose if they are equal to the same index. If the indexes are equal reselect until they are not. Quick+Dirty.
        while B == A:
                B = random.randint(0,len(pop)-1)

        return A,B

def generate_offspring(pop,A,B):
        ''' Use a regular average formula to generate the offspring. '''
        C_value = (pop[A]+pop[B])*0.5 # AVERAGE the Values of A and B.

        print("Breed:",A,B,C_value)

        return C_value

def fitness_evaluation(pop,opt_for_min,fitness_offspring,fitness_ref,C_value,sample_pop):
        ''' Evalute the fitness of the randomly selected (sample_pop) value versus the C_value which is
            the value of the offspring. Also determine if minimization, the default is occuring. Replace
            the population element at index sample_pop with the C-value if it helps with optimization through
            improved fitness. If not leave the  population the same. '''        
        if opt_for_min and fitness_offspring < fitness_ref: # Minimize the error in this case. Others cases may involve mazimizing op$
                pop[sample_pop] = C_value # Replace a element of pop with offspring.
                print("Replace with offspring that minimizes.")
        elif not opt_for_min and fitness_offspring < fitness_ref: # Maximizing optimization
                pop[sample_pop] = C_value # Replace a element of pop with offspring.
                print("Replace with offspring that maximizes.")
        else:
                print("Leave original.")

        return pop


# GENETIC ALGORITM
def ga(pop,bounds=[0,1],opt_for_min=True,mutation_rate=0.0):
        ''' Run a minimal genetic algorithm. Tests fitness of an element of the population.
            Creates offspring and then tests the fitness of the offspring.
            offspring is the average of two randomly selected elements, selected without 
            repeat. The fittest of them is selected and put in place of the orignally selected
            element.
            Calls function test that tests for fitness. 
            Called twice for both referance and trial fitness tests.
            mutation_rate is optional as it is set to zero by default no mutation occurs.'''            

        # Take a random sample
        sample_pop = random.randint(0,len(pop)-1)
        fitness_ref = test(pop[sample_pop]) # Test fitness of the random sample via test function.
        print("Test Fitness, pop# and fitness: ",sample_pop,fitness_ref) 

        # Breed at random. Random selection from population without replacement/duplication.
        A,B = random_pop_select(pop)

        # Offspring is taken using a simple average for this simple GA. C_value is the offspring value.
        C_value = generate_offspring(pop,A,B)

        # Test Fitness of offspring
        fitness_offspring = test(C_value) # Run the value of the offspring through the test function.
        print("Fitness Offsping:",fitness_offspring)


        # Test for fitness, eliminating the original if the randomly generated A+B offspring shows better fitness.
        pop = fitness_evaluation(pop,opt_for_min,fitness_offspring,fitness_ref,C_value,sample_pop)

       # Mutation, mutate at a 5% rate, pick a random index and mutate that populatin with a random seed.
        mutate(pop,bounds,mutation_rate)

        return pop

def init_population(pop,bounds):
        ''' Randomly uniform, init a population with bounded values set by bounds[0] and [1], lower,upper. '''
        bias = bounds[0] # Find the midpoint and bias the range down from this point.
        range_of_optimize = bounds[1]-bounds[0] # Multiplier for the range of the search.
        print(bias,range_of_optimize)
        # Randomly initialize population with uniform random from bounds[0] to bounds[1]
        for x in range(pop_len):
          pop.append((random.random()*range_of_optimize)+bias) # Append to the population as a list. Normalize to the range to optimize.
          print("initial population",x,pop[x])

        return pop

def show_final_population(pop):
        ''' Helper fxn to display the population when training the model is over. '''
        print("")
        for x in range(len(pop)):
                print("final population",x,pop[x])

#MAIN

pop = []

# The bounds are the lower and upper values for the search.
bounds = [0,1]

pop_len = 3 # Choose a population size
loops = 100
best_parameter = None

# Initialize a population uniform random within bounds [0] lower and [1] upper.
init_population(pop,bounds)


# Run the Genetic Algorithm Main Fxn
for n in range(0,loops):
        print("")
        print("--- Loop ---- :",n)
        print("")
        #ga(pop,bounds,mutation_rate=0.05)
        #pop_r = ga(pop,bounds,mutation_rate=0.05)
        pop_r = ga(pop,bounds)
        #pop_r = sa(pop,bounds) 

        # Converge in on the best parameter
        best_parameter = calculate_best_parameter(pop_r,best_parameter) 

show_final_population(pop)

