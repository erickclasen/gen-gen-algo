
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
best_fitness = 0

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

def deadwood_generate_random_trial(bounds): # Leave for now as example for range and bias
        ''' Generate a uniform random trial value who's vale is constrained by the bounds. '''
        bias = bounds[0] # Find the midpoint and bias the range down from this point.
        range_of_optimize = bounds[1]-bounds[0] # Multiplier for the range of the search.
        rand_trial = (random.random()*range_of_optimize)+bias

        return rand_trial

def generate_random_trial(bounds):
        ''' Generate a uniform random trial value who's vale is constrained by the bounds. '''
        rand_trial = (random.uniform(bounds[0],bounds[1]))

        return rand_trial

# EXAMPLE STOCHASTIC ALGORITM normalized
def sa(fxn_to_pass,pop,bounds=[0,1],opt_for_min=True):
        ''' Stochastic optimization. Precursor to GA. It just creates a random number and 
           is just like taking a guess, if the guess is better than the last one then 
           discard the last guess. Will work with just a population of one.
           Basically stripped down ga code.'''

        # Take a random sample from the population
        sample_pop = random.randint(0,len(pop)-1)
        print("Reference Sample taken from pop["+str(sample_pop)+"] with Value",sample_pop,pop[sample_pop])
        print("Run fitness test with reference...")
        fitness_ref = test(fxn_to_pass,pop[sample_pop]) # Test fitness of the random sample via test function.

        # Generate a bounded uniform random value for the random trial.
        rand_trial = generate_random_trial(bounds)

        print("Random Trial Value:",rand_trial)
        print("Run fitness test with random trail value...")
        fitness_rand_trial = test(fxn_to_pass,rand_trial)
        print("Referance Fitness and Random Trial Fitness",fitness_ref,fitness_rand_trial)

        # Test for fitness, eliminating the original if the randomly generated A+B offspring shows better fitness.
        pop = fitness_evaluation(pop,opt_for_min,fitness_rand_trial,fitness_ref,rand_trial,sample_pop)

        return pop

def mutate(pop,bounds,mutation_rate):
        ''' Allows an element of the population picked at random to be mutated by replacement via a random value. '''
       # Mutation, mutate at a 5% rate, pick a random index and mutate that populatin with a random seed.
        if random.random() < mutation_rate:
                mut_index = random.randint(1,len(pop)-1) # Don't mutate pop[0], the best one.
                pop[mut_index] = random.uniform(bounds[0],bounds[1])
                print("---- Mutate Population at Index",mut_index)

        return pop

def gaussian_mutate(pop,mutation_rate,std_dev=0.05,force=False):
        ''' Allows an element of the population picked at random to be mutated by replacement via a random value.
            This is based on a normal distribution and only slightly mutates the value. 

            Drives off of center of mass of population --- may or may not be a good idea in all cases.

            In theory this allows a slight dither mutation to occur, not a large mutation like generating a new 
            seed which should be more infrequent. A uniform mutation is like taking a element that was raised elsewhere, 
            on another island and putting into the population and letting it breed. Like a very distant breed. 

            With the Gaussian, the idea is to mutate just a little bit off of the center value of the population average. '''
       # Mutation, mutate at a 5% rate, pick a random index and mutate that populatin with a random seed.
        if random.random() < mutation_rate or force: # Happens infrequently unless force is used to make it happen.
                mut_index = random.randint(1,len(pop)-1) # Don't mutate pop[0], the best one.
                mean = sum(pop)/len(pop) # Center of mass of population.
                pop[mut_index] = random.gauss(mean,std_dev)
                print("---- Gaussian Mutate Population at Index",mut_index)

        return pop


