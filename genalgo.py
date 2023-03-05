#!/usr/bin/python
#title                  :genalgo.py
#description    :A module that contains Genetic Algorithm Code that can be used for optimization or in a machine learning application. Also cotains a basic stochastic optimization algorithm as a warmup.
#author                 :Erick Clasen
#date                   :20200610
#version                :1.0
#usage                  :python genalgo.py
#notes                  :
#python_version :2.6.6
#==============================================================================


import random
import json


def example_called_fxn(t):
        #return pow(pow(0.5-t,2),0.5) # RMS Error
        return abs(0.5-t) # The error value, how far it is away from 0.5, this is to be minimized.



def test(fxn,t):
        ''' Generic function that can contain anything to test and optimize. It uses a function passed in
            as an argument. In this way any function to be optimized can be called by reference by either passing it in
            OR mosre importantly calling its label in this function. Thereby just modding it in one place.
            the called_fxn must appear or be imported above this function in order to be defined!
            This test function just is a wrapper and returns the so called output of the function called to be
            optimized. '''
        
        return fxn(t)


def calculate_best_parameter(pop,best_parameter,smoothing_const=0.1):
        ''' This function averages all of the populations and then uses a smoothing function to create a best parameter.
            Smoothing function works like an EMA or IIR filter. (a*(c-1)+b)/c where c is normally the count overall for
            a running or stream average. In this case... a = a*(1-c) + b*c. Where c is a exponential weighting const that
            takes most of the old value and recurses it with a new b added in small doses. '''

        # Get the best parameter by averaging population.
        pop_avg = sum(pop)/len(pop)

        # In case the population values jump around due to mutations, smooth the average using EMA.
        if best_parameter is None: # First run, pre-load with the pop_avg to init.
                best_parameter = pop_avg
                print("Init Best Parameter to Population Average.")
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
def sa(fxn_to_pass,pop,bounds=[0,1],opt_for_min=True):
        ''' Stochastic optimization. Precursor to GA. It just creates a random number and 
           is just like taking a guess, if the guess is better than the last one then 
           discard the last guess. Will work with just a population of one.
           Basically stripped down ga code.'''

        # Take a random sample from the population
        sample_pop = random.randint(0,len(pop)-1)
        print("Sample Population Index and Value",sample_pop,pop[sample_pop])
        fitness_ref = test(fxn_to_pass,pop[sample_pop]) # Test fitness of the random sample via test function.

        # Generate a bounded uniform random value for the random trial.
        rand_trial = generate_random_trial(bounds)

        print("Random Trial Value:",rand_trial)
        fitness_rand_trial = test(fxn_to_pass,rand_trial)
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

# CALLABLE HELPER FXNS

def read_pop_from_file(filename="pop.json"):
    '''  Helper function to read in the population. Declutters the main function.    '''      


    # If the file exists read it in, if not just create an empty pop to be init'd in the run_algo fxn on the 1st run.
    try:
            with open(filename) as f_obj:
                    pop = json.load(f_obj)
    except ValueError:
            pop = []

    return pop

def write_pop_to_file(pop,filename="pop.json"):
    '''  Helper function to write in the state, declutters the main algo function.'''

    with open(filename, 'w') as f_obj:
        json.dump(pop,f_obj)




# GENETIC ALGORITM
def ga(fxn_to_pass,pop,bounds=[0,1],opt_for_min=True,mutation_rate=0.0):
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
        fitness_ref = test(fxn_to_pass,pop[sample_pop]) # Test fitness of the random sample via test function.


        # Breed at random. Random selection from population without replacement/duplication.
        A,B = random_pop_select(pop)

        # Offspring is taken using a simple average for this simple GA. C_value is the offspring value.
        C_value = generate_offspring(pop,A,B)

        # Test Fitness of offspring
        fitness_offspring = test(fxn_to_pass,C_value) # Run the value of the offspring through the test function.

        # Print summary, can be commented out for less verbose output.
        print("Test Fitness, pop# and fitness: ",sample_pop,fitness_ref) 
        print("Fitness Offsping:",fitness_offspring)


        # Test for fitness, eliminating the original if the randomly generated A+B offspring shows better fitness.
        pop = fitness_evaluation(pop,opt_for_min,fitness_offspring,fitness_ref,C_value,sample_pop)

       # Mutation, mutate at a 5% rate, pick a random index and mutate that populatin with a random seed.
        mutate(pop,bounds,mutation_rate)

        return pop

def init_population(pop,pop_init_len,bounds):
        ''' Randomly uniform, init a population with bounded values set by bounds[0] and [1], lower,upper. '''
        bias = bounds[0] # Find the midpoint and bias the range down from this point.
        range_of_optimize = bounds[1]-bounds[0] # Multiplier for the range of the search.
        print(bias,range_of_optimize)
        # Randomly initialize population with uniform random from bounds[0] to bounds[1]
        for x in range(pop_init_len):
          pop.append((random.random()*range_of_optimize)+bias) # Append to the population as a list. Normalize to the range to optimize.
          print("initial population",x,pop[x])

        return pop

def show_final_population(pop):
        ''' Helper fxn to display the population when training the model is over. '''
        print("")
        for x in range(len(pop)):
                print("final population",x,pop[x])

def optimize_by_delta_best_parameter(optimization_threshold,best_parameter,prior_best_parameter,n,loops,warmup_loops=10):
        ''' Instead of using loops alone, allow an early breakout of the code when a minimum delta of the best parameter
            minus the prior best parameter becomes lower than a threshold value that is a hyperparameter passed into the
            run algo fxn.

        '''     
        
        break_out = False # Always false unless a breakout condition is reached.

        if prior_best_parameter is not None and n > warmup_loops: # Make for a warmup. 
                # If the best parameter has settled to a value without improvement, optimization is complete.
                if abs(best_parameter - prior_best_parameter) < optimization_threshold:
                                break_out = True # Set for a break out of code in the upper loop, run_algo.

        # Update the prior if a real value is available.
        if best_parameter is not None:
                prior_best_parameter = best_parameter

        print(best_parameter,prior_best_parameter)

        return prior_best_parameter,break_out


def epoch_count_print(n,loops):
        ''' Helper, just prints out the epoch aka loop count every 10 loops. '''
        if n % 10 == 0:
                print("")
                print("Epoch: "+str(n)+" of ",loops)
        print("") # Print one space every time through for better formatting




# ------------------------------------------------------------------------------------------------------------
def run_algo(fxn_to_pass,pop=[],bounds=[0,1],opt_for_min=True,mutation_rate=0.0,pop_init_len=10,loops=10,optimization_threshold=0.0,warmup_loops=10,smoothing_const=0.1,run_ga_code=True):
        ''' Outer code that initializes and then runs the genetic algo code by looping. Made into a fxn so
            it can be called from other code by importing. Inits pop of length default of 10 pop_init_len
            for a specific number of loops default to 10, mutation rate of 0.0 means no mutation by default.
            opt for min, optimize for minimum by default.       

                pop: The population optional passed from outside the fxn by loading using the read pop fxn.
                bounds: The bounds are the lower and upper values for the search. Normalizes the serach to the data range.

                opt_for_min: The default mode is True to optimize for a minimum, like error. Can be set False to optimize for Maximum.

                pop_init_len: population size to initialize to, stays constant once initialized.

                loops : How many times to loop through the ga.
                
                Alternatively, allow breakout early based on convergance of delta value of best parameter, break on
                a value less than a threshold.
                
                optimization_threshold: Hyperparameter, when non zero it is the value of delta best parameter at which to early the code
                early as it has optimized enough.
        
                warmup_loops: Defaults to 10, number of loops to run before allowing early breakout on optimization.

                smoothing_const: The Rate of decay for the EMA that calculates the best parameter, default = 0.1.

                run_ga_code: By default the GA algorithm is run, if this is set or passed as False then the SA,
                Stochastic Algorithm is run, mostly for a demo and to use as a sanity check. Lets say running the 
                GA code is giving weird results or a warmup test is needed to just get going. Getting an optimization
                up and running or debugged with the SA code means less hyperparams to worry about and when it works 
                with SA than goto GA (again) to adjust hyperparameters.

                ??? verbose: Turns on verbose messaging, mostly for debug. Turned off means less printed info when the epochs run.

                                                                                                '''

        # The value of the best parameter, based on the population and a running average that slowly converges to the best parameter value.
        best_parameter = None
        # Value of best parameter at loop # -1, to create a delta of the best parameter from.
        prior_best_parameter = None

        # Initialize a population uniform random within bounds [0] lower and [1] upper.
        if len(pop) == 0:
                print("Empty Population, Initial to random values.")
                init_population(pop,pop_init_len,bounds)

        # Loop the Genetic Algorithm Main Fxn
        for n in range(0,loops):

                epoch_count_print(n,loops)

                # By default run the GA code, else SA example code to be able to sanity check.
                if run_ga_code:
                        pop = ga(fxn_to_pass,pop,bounds=[0,1],opt_for_min=True,mutation_rate=0.0)
                else:
                        pop = sa(fxn_to_pass,pop,bounds=[0,1],opt_for_min=True)  # Example Stochastic fxn, when in doubt can be used as a sanity check as well.

                # Converge in on the best parameter
                best_parameter = calculate_best_parameter(pop,best_parameter,smoothing_const=0.1) 

                # Allow an early breakout if optimized enough based on best_parameter deltas settling below
                # an optimization_threshold after a preset number of warmup_loops, defaults at 10.
                if optimization_threshold > 0: # Only if in breakout early when optimized mode is active.
                        prior_best_parameter,break_out = optimize_by_delta_best_parameter(optimization_threshold,best_parameter,prior_best_parameter,n,loops,warmup_loops=10)
                        # Exit early if a breakout signal is sent by optimize_by_delta_best_parameter.
                        if break_out:
                                break

        # Final results
        print("The End: "+str(n)+" of ",loops)

        show_final_population(pop)

        # Return so that the code that is calling this fxn can do something with it like use it or store it
        return pop,best_parameter
# MAIN
# UNIT TEST DEBUG
#run_algo(example_called_fxn)