def gaussian_mutate_element(pop,element,mutation_rate,std_dev=0.05,force=False):
        ''' Allows an element of the population picked BY LOCATION and to be mutated by replacement via a gaussian random value.
            This is based on a normal distribution and only slightly mutates the value. 
            In theory this allows a slight dither mutation to occur, not a large mutation like generating a new 
            seed which should be more infrequent. A uniform mutation is like taking a element that was raised elsewhere, 
            on another island and putting into the population and letting it breed. Like a very distant breed. 

            With the Gaussian, the idea is to mutate just a little bit off of the value to explore near space around the value
            of the pop[x] element, might help it find a better max/min. '''
       # Mutation, mutate at a 5% rate, pick a random index and mutate that populatin with a random seed.
        if random.random() < mutation_rate or force: # Happens infrequently unless force is used to make it happen.
                mean = sum(bounds)/2
                pop[element] = random.gauss(mean,std_dev)
                print("---- Gaussian Mutate Population at Index",mut_index)

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

        print("Breed: pop["+str(A)+"] and pop["+str(B)+"] , creating offspring with value:",C_value)

        return C_value

def fitness_evaluation(pop,opt_for_min,fitness_offspring,fitness_ref,C_value,sample_pop):
        ''' Evalute the fitness of the randomly selected (sample_pop) value versus the C_value which is
            the value of the offspring. Also determine if minimization, the default is occuring. Replace
            the population element at pop[sample_pop] with pop[0] and copy the C-value to pop[0] if it helps with
             optimization through improved fitness. If not leave the  population the same. 

             best_fitness takes on the value of the best fitness. When the new offspring is better than the
             best fitness, the best fitness gets updated and the following occurs...    
             The trick with copying pop[0] over the less fit pop[sample_pop] allows for demoting of the previous
             best value at pop[0], and promotion of the winner to pop[0] at all times.

             if the off spring is not more fit than best fitness but better than the reference than it updates
             the value refernce that it beat. pop[sample_pop]   the ref. gets overwritten with C_value, the offspring.

            '''
        global best_fitness     
        

        if opt_for_min and fitness_offspring < fitness_ref: # Minimize the error in this case. Others cases may involve mazimizing op$
                print("Optimize for Minimum.")

                if fitness_offspring < best_fitness:
                        best_fitness = fitness_offspring
                        print("Offspring -> pop[0] and breed offspring and pop[0] -> pop["+str(sample_pop)+"] , Update Best Fitness: ",best_fitness)
                        pop[sample_pop] =pop[0] # (pop[0] * C_value)/2  # Demote and breed the previous best fit with the new best, overwritting the less fit reference.
                        pop[0] = C_value # Replace a element of pop with offspring.
                else:
                        print("Offspring -> pop["+str(sample_pop)+"]")
                        pop[sample_pop] = C_value # Replace a element of pop with offspring.

        elif not opt_for_min and fitness_offspring > fitness_ref: # Maximizing optimization
                print("Optimize for Maximum.")

                if fitness_offspring > best_fitness and False:
                        best_fitness = fitness_offspring
                        print("Offspring -> pop[0] and breed offspring and pop[0] -> pop["+str(sample_pop)+"] , Update Best Fitness: ",best_fitness)
                        pop[sample_pop] = pop[0] #(pop[0] * C_value)/2  # Demote and breed the previous best fit with the new best, overwritting the less fit reference.
                        pop[0] = C_value # Replace a element of pop with offspring.
                else:
                        print("Offspring -> pop["+str(sample_pop)+"]")
                        pop[sample_pop] = C_value # Replace a element of pop with offspring.

        else:
                if fitness_offspring > best_fitness:
                        best_fitness = fitness_ref
                        print("Ref -> pop[0], Update Best Fitness: ",best_fitness)
                        temp = pop[sample_pop] # Save ref off. 
                        pop[sample_pop] = pop[0] #(pop[0] * temp)/2  # Demote and breed the previous best fit with the new best, overwritting the less fit reference.
                        pop[0] = temp # Replace pop[0] with ref
                else:
                        print("Leave original ref in pop["+str(sample_pop)+"]")


        print("pop[0]=",pop[0])
        return pop

def orig_fitness_evaluation(pop,opt_for_min,fitness_offspring,fitness_ref,C_value,sample_pop):
        ''' Evalute the fitness of the randomly selected (sample_pop) value versus the C_value which is
            the value of the offspring. Also determine if minimization, the default is occuring. Replace
            the population element at pop[sample_pop] with pop[0] and copy the C-value to pop[0] if it helps with
             optimization through improved fitness. If not leave the  population the same. 

             best_fitness takes on the value of the best fitness. When the new offspring is better than the
             best fitness, the best fitness gets updated and the following occurs...    
             The trick with copying pop[0] over the less fit pop[sample_pop] allows for demoting of the previous
             best value at pop[0], and promotion of the winner to pop[0] at all times.

             if the off spring is not more fit than best fitness but better than the reference than it updates
             the value refernce that it beat. pop[sample_pop]   the ref. gets overwritten with C_value, the offspring.

            '''
        global best_fitness     
        

        if opt_for_min and fitness_offspring < fitness_ref: # Minimize the error in this case. Others cases may involve mazimizing op$
                if fitness_offspring < best_fitness:
                        best_fitness = fitness_offspring
                        print("OM Update Best Fitness: ",best_fitness)
                        pop[sample_pop] = pop[0]  # Demote the previous best fit, overwritting the less fit reference.
                        pop[0] = C_value # Replace a element of pop with offspring.
                else:
                        pop[sample_pop] = C_value # Replace a element of pop with offspring.

                print("Replace with offspring that minimizes.")
        elif not opt_for_min and fitness_offspring > fitness_ref: # Maximizing optimization
                if fitness_offspring > best_fitness:
                        best_fitness = fitness_offspring
                        print("OM Update Best Fitness: ",best_fitness)
                        pop[sample_pop] = pop[0]  # Demote the previous best fit, overwritting the less fit reference.
                        pop[0] = C_value # Replace a element of pop with offspring.
                else:
                        pop[sample_pop] = C_value # Replace a element of pop with offspring.

                print("Replace with offspring that maximizes.")
        else:
                print("Leave original ref in posn: ",sample_pop)
                if fitness_offspring > best_fitness:
                        best_fitness = fitness_ref
                        print("LO Update Best Fitness: ",best_fitness)
                        temp = pop[sample_pop] # Save ref off. 
                        pop[sample_pop] = pop[0]  # Demote the previous best fit, overwritting the less fit reference.
                        pop[0] = temp # Replace pop[0] with ref


        print("pop[0]=",pop[0])
        return pop

# CALLABLE HELPER FXNS

def read_pop_from_file(filename="pop.json"):
    '''  Helper function to read in the population. Declutters the main function.    '''      


    # If the file exists read it in, if not just create an empty pop to be init'd in the run_algo fxn on the 1st run.
    try:
            with open(filename) as f_obj:
                    pop = json.load(f_obj)
    except IOError: #ValueError:
            pop = []

    return pop

def write_pop_to_file(pop,filename="pop.json"):
    '''  Helper function to write in the state, declutters the main algo function.'''

    with open(filename, 'w') as f_obj:
        json.dump(pop,f_obj)




# GENETIC ALGORITM
def ga(fxn_to_pass,pop,bounds,opt_for_min,mutation_rate):
        ''' Run a minimal genetic algorithm. Tests fitness of an element of the population.
            Creates offspring and then tests the fitness of the offspring.
            offspring is the average of two randomly selected elements, selected without 
            repeat. The fittest of them is selected and put in place of the orignally selected
            element.
            Calls function test that tests for fitness. 
            Called twice for both referance and trial fitness tests.
            mutation_rate is optional as it is set to zero by default no mutation occurs.'''            

        global best_fitness
        # Take a random sample normally but on first run use pop[0]
        # It is set as the best performer by the fitness test.
        if best_fitness == 0:
                print("First run use the best item saved at pop[0] as the reference...")
                fitness_ref = test(fxn_to_pass,pop[0])
                sample_pop = 0 # Force to zero.
        else:   # Normally take a random sample for reference.
                sample_pop = random.randint(0,len(pop)-1)
                print("Test fitness of reference at pop["+str(sample_pop)+"]...")
                fitness_ref = test(fxn_to_pass,pop[sample_pop]) # Test fitness of the random sample via test function.

        chksum = sum(pop)        

                
        # Breed at random. Random selection from population without replacement/duplication.
        A,B = random_pop_select(pop)

        # Offspring is taken using a simple average for this simple GA. C_value is the offspring value.
        C_value = generate_offspring(pop,A,B)

        # Test Fitness of offspring
        print("Test fitness of offspring...")
        fitness_offspring = test(fxn_to_pass,C_value) # Run the value of the offspring through the test function.

        # Print summary, can be commented out for less verbose output.
        print("Reference Fitness of pop["+str(sample_pop)+"] :",fitness_ref) 
        print("Fitness of Offsping:",fitness_offspring)


        # Test for fitness, eliminating the original if the randomly generated A+B offspring shows better fitness.
        pop = fitness_evaluation(pop,opt_for_min,fitness_offspring,fitness_ref,C_value,sample_pop)

       # Mutation, mutate at a 5% rate, pick a random index and mutate that populatin with a random seed.
        mutate(pop,bounds,mutation_rate)

        if sum(pop) == chksum:
                print("Same pop ")
                #gaussian_mutate(pop,mutation_rate,force=True)
        diversity = (max(pop)-min(pop))/(max(bounds)-min(bounds))
        print("Pop Diversity:",diversity)

        return pop

def init_population(pop,pop_init_len,bounds):
        ''' Randomly uniform, init a population with bounded values set by bounds[0] and [1], lower,upper. '''
        print("Bounds:",bounds)
        # Randomly initialize population with uniform random from bounds[0] to bounds[1]
        for x in range(pop_init_len):
          pop.append(random.uniform(bounds[0],bounds[1])) # Append to the population as a list. Normalize to the range to optimize.
          print("initial population",x,pop[x])

        return pop

def show_final_population(pop):
        ''' Helper fxn to display the population when training the model is over. '''
        print("")
        for x in range(len(pop)):
                print("final population",x,pop[x])


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
        count = 0 # Count loops, if pop changes gets reset, else ticks up.                                                                                               

        # Initialize a population uniform random within bounds [0] lower and [1] upper.
        if len(pop) == 0:
                print("Empty Population, Initial to random values.")
                init_population(pop,pop_init_len,bounds)

        # Loop the Genetic Algorithm Main Fxn
        for n in range(0,loops):

                epoch_count_print(n,loops)
                chksum = sum(pop) # checksum it, to compare below.

                # By default run the GA code, else SA example code to be able to sanity check.
                if run_ga_code:
                        pop = ga(fxn_to_pass,pop,bounds,opt_for_min,mutation_rate)
                else:
                        pop = sa(fxn_to_pass,pop,bounds=[0,1],opt_for_min=True)  # Example Stochastic fxn, when in doubt can be used as a sanity check as well.

                # Check for a pop that has settled. If so allow to run a bit more , then exit early.
                if count == 5:
                        print("Timeout.")
                        #break  # Watchdog timeout.
                elif chksum == sum(pop):
                        print("No change in pop. Timeout Count: ",count)
                        count += 1 # Pending watchdog timeout.
                else:
                        count = 0 # Watchdog reset


        # Final results
        print("The End: "+str(n)+" of ",loops)

        show_final_population(pop)

        # Return so that the code that is calling this fxn can do something with it like use it or store it
        return pop
# MAIN
# UNIT TEST DEBUG
import statistics
import csv
out_list = []
raw_list = []


for n in range(0,100):

        pop = run_algo(example_called_fxn,pop=[],loops=100)

        diversity = (max(pop)-min(pop))/(1-0)
        print("Diversity:",diversity)
        a = statistics.stdev(pop)

        print("Stddev",a)

        if a > 0:
                print("ratio",diversity/a)



        out_list.append(str(a)) # CUML GAIN
        out_list.append("") # CUML GAIN

        raw_list.append(a)

print("Sum of Stddevs Score:",sum(raw_list))

exit()
    #Open the CSV file and output a row using the out_list
with open("test.csv", mode='a') as outfile:
        output_writer = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        output_writer.writerow(out_list)



